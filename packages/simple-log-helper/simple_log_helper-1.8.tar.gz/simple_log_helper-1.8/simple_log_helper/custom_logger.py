import logging
import time
from functools import wraps
from pathlib import Path
from typing import Any, Callable


class CustomLogger(logging.Logger):
    """
    A custom logger class that extends the standard logging.Logger with additional features.
    """

    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] "%(name)s" (%(filename)s:) %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    def __init__(self, name: str, log_filename: str = "./Logs/default.log", level: int = logging.INFO):
        """
        Initialize a CustomLogger instance.

        Args:
            name (str): The name of the logger.
            log_filename (str): The file path for logging output.
            level (int): The logging level.
        """
        super().__init__(name, level)
        self.log_filename = log_filename
        self._initialize_logger()

    def _initialize_logger(self) -> None:
        """
        Initialize the logger by setting up file and console handlers.
        """
        if not self.handlers:  # Prevent adding duplicate handlers
            try:
                log_path = Path(self.log_filename)
                log_path.parent.mkdir(parents=True, exist_ok=True)

                # Ensure the log file has a .log extension
                if log_path.suffix != '.log':
                    log_path = log_path.with_suffix('.log')
                    self.log_filename = str(log_path)

                # File handler
                file_handler = logging.FileHandler(self.log_filename, mode='a')
                file_handler.setFormatter(self.formatter)
                self.addHandler(file_handler)

                # Console handler
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(self.formatter)
                self.addHandler(console_handler)
            except OSError as e:
                self.error(f"Failed to initialize logger: {e}")
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

    def log_function_call(self, func: Callable) -> Callable:
        """
        Decorator to log function calls and execution time.

        Args:
            func (Callable): The function to be decorated.

        Returns:
            Callable: The wrapped function.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.info(f"Calling function: {func.__name__} with args: {args}, kwargs: {kwargs}")
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            self.info(f"Function '{func.__name__}' executed in {end_time - start_time:.4f} seconds")
            return result
        return wrapper