# logger.py

from enum import Enum
import logging
import os
from typing import Any, Optional
from logging.handlers import RotatingFileHandler

class LoggerConfig(Enum):
    MAIN_LEVEL = 1
    CONSOLE_LEVEL = 2
    FORMAT = 3
    LOG_TO_FILE_FLAG = 4
    FILE_LEVEL = 5
    LOG_FILE_PATH = 6
    USE_ROTATING_FILE = 7
    MAX_BYTES = 8
    BACKUP_COUNT = 9

_logger_cache = {}

def setup_logger(name: str, config: Optional[dict[LoggerConfig, Any]] = None) -> logging.Logger:
    logger = get_cached_logger(name)
    if logger:
        return logger

    default_config = get_default_config()
    config = {**default_config, **(config or {})}
    
    validate_config(config)

    logger = logging.getLogger(name)
    logger.setLevel(config[LoggerConfig.MAIN_LEVEL])

    if not logger.handlers:
        formatter = create_formatter(config[LoggerConfig.FORMAT])
        add_console_handler(logger, formatter, config)
        if config[LoggerConfig.LOG_TO_FILE_FLAG]:
            add_file_handler(logger, formatter, config)

        cache_logger(name, logger)
        
    return logger

def get_default_config() -> dict[LoggerConfig, Any]:
    return {
        LoggerConfig.LOG_TO_FILE_FLAG: True,
        LoggerConfig.LOG_FILE_PATH: 'logs/cli_tool.log',
        LoggerConfig.MAIN_LEVEL: logging.INFO,
        LoggerConfig.CONSOLE_LEVEL: logging.INFO,
        LoggerConfig.FILE_LEVEL: logging.INFO,
        LoggerConfig.FORMAT: '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        LoggerConfig.MAX_BYTES: 10 * 1024 * 1024,
        LoggerConfig.BACKUP_COUNT: 3,
        LoggerConfig.USE_ROTATING_FILE: True
    }

def validate_config(config: dict[LoggerConfig, Any]) -> None:
    if config[LoggerConfig.MAX_BYTES] <= 0:
        raise ValueError(f"Invalid MAX_BYTES: {config[LoggerConfig.MAX_BYTES]}. It must be a positive integer.")
    if config[LoggerConfig.BACKUP_COUNT] < 0:
        raise ValueError(f"Invalid BACKUP_COUNT: {config[LoggerConfig.BACKUP_COUNT]}. It must be non-negative.")

def add_console_handler(logger: logging.Logger, formatter: logging.Formatter, config: dict[LoggerConfig, Any]) -> None:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(config[LoggerConfig.CONSOLE_LEVEL])
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

def add_file_handler(logger: logging.Logger, formatter: logging.Formatter, config: dict[LoggerConfig, Any]) -> None:
    log_file = config[LoggerConfig.LOG_FILE_PATH]
    log_dir = os.path.dirname(log_file)

    ensure_log_directory_exists(log_dir)

    try:
        if config[LoggerConfig.USE_ROTATING_FILE]:
            file_handler = setup_rotating_file_handler(config)
        else:
            file_handler = setup_standard_file_handler(config)
        file_handler.setLevel(config[LoggerConfig.FILE_LEVEL])
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.error(f"Failed to set up file handler for log file '{log_file}': {e}")
        raise

def setup_rotating_file_handler(config: dict[LoggerConfig, Any]) -> RotatingFileHandler:
    log_file = config[LoggerConfig.LOG_FILE_PATH]
    return RotatingFileHandler(
        log_file,
        maxBytes=config[LoggerConfig.MAX_BYTES],
        backupCount=config[LoggerConfig.BACKUP_COUNT]
    )

def setup_standard_file_handler(config: dict[LoggerConfig, Any]) -> logging.FileHandler:
    log_file = config[LoggerConfig.LOG_FILE_PATH]
    return logging.FileHandler(log_file)

def ensure_log_directory_exists(log_dir: str) -> None:
    if log_dir:
        try:
            os.makedirs(log_dir, exist_ok=True)
        except OSError as e:
            raise RuntimeError(f"Failed to create log directory '{log_dir}': {e}")

def create_formatter(format_string: str) -> logging.Formatter:
    return logging.Formatter(format_string)

def get_cached_logger(name: str) -> Optional[logging.Logger]:
    return _logger_cache.get(name)

def cache_logger(name: str, logger: logging.Logger) -> None:
    _logger_cache[name] = logger
