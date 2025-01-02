import os
import sys
from datetime import datetime
from enum import Enum
import inspect
import threading


class LogLevel(Enum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40

    @staticmethod
    def to_string(level):
        if level == LogLevel.DEBUG:
            return " DEBUG "
        elif level == LogLevel.INFO:
            return " INFO  "
        elif level == LogLevel.WARNING:
            return "WARNING"
        elif level == LogLevel.ERROR:
            return " ERROR "
        else:
            return "UNKNOWN"


class Log:
    _log_file = None
    _to_file = False
    _to_console = True
    _logger_name = "default"

    def __init__(self, logger_name="default", filename="", log_to_file=False, log_to_console=True):
        self._to_file = log_to_file
        self._to_console = log_to_console
        self._logger_name = logger_name
        self._initialize_log_file(filename)
        self._lock = threading.Lock()

    def _initialize_log_file(self, filename):
        if self._to_file and filename:
            try:
                self._log_file = open(filename, "a")
            except Exception as e:
                print(f"Failed to open log file: {filename}: {str(e)}", file=sys.stderr)
                Log._to_file = False

    def cleanup(self):
        if self._log_file:
            self._log_file.close()
            self._log_file = None

    def _log_message(self, level, message, file_details=None):
        with self._lock:
            timestamp = Log._get_timestamp()
            level_str = LogLevel.to_string(level)

            if not file_details:
                filename,line = self._get_caller_details()
            else:
                filename, line = file_details

            log_entry = f"[{timestamp}] [{level_str}] [{filename}:{line}]\t{message} ({self._logger_name})"

            if self._to_console:
                self._log_to_console(log_entry, level)

            if self._to_file and Log._log_file:
                self._log_to_file(log_entry, level)

    def _log_to_file(self, message, level):
        if not (level == LogLevel.DEBUG):
            self._log_file.write(f"{message}\n")

    def debug(self, message):
        """Logs a debug-level message."""
        file_details = self._get_caller_details()
        self._log_message(level=LogLevel.DEBUG, message=message, file_details=file_details)

    def info(self, message):
        """Logs an info-level message."""
        file_details = self._get_caller_details()
        self._log_message(level=LogLevel.INFO, message=message, file_details=file_details)

    def warning(self, message):
        """Logs a warning-level message."""
        file_details = self._get_caller_details()
        self._log_message(level=LogLevel.WARNING, message=message, file_details=file_details)

    def error(self, message):
        """Logs an error-level message."""
        file_details = self._get_caller_details()
        self._log_message(level=LogLevel.ERROR, message=message, file_details=file_details)

    @staticmethod
    def _log_to_console(message, level):
        reset_color = "\033[0m"
        COLORS = {
            LogLevel.DEBUG: "\033[37m",  # White (for DEBUG)
            LogLevel.INFO: "\033[34m",  # Blue (for INFO)
            LogLevel.WARNING: "\033[33m",  # Yellow (for WARN)
            LogLevel.ERROR: "\033[31m",  # Red (for ERROR)
        }

        color = COLORS.get(level, reset_color)  # Default to no color (reset)
        print(f"{color}{message}{reset_color}")

    @staticmethod
    def _get_timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _get_caller_details():
        """
        Retrieves the filename and line number of the caller.

        Returns:
            tuple: A tuple containing the filename and line number.
        """
        frame = inspect.currentframe().f_back.f_back
        filename = os.path.basename(frame.f_code.co_filename)
        line = frame.f_lineno
        return filename, line


# Example usage
if __name__ == "__main__":
    logger = Log(filename="logfile.txt", log_to_file=True, log_to_console=True)
    # Log.initialize(filename="logfile.txt", log_to_file=True, log_to_console=True)
    # logger._log_message(LogLevel.INFO, "This is an informational message.")
    # logger._log_message(LogLevel.WARNING, "This is a warning message.")
    # logger.log_message(LogLevel.ERROR, "This is an error message.")
    # logger.log_message(LogLevel.DEBUG, "This is a debug message.")

    logger.debug("This is debug function")
    logger.info("this is info")
    logger.warning("this is warning")
    logger.error("this is error")
    logger.cleanup()
