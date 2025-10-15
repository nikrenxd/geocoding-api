from logging import config


def logging_config() -> dict:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "[%(levelname)s] - %(asctime)s - %(name)s - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": "DEBUG",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "services.geodata.client": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False,
            },
            "services.geodata.service": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False,
            },
            "repositories.geodata": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False,
            },
            "tasks": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }


def setup_logging() -> None:
    logging_cfg = logging_config()
    config.dictConfig(logging_cfg)
