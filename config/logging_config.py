import logging


def init_logging():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level=logging.INFO)
    stream_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))

    logger = logging.getLogger()
    logger.setLevel(level=logging.INFO)
    logger.addHandler(stream_handler)
