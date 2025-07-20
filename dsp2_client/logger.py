import logging
import os


def get_logger(name: str = "dsp2client") -> logging.Logger:
    """
    Create and return a configured logger.
    """
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        log_level = os.getenv("DSP2CLIENT_LOG_LEVEL", "INFO").upper()
        logger.setLevel(getattr(logging, log_level, logging.INFO))

        handler = logging.StreamHandler()
        handler.setLevel(logger.level)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger


logger = get_logger()
