import os
import sys
from datetime import datetime
from enum import Enum
import inspect
import threading


# Enum to represent different log levels with corresponding numeric values.
class LogLevel(Enum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40

    @staticmethod
    def to_string(level):
        """
        Convert a LogLevel to its string representation.

        Args:
            level (LogLevel): The log level to convert.

        Returns:
            str: The string representation of the log level.
        """
        if level == LogLevel.DEBUG:
            return "DEBUG"
        elif level == LogLevel.INFO:
            return "INFO"
        elif level == LogLevel.WARNING:
            return "WARNING"
        elif level == LogLevel.ERROR:
            return "ERROR"
        else:
            return "UNKNOWN"


# Log class to manage logging messages to both console and file.
class Log:
    _log_file = None
    _to_file = False
    _to_console = True
    _logger_name = "default"

    def __init__(self, logger_name="default", filename="", log_to_file=False, log_to_console=True):
        """
        Initializes the Log object with optional file and console logging.

        Args:
            logger_name (str): The name of the logger.
            filename (str): The log file path.
            log_to_file (bool): Whether to log to a file.
            log_to_console (bool): Whether to log to console.
        """
        self._to_file = log_to_file
        self._to_console = log_to_console
        self._logger_name = logger_name
        self._initialize_log_file(filename)
        self._lock = threading.Lock()

    def _initialize_log_file(self, filename):
        """
        Initializes the log file for logging if log_to_file is enabled.

        Args:
            filename (str): The log file path.
        """
        if self._to_file and filename:
            try:
                self._log_file = open(filename, "a")  # Open file in append mode
            except Exception as e:
                print(f"Failed to open log file: {filename}: {str(e)}", file=sys.stderr)
                Log._to_file = False

    def cleanup(self):
        """
        Cleans up the log file by closing it.
        """
        if self._log_file:
            self._log_file.close()
            self._log_file = None

    def _log_message(self, level, message, file_details=None):
        """
        Logs a message at a specified level with optional file details.

        Args:
            level (LogLevel): The log level.
            message (str): The message to log.
            file_details (tuple, optional): A tuple with filename and line number.
        """
        with self._lock:
            timestamp = Log._get_timestamp()
            level_str = LogLevel.to_string(level)

            # Get caller details (filename and line) if not provided
            if not file_details:
                filename, line = self._get_caller_details()
            else:
                filename, line = file_details

            log_entry = self._format_log_entry(timestamp, level_str, filename, line, message, self._logger_name)

            if self._to_console:
                self._log_to_console(log_entry, level)

            if self._to_file and Log._log_file:
                self._log_to_file(log_entry, level)

    def _log_to_file(self, message, level):
        """
        Logs a message to the file if the level is not DEBUG.

        Args:
            message (str): The log message.
            level (LogLevel): The log level.
        """
        if not (level == LogLevel.DEBUG):  # Don't log DEBUG level messages to the file
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
        """
        Logs a message to the console with color-coded output based on the level.

        Args:
            message (str): The log message.
            level (LogLevel): The log level.
        """
        reset_color = "\033[0m"
        COLORS = {
            LogLevel.DEBUG: "\033[37m",  # White for DEBUG
            LogLevel.INFO: "\033[34m",  # Blue for INFO
            LogLevel.WARNING: "\033[33m",  # Yellow for WARNING
            LogLevel.ERROR: "\033[31m",  # Red for ERROR
        }

        color = COLORS.get(level, reset_color)  # Default to no color (reset)
        print(f"{color}{message}{reset_color}")

    @staticmethod
    def _format_log_entry(timestamp, level_str, filename, line, message, logger_name):
        """
        Formats a log entry into a structured string.

        Args:
            timestamp (str): The timestamp of the log.
            level_str (str): The string representation of the log level.
            filename (str): The filename where the log was called.
            line (int): The line number where the log was called.
            message (str): The log message.
            logger_name (str): The name of the logger.

        Returns:
            str: The formatted log entry.
        """
        timestamp_width = 19
        level_width = 7

        # Format each component of the log entry
        timestamp = timestamp[:timestamp_width]
        if len(level_str) % 2 == 0:
            level_str = level_str.center(level_width - 1) + " "
        else:
            level_str = level_str.center(level_width)

        fixed_part_length = len(f"[{timestamp}] [{level_str}] [{filename}:{line}]")
        max_fixed_part_length = 54
        padding = " " * max(0, max_fixed_part_length - fixed_part_length)

        # Construct the full log entry string
        log_entry = (
            f"[{timestamp}] [{level_str}] [{filename}:{line}]{padding}{message} ({logger_name})"
        )

        return log_entry

    @staticmethod
    def _get_timestamp():
        """
        Gets the current timestamp in the format YYYY-MM-DD HH:MM:SS.

        Returns:
            str: The current timestamp.
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _get_caller_details():
        """
        Retrieves the filename and line number of the caller.

        Returns:
            tuple: A tuple containing the filename and line number.
        """
        frame = inspect.currentframe().f_back.f_back  # Get caller's frame
        filename = os.path.basename(frame.f_code.co_filename)  # Get the file name
        line = frame.f_lineno  # Get the line number
        return filename, line


# Example usage of the Log class
if __name__ == "__main__":
    logger = Log(filename="logfile.txt", log_to_file=True, log_to_console=True)

    # Logging messages at different levels
    logger.debug("This is debug function")
    logger.info("This is info")
    logger.warning("This is warning")
    logger.error("This is error")

    # Cleanup resources (close log file)
    logger.cleanup()

# import os
# import sys
# from datetime import datetime
# from enum import Enum
# import inspect
# import threading
#
#
# class LogLevel(Enum):
#     DEBUG = 10
#     INFO = 20
#     WARNING = 30
#     ERROR = 40
#
#     @staticmethod
#     def to_string(level):
#         if level == LogLevel.DEBUG:
#             return "DEBUG"
#         elif level == LogLevel.INFO:
#             return "INFO"
#         elif level == LogLevel.WARNING:
#             return "WARNING"
#         elif level == LogLevel.ERROR:
#             return "ERROR"
#         else:
#             return "UNKNOWN"
#
#
# class Log:
#     _log_file = None
#     _to_file = False
#     _to_console = True
#     _logger_name = "default"
#
#     def __init__(self, logger_name="default", filename="", log_to_file=False, log_to_console=True):
#         self._to_file = log_to_file
#         self._to_console = log_to_console
#         self._logger_name = logger_name
#         self._initialize_log_file(filename)
#         self._lock = threading.Lock()
#
#     def _initialize_log_file(self, filename):
#         if self._to_file and filename:
#             try:
#                 self._log_file = open(filename, "a")
#             except Exception as e:
#                 print(f"Failed to open log file: {filename}: {str(e)}", file=sys.stderr)
#                 Log._to_file = False
#
#     def cleanup(self):
#         if self._log_file:
#             self._log_file.close()
#             self._log_file = None
#
#     @staticmethod
#     def _format_log_entry(timestamp, level_str, filename, line, message, logger_name):
#         # Define fixed widths for components
#         timestamp_width = 19
#         level_width = 7
#
#         # Format each component
#         timestamp = timestamp[:timestamp_width]
#         if len(level_str) % 2 == 0:
#             level_str = level_str.center(level_width - 1)+" "
#         else:
#             level_str = level_str.center(level_width)
#
#         # Calculate the padding length
#         fixed_part_length = len(f"[{timestamp}] [{level_str}] [{filename}:{line}]")
#         max_fixed_part_length = 54
#         padding = " " * max(0, max_fixed_part_length - fixed_part_length)
#
#         # Construct the log entry
#         log_entry = (
#             f"[{timestamp}] [{level_str}] [{filename}:{line}]{padding}{message} ({logger_name})"
#         )
#
#         return log_entry
#
#     def _log_message(self, level, message, file_details=None):
#         with self._lock:
#             timestamp = Log._get_timestamp()
#             level_str = LogLevel.to_string(level)
#
#             if not file_details:
#                 filename, line = self._get_caller_details()
#             else:
#                 filename, line = file_details
#
#
#             log_entry = self._format_log_entry(timestamp, level_str, filename, line, message, self._logger_name)
#
#             if self._to_console:
#                 self._log_to_console(log_entry, level)
#
#             if self._to_file and Log._log_file:
#                 self._log_to_file(log_entry, level)
#
#     def _log_to_file(self, message, level):
#         if not (level == LogLevel.DEBUG):
#             self._log_file.write(f"{message}\n")
#
#     def debug(self, message):
#         """Logs a debug-level message."""
#         file_details = self._get_caller_details()
#         self._log_message(level=LogLevel.DEBUG, message=message, file_details=file_details)
#
#     def info(self, message):
#         """Logs an info-level message."""
#         file_details = self._get_caller_details()
#         self._log_message(level=LogLevel.INFO, message=message, file_details=file_details)
#
#     def warning(self, message):
#         """Logs a warning-level message."""
#         file_details = self._get_caller_details()
#         self._log_message(level=LogLevel.WARNING, message=message, file_details=file_details)
#
#     def error(self, message):
#         """Logs an error-level message."""
#         file_details = self._get_caller_details()
#         self._log_message(level=LogLevel.ERROR, message=message, file_details=file_details)
#
#     @staticmethod
#     def _log_to_console(message, level):
#         reset_color = "\033[0m"
#         COLORS = {
#             LogLevel.DEBUG: "\033[37m",  # White (for DEBUG)
#             LogLevel.INFO: "\033[34m",  # Blue (for INFO)
#             LogLevel.WARNING: "\033[33m",  # Yellow (for WARN)
#             LogLevel.ERROR: "\033[31m",  # Red (for ERROR)
#         }
#
#         color = COLORS.get(level, reset_color)  # Default to no color (reset)
#         print(f"{color}{message}{reset_color}")
#
#     @staticmethod
#     def _get_timestamp():
#         return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#
#     @staticmethod
#     def _get_caller_details():
#         """
#         Retrieves the filename and line number of the caller.
#
#         Returns:
#             tuple: A tuple containing the filename and line number.
#         """
#         frame = inspect.currentframe().f_back.f_back
#         filename = os.path.basename(frame.f_code.co_filename)
#         line = frame.f_lineno
#         return filename, line
#
#
# # Example usage
# if __name__ == "__main__":
#     logger = Log(filename="logfile.txt", log_to_file=True, log_to_console=True)
#     # Log.initialize(filename="logfile.txt", log_to_file=True, log_to_console=True)
#     # logger._log_message(LogLevel.INFO, "This is an informational message.")
#     # logger._log_message(LogLevel.WARNING, "This is a warning message.")
#     # logger.log_message(LogLevel.ERROR, "This is an error message.")
#     # logger.log_message(LogLevel.DEBUG, "This is a debug message.")
#
#     logger.debug("This is debug function")
#     logger.info("this is info")
#     logger.warning("this is warning")
#     logger.error("this is error")
#     logger.cleanup()
