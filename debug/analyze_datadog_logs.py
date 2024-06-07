import pickle
import polars as pl

from config.config_logging import logger


def extract_float(value):
    pass


def load_logs_from_file(fileName: str):
    with open(fileName, "rb") as file:
        logs = pickle.load(file)

    return {
        "function": [log["function"] for log in logs],
        "file": [log["file"] for log in logs],
        "duration": [log["duration"] for log in logs],
    }


def main():
    fileName0 = "2024-06-07.pkl"
    logs0 = load_logs_from_file(fileName0)
    frame0 = pl.DataFrame(logs0, schema={"function": pl.String, "file": pl.String, "duration": pl.Float32})

    logger.info(logs0)


main()
