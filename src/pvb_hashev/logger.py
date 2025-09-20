import logging

def get_logger(name: str) -> logging.Logger:
    """
    Create and configure a logger for the library.
    Uses a NullHandler by default to avoid interfering with user logging setup.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.NullHandler()
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger