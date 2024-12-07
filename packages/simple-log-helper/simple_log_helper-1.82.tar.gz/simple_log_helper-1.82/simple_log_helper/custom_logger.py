import logging
import time
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Union
from logging.handlers import RotatingFileHandler


class CustomLogger(logging.Logger):
    """
    A custom logger class that extends the standard logging.Logger with additional features.
    """

    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] "%(name)s" (%(filename)s:) %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    def __init__(
        self, 
        name: str, 
        log_filename: Optional[str] = None, 
        level: Union[int, str] = logging.INFO,
        max_log_size_mb: int = 10,
        backup_count: int = 5,
        custom_formatter: Optional[logging.Formatter] = None
    ):
        """
        Initialize an enhanced logger with configurable parameters.

        Args:
            name (str): Logger name
            log_filename (str, optional): Log file path
            level (int/str): Logging level
            max_log_size_mb (int): Maximum log file size in megabytes
            backup_count (int): Number of backup log files to keep
            custom_formatter (Formatter, optional): Custom log formatter
        """
        super().__init__(name,level=level)
        self.propagate = False
        self.log_filename = log_filename
        self.max_log_size_mb = max_log_size_mb
        self.backup_count = backup_count
        self._initialize_logger(custom_formatter)

    def _initialize_logger(self, custom_formatter: Optional[logging.Formatter] = None) -> None:
        """
        Set up logger with file and console handlers using advanced configuration.
        """
        try:
            # Clear any existing handlers
            if self.handlers:
                for handler in self.handlers[:]:
                    self.removeHandler(handler)

            formatter = custom_formatter or self.DEFAULT_FORMATTER

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.addHandler(console_handler)

            # File handler with rotation
            if self.log_filename:
                log_path = Path(self.log_filename)
                log_path.parent.mkdir(parents=True, exist_ok=True)

                file_handler = RotatingFileHandler(
                    log_path, 
                    maxBytes=self.max_log_size_mb * 1024 * 1024,
                    backupCount=self.backup_count
                )
                file_handler.setFormatter(formatter)
                self.addHandler(file_handler)

            # Set logging level
            self.setLevel(self._resolve_log_level(self.level))

        except Exception as e:
            print(f"Logger initialization failed: {e}")
            raise

    def setLevel(self, level: Any) -> None:
        """
        Set the logging level.

        Args:
            level (Any): The logging level as an integer or string.
        """
        if isinstance(level, str):
            level = self._resolve_log_level(level)
        super().setLevel(level)

    def getChild(self, suffix):
        sub_logger = super().getChild(suffix)
        sub_logger.propagate = False
        sub_logger.handlers.clear()  
        for handler in self.handlers:
            sub_logger.addHandler(handler)
        return sub_logger
    
    @staticmethod
    def _resolve_log_level(level: str) -> int:
        """
        Resolves a string log level to the corresponding numeric value.
        
        Args:
            level (str): Log level as a string.
        
        Returns:
            int: Corresponding logging level.
        
        Raises:
            ValueError: If the provided level is invalid.
        """
        level = level.upper()
        try:
            return getattr(logging, level)
        except AttributeError:
            raise ValueError(f"Invalid log level: {level}")

    def show_progress(self, progress: float, bar_length: int = 50) -> None:
        """
        Display a progress bar in the logs.

        Args:
            progress (float): Progress percentage between 0 and 100.
            bar_length (int): The length of the progress bar.
        """
        progress = int(progress)
        filled_length = int(round(bar_length * progress / 100))
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        self.info(f"Processing: [{bar}] {progress}%")

    def time_execution(self, func: Callable) -> Callable:
        """
        Decorator to log function execution time and details.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            try:
                self.info(f"Executing: {func.__name__}")
                result = func(*args, **kwargs)
                exec_time = time.perf_counter() - start_time
                self.info(f"Function {func.__name__} completed in {exec_time:.4f} seconds")
                return result
            except Exception as e:
                self.error(f"Error in {func.__name__}: {e}", exc_info=True)
                raise
        return wrapper
