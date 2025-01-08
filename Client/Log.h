#ifndef LOG_H
#define LOG_H

#include <string>
#include <fstream>
#include <mutex>

// .cpp include
#include <iostream>
#include <iomanip>
#include <ctime>
#include <sstream>
#include <map>

enum class LogLevel {
    DEBUG = 10,
    INFO = 20,
    WARNING = 30,
    ERROR = 40
};

class Log {
public:
    Log(const std::string& logger_name = "default",
        const std::string& filename = "",
        bool log_to_file = false,
        bool log_to_console = true);

    ~Log();

    void debug(const std::string& message, const char* file = __builtin_FILE(), int line = __builtin_LINE());
    void info(const std::string& message, const char* file = __builtin_FILE(), int line = __builtin_LINE());
    void warning(const std::string& message, const char* file = __builtin_FILE(), int line = __builtin_LINE());
    void error(const std::string& message, const char* file = __builtin_FILE(), int line = __builtin_LINE());

private:
    std::string _logger_name;
    bool _log_to_file;
    bool _log_to_console;
    std::ofstream _log_file;
    std::mutex _mutex;

    void cleanup();
    void log_message(LogLevel level, const std::string& message, const char* file, int line);
    void log_to_console(const std::string& message, LogLevel level);
    void log_to_file(const std::string& message, LogLevel level);

    std::string get_timestamp();
    std::string log_level_to_string(LogLevel level, int width = 7);
    std::string get_caller_details(const char* file, int line);
};

#endif // LOG_H
