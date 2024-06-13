import pickle
import polars as pl

from config.config_logging import logger


def extract_float(value):
    if isinstance(value, str):
        return float(value.split(" ")[0])

    return value


def load_logs_from_file(fileName: str):
    with open(fileName, "rb") as file:
        logs = pickle.load(file)

    return {
        "function": [log["function"] for log in logs],
        "file": [log["file"] for log in logs],
        "duration": [extract_float(log["duration"]) for log in logs],
    }


def main():
    fileName0 = "2024-06-13.pkl"
    logs0 = load_logs_from_file(fileName0)
    frame0 = pl.DataFrame(logs0, schema={"function": pl.String, "file": pl.String, "duration": pl.Float32})

    result0 = (
        frame0.group_by("function", "file")
        .agg(
            pl.count("function").alias("call_count"),
            pl.col("duration").sum().alias("total_duration"),
            pl.col("duration").mean().alias("mean_duration"),
            pl.col("duration").max().alias("max_duration"),
            pl.col("duration").min().alias("min_duration"),
            pl.col("duration").std().alias("std_duration"),
        )
        .sort("file")
    )

    result0.write_excel("2024-06-13.xlsx")


main()
