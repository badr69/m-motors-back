import logging
import os


def setup_logger(name: str = "m-motors"):

    # =====================
    # CREATE LOGS DIRECTORY
    # =====================
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # =====================
    # LOGGER INSTANCE
    # =====================
    logger = logging.getLogger(name)

    # prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # =====================
    # FORMATTER
    # =====================
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # =====================
    # CONSOLE HANDLER
    # =====================
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # =====================
    # FILE HANDLER
    # =====================
    file_handler = logging.FileHandler(
        "logs/app.log",
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    # =====================
    # ADD HANDLERS
    # =====================
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger