import sys

from loguru import logger


def setup_logger(mode: str = "development") -> None:
    logger.remove()

    if mode == "test":
        return

    logger_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    console_level = "DEBUG" if mode == "development" else "INFO"

    logger.add(
        sys.stdout,
        format=logger_format,
        level=console_level,
        colorize=True,
    )

    logger.add(
        "logs/agrow.log",
        format=logger_format,
        level="INFO",
        rotation="10 MB",
        retention=5,
        compression="zip",
        colorize=True,
    )
