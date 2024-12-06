import logging
import datetime
import os
from tian_core import singleton
import sentry_sdk

@singleton
class GLog(logging.Formatter):
    """Custom logging formatter with color-coded log levels."""

    COLOR_MAP = {
        logging.DEBUG: '\x1b[38;5;46m',   # Green
        logging.INFO: '\x1b[38;5;39m',    # Blue
        logging.WARNING: '\x1b[38;5;226m', # Yellow
        logging.ERROR: '\x1b[38;5;196m',   # Red
        logging.CRITICAL: '\x1b[36m'      # Bold Red
    }
    RESET = '\x1b[0m'
    BASE_FORMAT = "[%(levelname)s][%(asctime)s] %(module)s.%(funcName)s():Line %(lineno)d: - %(message)s"

    def format(self, record):
        log_fmt = self.COLOR_MAP.get(record.levelno, '') + self.BASE_FORMAT + self.RESET
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

    def formatTime(self, record, datefmt=None):
        return datetime.datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')


@singleton
class LogManager:
    """Manages logging configuration and setup."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        self.logger.setLevel(log_level)

        # Configure console logging
        self._configure_console_logging(log_level)
        
        # Configure file logging if enabled
        if self._is_logging_enabled():
            self._configure_file_logging()
        
        # Configure Sentry if enabled
        if self._is_sentry_enabled():
            self._configure_sentry()

    def _configure_console_logging(self, log_level):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(GLog())
        self.logger.addHandler(console_handler)

    def _configure_file_logging(self):
        log_file = os.getenv("LOG_FILE", "tian.log") + f"_{datetime.date.today():%Y_%m_%d}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(GLog())
        self.logger.addHandler(file_handler)

    def _configure_sentry(self):
        sentry_sdk.init(
            dsn=os.getenv("SENTRY_LOG"),
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0
        )

    def _is_logging_enabled(self):
        return os.getenv("LOG_ENABLED", "False").lower() == "true"

    def _is_sentry_enabled(self):
        return os.getenv("SENTRY_ENABLED", "True").lower() == "true"

    def get_logger(self):
        return self.logger

# Initialize the logger
logger = LogManager().get_logger()
