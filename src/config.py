import logging

class InfoOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO

class NotInfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno != logging.INFO


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "info_only": {
            "()": InfoOnlyFilter,
        },
        "not_info": {
            "()": NotInfoFilter,
        },
    },
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] %(levelname)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "console_format": {
            "format": "%(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console_format",
            "level": "INFO",
            "filters": ["info_only"],
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "mode": "a",
            "filename": "sim.log",
            "maxBytes": 5 * 1024 * 1024,  # 5 MB before rotating
            "backupCount": 5,
            "level": "DEBUG",
            "filters": ["not_info"],
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        }
    },
}