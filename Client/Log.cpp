#include "Log.h"


Log::Log(const std::string& logger_name, const std::string& filename, bool log_to_file, bool log_to_console)
    : _logger_name(logger_name),
    _log_to_file(log_to_file),
    _log_to_console(log_to_console) {
    if (_log_to_file && !filename.empty()) {
        _log_file.open(filename, std::ios::app);
        if (!_log_file.is_open()) {
            std::cerr << "Failed to open log file: " << filename << std::endl;
            _log_to_file = false;
        }
    }
}

Log::~Log() {
    cleanup();
}

void Log::debug(const std::string& message, const char* file, int line) {
    log_message(LogLevel::DEBUG, message, file, line);
}

void Log::info(const std::string& message, const char* file, int line) {
    log_message(LogLevel::INFO, message, file, line);
}

void Log::warning(const std::string& message, const char* file, int line) {
    log_message(LogLevel::WARNING, message, file, line);
}

void Log::error(const std::string& message, const char* file, int line) {
    log_message(LogLevel::ERROR, message, file, line);
}

void Log::cleanup() {
    if (_log_file.is_open()) {
        _log_file.close();
    }
}

void Log::log_message(LogLevel level, const std::string& message, const char* file, int line) {
    std::lock_guard<std::mutex> lock(_mutex);

    std::string timestamp = get_timestamp();
    std::string level_str = log_level_to_string(level);
    std::string file_details = get_caller_details(file, line);

    std::ostringstream log_entry;
    log_entry << "[" << timestamp << "] [" << std::setw(7) << level_str << "] "
        << file_details << " " << message << " (" << _logger_name << ")";

    if (_log_to_console) {
        log_to_console(log_entry.str(), level);
    }

    if (_log_to_file && _log_file.is_open()) {
        log_to_file(log_entry.str(), level);
    }
    
}

void Log::log_to_console(const std::string& message, LogLevel level) {
    static const std::map<LogLevel, std::string> COLORS = {
        {LogLevel::DEBUG, "\033[37m"},
        {LogLevel::INFO, "\033[34m"},
        {LogLevel::WARNING, "\033[33m"},
        {LogLevel::ERROR, "\033[31m"}
    };

    std::string reset_color = "\033[0m";

    std::string color = COLORS.at(level);
    std::cout << color << message << reset_color << std::endl;
}

void Log::log_to_file(const std::string& message, LogLevel level) {
    if (level != LogLevel::DEBUG) {
        _log_file << message << std::endl;
    }
}

std::string Log::get_timestamp() {
    auto now = std::time(nullptr);
    std::tm local_time;
    // Use std::localtime_s for thread-safe conversion to local time
    if (::localtime_s(&local_time, &now) == 0) {
        std::ostringstream oss;
        oss << std::put_time(&local_time, "%Y-%m-%d %H:%M:%S");
        return oss.str();
    }
    // If std::localtime_s fails, return an empty timestamp
    return {};
}

std::string Log::log_level_to_string(LogLevel level, int width) {
    std::string level_str;
    switch (level) {
    case LogLevel::DEBUG: level_str = "DEBUG"; break;
    case LogLevel::INFO: level_str = "INFO"; break;
    case LogLevel::WARNING: level_str = "WARNING"; break;
    case LogLevel::ERROR: level_str = "ERROR"; break;
    default: level_str = "UNKNOWN"; break;
    }

    // Center-align the level_str within 7 characters
    //int total_width = 7;
    int padding = width - level_str.size();
    int left_padding = padding / 2;
    int right_padding = padding - left_padding;
    std::string centered_level_str = std::string(left_padding, ' ') + level_str + std::string(right_padding, ' ');

    return centered_level_str;
}

std::string Log::get_caller_details(const char* file, int line) {
    std::ostringstream oss;

    // Extract only the file name from the full path
    std::string file_name = file;
    size_t pos = file_name.find_last_of("/\\"); // Handle both '/' and '\\' path separators
    if (pos != std::string::npos) {
        file_name = file_name.substr(pos + 1);
    }

    oss << "[" << file_name << ":" << line << "]";
    return oss.str();
}
