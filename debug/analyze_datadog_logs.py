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


def analyze_logs(fileName: str):
    logs0 = load_logs_from_file(fileName)
    frame0 = pl.DataFrame(logs0, schema={"function": pl.String, "file": pl.String, "duration": pl.Float32})

    statistics = (
        frame0.group_by("function", "file")
        .agg(
            pl.count("function").alias("call_count"),
            pl.col("duration").sum().alias("total_duration"),
            pl.col("duration").mean().alias("mean_duration"),
            pl.col("duration").max().alias("max_duration"),
            pl.col("duration").min().alias("min_duration"),
            pl.col("duration").std().alias("std_duration"),
        )
        .sort("function", "file")
    )

    logger.info(f"{fileName} has {len(frame0)} records")

    return statistics


def main():
    result0 = analyze_logs("2024-06-28.pkl")
    # result1 = analyze_logs("2024-06-14.pkl")

    # numeric0 = result0.drop("function").drop("file")
    # numeric1 = result1.drop("function").drop("file")

    # difference = numeric0.with_columns([pl.col(c) - numeric1[c] for c in numeric0.columns])

    result0.write_excel("2024-06-28.xlsx")
    # result1.write_excel("2024-06-14.xlsx")


main()
