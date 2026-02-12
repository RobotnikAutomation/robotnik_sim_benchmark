#include <chrono>
#include <deque>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <memory>
#include <optional>
#include <string>
#include <utility>
#include <vector>
#include <cmath>
#include <filesystem>
#include <random>
#include <cctype>

#include "rclcpp/rclcpp.hpp"
#include "rclcpp/generic_subscription.hpp"
#include "rclcpp/serialization.hpp"
#include "rclcpp/serialized_message.hpp"
#include "rclcpp/qos.hpp"
#include "rclcpp/executors/multi_threaded_executor.hpp"
#include "rosgraph_msgs/msg/clock.hpp"

using namespace std::chrono_literals;
namespace fs = std::filesystem;

struct RollingStats {
  explicit RollingStats(size_t cap = 256) : cap_(cap) {}
  void add(double x) {
    periods_.push_back(x);
    if (periods_.size() > cap_) periods_.pop_front();
  }
  size_t size() const { return periods_.size(); }
  std::optional<double> mean() const {
    if (periods_.empty()) return std::nullopt;
    double s = 0.0;
    for (double v : periods_) s += v;
    return s / static_cast<double>(periods_.size());
  }
  std::optional<double> stddev() const {
    if (periods_.size() < 2) return std::nullopt;
    double m = *mean();
    double s2 = 0.0;
    for (double v : periods_) { double d = v - m; s2 += d * d; }
    s2 /= static_cast<double>(periods_.size() - 1);
    return std::sqrt(s2);
  }
  std::optional<double> min() const {
    if (periods_.empty()) return std::nullopt;
    double m = periods_.front();
    for (double v : periods_) m = std::min(m, v);
    return m;
  }
  std::optional<double> max() const {
    if (periods_.empty()) return std::nullopt;
    double m = periods_.front();
    for (double v : periods_) m = std::max(m, v);
    return m;
  }
  std::optional<double> last() const {
    if (periods_.empty()) return std::nullopt;
    return periods_.back();
  }
  size_t cap_;
  std::deque<double> periods_;
};

struct TopicTracker {
  std::string topic;
  std::string type;
  rclcpp::QoS qos{rclcpp::KeepLast(10)};
  std::shared_ptr<rclcpp::GenericSubscription> sub;

  std::optional<std::chrono::steady_clock::time_point> first_tp;
  std::optional<std::chrono::steady_clock::time_point> last_tp;
  RollingStats periods;
  uint64_t count{0};

  explicit TopicTracker(std::string t, std::string ty, size_t window)
      : topic(std::move(t)), type(std::move(ty)), periods(window) {}

  void on_msg() {
    auto now = std::chrono::steady_clock::now();
    if (!first_tp) first_tp = now;
    if (last_tp) {
      auto dt = std::chrono::duration<double>(now - *last_tp).count();
      if (dt > 0.0 && dt < 10.0) periods.add(dt);
    }
    last_tp = now;
    ++count;
  }
};

class TopicStatsNode : public rclcpp::Node {
public:
  TopicStatsNode()
  : Node("topic_stats_node"),
    start_steady_(std::chrono::steady_clock::now())
  {
    declare_parameter<std::vector<std::string>>("topics", std::vector<std::string>{});
    declare_parameter<int>("print_period_ms", 1000);
    declare_parameter<int>("window_size", 256);
    declare_parameter<bool>("best_effort", false);

    // New: split-CSV output into a run folder
    declare_parameter<std::string>("csv_dir", std::string(""));   // parent directory for run folders
    declare_parameter<std::string>("run_tag", std::string("run")); // custom name for run-id

    // Legacy: single CSV file path (kept for compatibility)
    declare_parameter<std::string>("csv_path", std::string(""));

    auto topics = get_parameter("topics").as_string_array();
    const int print_ms = get_parameter("print_period_ms").as_int();
    const int window = get_parameter("window_size").as_int();
    const bool best_effort = get_parameter("best_effort").as_bool();

    const std::string csv_dir = get_parameter("csv_dir").as_string();
    const std::string run_tag = get_parameter("run_tag").as_string();
    const std::string csv_path = get_parameter("csv_path").as_string();

    // Decide output mode
    if (!csv_dir.empty()) {
      split_csv_ = init_run_folder(csv_dir, run_tag);
      if (!split_csv_) {
        RCLCPP_WARN(get_logger(), "Failed to init csv_dir. Falling back to csv_path if set.");
      }
    }

    // Fallback: legacy single CSV
    if (!split_csv_ && !csv_path.empty()) {
      csv_.open(csv_path, std::ios::out | std::ios::app);
      csv_enabled_ = csv_.good();
      if (!csv_enabled_) {
        RCLCPP_WARN(get_logger(), "Failed to open CSV path: %s", csv_path.c_str());
      }
    }

    rclcpp::QoS data_qos = rclcpp::QoS(rclcpp::KeepLast(10));
    if (best_effort) data_qos.best_effort().durability_volatile();
    else data_qos.reliable().durability_volatile();

    auto name_types = this->get_topic_names_and_types();
    for (const auto & tname : topics) {
      auto it = name_types.find(tname);
      if (it == name_types.end() || it->second.empty()) {
        RCLCPP_WARN(get_logger(), "Topic '%s' not found or has no type yet. Will retry later.",
                    tname.c_str());
        pending_topics_.push_back(tname);
        continue;
      }
      const std::string & type = it->second.front();
      add_subscription(tname, type, data_qos, window);
    }

    retry_timer_ = this->create_wall_timer(1000ms, [this, data_qos, window]() {
      if (pending_topics_.empty()) return;
      auto name_types = this->get_topic_names_and_types();
      std::vector<std::string> still_pending;
      for (const auto & tname : pending_topics_) {
        auto it = name_types.find(tname);
        if (it == name_types.end() || it->second.empty()) {
          still_pending.push_back(tname);
          continue;
        }
        add_subscription(tname, it->second.front(), data_qos, window);
      }
      pending_topics_.swap(still_pending);
    });

    clock_sub_ = this->create_subscription<rosgraph_msgs::msg::Clock>(
      "/clock", rclcpp::QoS(rclcpp::KeepLast(10)).best_effort(),
      [this](const rosgraph_msgs::msg::Clock::SharedPtr msg) { on_clock(msg->clock); });

    print_timer_ = this->create_wall_timer(std::chrono::milliseconds(print_ms),
      [this]() { print_stats(); });
  }

private:
  struct CsvFile {
    std::ofstream ofs;
    bool header_written{false};
  };

  static std::string normalize_topic_filename(const std::string &topic) {
    // Replace any non-alphanumeric with '_', collapse repeats, trim edges.
    std::string out;
    out.reserve(topic.size());
    char prev = '\0';
    for (char c : topic) {
      bool keep = std::isalnum(static_cast<unsigned char>(c));
      char a = keep ? c : '_';
      if (a == '_' && prev == '_') continue;
      out.push_back(keep ? a : '_');
      prev = out.back();
    }
    if (!out.empty() && out.front() == '_') out.erase(out.begin());
    if (!out.empty() && out.back()  == '_') out.pop_back();
    if (out.empty()) out = "topic";
    return out;
  }

  static std::string sanitize_run_tag(std::string s) {
    // Lowercase. Replace spaces and non [a-z0-9-] with '-'. Collapse repeats.
    std::string out;
    out.reserve(s.size());
    char prev = '\0';
    for (char c : s) {
      char d = std::tolower(static_cast<unsigned char>(c));
      bool ok = (d >= 'a' && d <= 'z') || (d >= '0' && d <= '9') || d=='-';
      char a = ok ? d : '-';
      if (a=='-' && prev=='-') continue;
      out.push_back(a);
      prev = a;
    }
    if (!out.empty() && out.front()=='-') out.erase(out.begin());
    if (!out.empty() && out.back()=='-') out.pop_back();
    if (out.empty()) out = "run";
    return out;
  }

  static std::string random_alnum_6() {
    static const char alphabet[] =
      "0123456789abcdefghijklmnopqrstuvwxyz";
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> dist(0, 35);
    std::string s(6, '0');
    for (int i = 0; i < 6; ++i) s[i] = alphabet[dist(gen)];
    return s;
  }

  static std::string today_yyyymmdd() {
    using clock = std::chrono::system_clock;
    auto now = clock::now();
    std::time_t t = clock::to_time_t(now);
    std::tm tm{};
#ifdef _WIN32
    localtime_s(&tm, &t);
#else
    localtime_r(&t, &tm);
#endif
    std::ostringstream os;
    os << std::put_time(&tm, "%Y%m%d");
    return os.str();
  }

  bool init_run_folder(const std::string &parent, const std::string &run_tag) {
    std::string tag = sanitize_run_tag(run_tag);
    run_id_ = today_yyyymmdd() + "-" + tag + "-" + random_alnum_6();
    run_dir_ = (fs::path(parent) / run_id_).string();
    std::error_code ec;
    if (!fs::create_directories(run_dir_, ec) && ec) {
      RCLCPP_WARN(get_logger(), "create_directories failed for %s: %s",
                  run_dir_.c_str(), ec.message().c_str());
      return false;
    }
    // Prepare rtf.csv
    rtf_csv_.ofs.open((fs::path(run_dir_) / "rtf.csv").string(),
                      std::ios::out | std::ios::app);
    if (!rtf_csv_.ofs.good()) {
      RCLCPP_WARN(get_logger(), "Failed to open %s/rtf.csv", run_dir_.c_str());
      return false;
    }
    return true;
  }

  CsvFile & ensure_topic_csv(const std::string &topic_name, const std::string &type) {
    std::string key = normalize_topic_filename(topic_name);
    auto it = topic_csvs_.find(key);
    if (it == topic_csvs_.end()) {
      CsvFile file;
      fs::path p = fs::path(run_dir_) / (key + ".csv");
      file.ofs.open(p.string(), std::ios::out | std::ios::app);
      if (!file.ofs.good()) {
        RCLCPP_WARN(get_logger(), "Failed to open topic csv: %s", p.string().c_str());
      } else {
        // header deferred to write_csv per file.header_written
      }
      it = topic_csvs_.emplace(key, std::move(file)).first;
    }
    // Write header once per file
    if (!it->second.header_written && it->second.ofs.good()) {
      it->second.ofs << "t_since_start,topic,type,count,init_delay_s,hz,jitter_s,last_dt_s,min_dt_s,max_dt_s\n";
      it->second.header_written = true;
      it->second.ofs.flush();
    }
    (void)type; // type is part of columns; nothing else to do here
    return it->second;
  }

  void add_subscription(const std::string & topic, const std::string & type,
                        const rclcpp::QoS & qos, int window) {
    if (trackers_.count(topic)) return;
    auto tracker = std::make_shared<TopicTracker>(topic, type, static_cast<size_t>(window));
    auto cb = [tracker](std::shared_ptr<rclcpp::SerializedMessage>) {
      tracker->on_msg();
    };
    tracker->sub = this->create_generic_subscription(
      topic, type, qos,
      [cb](std::shared_ptr<rclcpp::SerializedMessage> m) { cb(m); });
    trackers_[topic] = tracker;
    RCLCPP_INFO(this->get_logger(), "Subscribed: %s [%s]", topic.c_str(), type.c_str());
  }

  void on_clock(const builtin_interfaces::msg::Time & sim) {
    auto now = std::chrono::steady_clock::now();
    const double wall_now = std::chrono::duration<double>(now - start_steady_).count();
    const double sim_now = sim.sec + sim.nanosec * 1e-9;

    if (!rtf_wall_prev_) {
      rtf_wall_prev_ = wall_now;
      rtf_sim_prev_  = sim_now;
      return;
    }
    const double d_wall = wall_now - *rtf_wall_prev_;
    const double d_sim  = sim_now - *rtf_sim_prev_;
    if (d_wall > 0.0 && d_wall < 10.0 && d_sim >= 0.0) {
      rtf_wall_sum_ += d_wall;
      rtf_sim_sum_  += d_sim;
    }
    rtf_wall_prev_ = wall_now;
    rtf_sim_prev_  = sim_now;
  }

  static std::string fmt_opt(const std::optional<double> & v, int prec = 3) {
    if (!v) return "n/a";
    std::ostringstream os; os.setf(std::ios::fixed); os << std::setprecision(prec) << *v; return os.str();
  }

  static std::string fmt_seconds(double s) {
    std::ostringstream os; os.setf(std::ios::fixed);
    if (s < 1.0) { os << std::setprecision(3) << s << "s"; return os.str(); }
    if (s < 120.0) { os << std::setprecision(2) << s << "s"; return os.str(); }
    int sec = static_cast<int>(s + 0.5);
    int m = sec / 60, r = sec % 60;
    os << m << "m" << r << "s";
    return os.str();
  }

  void write_csv(double rtf) {
    const double t0 = std::chrono::duration<double>(std::chrono::steady_clock::now() - start_steady_).count();

    if (split_csv_) {
      // rtf.csv
      if (!rtf_header_written_) {
        rtf_csv_.ofs << "t_since_start,rtf\n";
        rtf_header_written_ = true;
      }
      rtf_csv_.ofs << std::setprecision(6) << std::fixed
                   << t0 << "," << (std::isfinite(rtf) ? rtf : NAN) << "\n";
      rtf_csv_.ofs.flush();

      // per-topic CSVs
      for (const auto & kv : trackers_) {
        const auto & tr = *kv.second;
        double init_delay_s = NAN;
        if (tr.first_tp) init_delay_s = std::chrono::duration<double>(*tr.first_tp - start_steady_).count();

        auto mean_p = tr.periods.mean();
        double hz = mean_p ? 1.0 / *mean_p : NAN;
        double jitter = tr.periods.stddev().value_or(NAN);
        double last_dt = tr.periods.last().value_or(NAN);
        double min_dt = tr.periods.min().value_or(NAN);
        double max_dt = tr.periods.max().value_or(NAN);

        CsvFile & f = ensure_topic_csv(tr.topic, tr.type);
        if (f.ofs.good()) {
          f.ofs << std::setprecision(6) << std::fixed
                << t0 << ","
                << tr.topic << ","
                << tr.type << ","
                << tr.count << ","
                << init_delay_s << ","
                << hz << ","
                << jitter << ","
                << last_dt << ","
                << min_dt << ","
                << max_dt << "\n";
          f.ofs.flush();
        }
      }
      return;
    }

    // Legacy single CSV
    if (!csv_enabled_) return;
    if (!csv_header_written_) {
      csv_ << "t_since_start,kind,topic,type,count,init_delay_s,hz,jitter_s,last_dt_s,min_dt_s,max_dt_s,rtf\n";
      csv_header_written_ = true;
    }

    csv_ << std::setprecision(6) << std::fixed
         << t0 << ",rtf,,,,,,,,,," << (std::isfinite(rtf) ? rtf : NAN) << "\n";

    for (const auto & kv : trackers_) {
      const auto & tr = *kv.second;
      double init_delay_s = NAN;
      if (tr.first_tp) init_delay_s = std::chrono::duration<double>(*tr.first_tp - start_steady_).count();

      auto mean_p = tr.periods.mean();
      double hz = mean_p ? 1.0 / *mean_p : NAN;
      double jitter = tr.periods.stddev().value_or(NAN);
      double last_dt = tr.periods.last().value_or(NAN);
      double min_dt = tr.periods.min().value_or(NAN);
      double max_dt = tr.periods.max().value_or(NAN);

      csv_ << t0 << ",topic,"
           << tr.topic << "," << tr.type << ","
           << tr.count << ","
           << init_delay_s << ","
           << hz << ","
           << jitter << ","
           << last_dt << ","
           << min_dt << ","
           << max_dt << ","
           << "\n";
    }
    csv_.flush();
  }

  void print_stats() {
    std::ostringstream os;
    os.setf(std::ios::fixed);
    os << "\n--- topic_stats ---\n";

    double rtf = (rtf_wall_sum_ > 0.0) ? (rtf_sim_sum_ / rtf_wall_sum_) : std::nan("");
    if (std::isnan(rtf))
      os << "RTF: n/a  [/clock not active]\n";
    else
      os << "RTF: " << std::setprecision(3) << rtf << "  [/clock]\n";

    for (const auto & kv : trackers_) {
      const auto & tr = *kv.second;
      const double since_start = std::chrono::duration<double>(
        (tr.first_tp ? *tr.first_tp : std::chrono::steady_clock::now()) - start_steady_).count();
      const std::string init_delay = tr.first_tp ? fmt_seconds(since_start) : "n/a";

      std::optional<double> mean_p = tr.periods.mean();
      std::optional<double> hz     = mean_p ? std::optional<double>(1.0 / *mean_p) : std::nullopt;

      os << tr.topic << " [" << tr.type << "]\n"
         << "  count=" << tr.count
         << "  init_delay=" << init_delay
         << "  hz=" << fmt_opt(hz, 2)
         << "  jitter(std s)=" << fmt_opt(tr.periods.stddev(), 4)
         << "  last_dt=" << fmt_opt(tr.periods.last(), 4)
         << "  min_dt=" << fmt_opt(tr.periods.min(), 4)
         << "  max_dt=" << fmt_opt(tr.periods.max(), 4)
         << "\n";
    }

    if (!pending_topics_.empty()) {
      os << "pending_topics: ";
      for (size_t i = 0; i < pending_topics_.size(); ++i) {
        if (i) os << ", ";
        os << pending_topics_[i];
      }
      os << "\n";
    }

    if (split_csv_) {
      os << "run_dir: " << run_dir_ << "\n";
    }

    std::cout << os.str() << std::flush;
    write_csv(rtf);
  }

  std::map<std::string, std::shared_ptr<TopicTracker>> trackers_;
  std::vector<std::string> pending_topics_;
  rclcpp::TimerBase::SharedPtr print_timer_;
  rclcpp::TimerBase::SharedPtr retry_timer_;
  rclcpp::Subscription<rosgraph_msgs::msg::Clock>::SharedPtr clock_sub_;
  std::chrono::steady_clock::time_point start_steady_;

  std::optional<double> rtf_wall_prev_;
  std::optional<double> rtf_sim_prev_;
  double rtf_wall_sum_{0.0};
  double rtf_sim_sum_{0.0};

  // Split-CSV mode
  bool split_csv_{false};
  std::string run_id_;
  std::string run_dir_;
  CsvFile rtf_csv_;
  bool rtf_header_written_{false};
  std::map<std::string, CsvFile> topic_csvs_;

  // Legacy single CSV
  std::ofstream csv_;
  bool csv_enabled_{false};
  bool csv_header_written_{false};
};

int main(int argc, char ** argv) {
  rclcpp::init(argc, argv);
  rclcpp::executors::MultiThreadedExecutor exec;
  auto node = std::make_shared<TopicStatsNode>();
  exec.add_node(node);
  exec.spin();
  rclcpp::shutdown();
  return 0;
}
