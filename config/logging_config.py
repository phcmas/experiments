import logging


def init_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level=logging.INFO)

    logger = logging.getLogger()
    logger.setLevel(level=logging.INFO)
    logger.addHandler(stream_handler)
