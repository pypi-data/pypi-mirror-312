import logging
import os
from datetime import datetime

class ColoredFormatter(logging.Formatter):
    """Custom formatter to add colors to log messages based on log level."""
    COLORS = {
        'DEBUG': '\033[94m',    # Blue
        'INFO': '\033[92m',     # Green
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',    # Red
        'CRITICAL': '\033[95m'  # Magenta
    }
    RESET = '\033[0m'  # Reset color

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        log_message = super().format(record)
        return f"{log_color}{log_message}{self.RESET}"


class Logger:
    def __init__(self, log_dir='./logs'):
        os.makedirs(log_dir, exist_ok=True)

        # Create a log file with the current date in the log directory
        log_file = os.path.join(log_dir, "python.log")

        # Set up the logger
        self.logger = logging.getLogger('Appcomm_python_Logger')
        self.logger.setLevel(logging.DEBUG)

        # File handler for logging to a file (without colors)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '[%(asctime)s] - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)

        # Console handler for logging to the terminal (with colors)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = ColoredFormatter(
            '[%(asctime)s] - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message, exc=None):
        if exc:
            self.logger.error(message, exc_info=exc)
        else:
            self.logger.error(message)

    def critical(self, message, exc=None):
        if exc:
            self.logger.critical(message, exc_info=exc)
        else:
            self.logger.critical(message)