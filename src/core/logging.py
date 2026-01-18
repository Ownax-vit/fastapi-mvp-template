import logging
import logging.config

from src.core.config import settings

LOG_LEVEL = settings.app_log_level


def get_logger(name: str) -> logging.Logger:

    logging_config = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s [%(name)s]: %(message)s",
                "use_colors": True,
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
                "use_colors": True,
            },
        },
        "handlers": {
            "default": {
                "level": LOG_LEVEL,
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "access": {
                "level": "INFO",
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "": {  # root logger
                "level": LOG_LEVEL,
                "handlers": ["default"],
                "propagate": False,
            },
            "src": {
                "level": LOG_LEVEL,
                "handlers": ["default"],
                "propagate": False,
            },
            "uvicorn.error": {
                "level": LOG_LEVEL,
                "handlers": ["default"],
                "propagate": False,
            },
            "uvicorn.access": {
                "level": "INFO",
                "handlers": ["access"],
                "propagate": False,
            },
        },
        "root": {"handlers": ["default"], "level": "DEBUG"},
    }

    logging.config.dictConfig(logging_config)
    return logging.getLogger(name)
