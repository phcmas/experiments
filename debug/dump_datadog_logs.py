import json
import pickle
from datetime import datetime
from typing import List

import pytz
import requests

from config import load_settings, logger

settings = load_settings()


def extract_year_month_day(date: datetime):
    return date.isoformat().split("T")[0]


def call_datadog_logs_api(query: dict, index: int):
    url = "https://api.datadoghq.com/api/v2/logs/events/search"
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": settings.DATADOG_API_KEY,
        "DD-APPLICATION-KEY": settings.DATADOG_APP_KEY,
    }

    try:
        response = requests.request(method="POST", url=url, headers=headers, data=json.dumps(query)).json()
        cursor = response["meta"]["page"]["after"] if "page" in response["meta"] else None
        logger.info(
            msg=f" Datadog API Called Sucessfully - {index}, Timestamp: {response['data'][-1]['attributes']['timestamp']}"
        )
    except Exception as err:
        logger.error(err)
        return

    return cursor, [attr["attributes"]["attributes"] for attr in response["data"]]


def get_datadog_logs(started_at: datetime, ended_at: datetime):
    query = {
        "filter": {"from": f"{started_at.isoformat()}", "to": f"{ended_at.isoformat()}", "query": "PERFORMANCE"},
        "page": {"cursor": None, "limit": 5000},
        "sort": "@pageViews",
    }
    result, index = [], 0

    while True:
        cursor, data = call_datadog_logs_api(query, index)
        query["page"]["cursor"] = cursor
        result += data
        index += 1

        if cursor is None:
            break

    return result


def get_datetime(year: int, month: int, day: int, hour: int, minute: int, second: int):
    time = datetime(year, month, day, hour, minute, second)
    return time.astimezone(pytz.timezone("Asia/Seoul"))


def write_file(started_at: datetime, result: List[dict]):
    file_name = f"{extract_year_month_day(started_at)}.pkl"
    with open(file_name, "wb") as file:
        pickle.dump(result, file)


def main():
    started_at0 = get_datetime(2024, 6, 13, 5, 0, 0)
    ended_at0 = get_datetime(2024, 6, 13, 8, 0, 0)
    result0 = get_datadog_logs(started_at0, ended_at0)
    write_file(started_at0, result0)

    # started_at1 = get_datetime(2024, 6, 7, 5, 0, 0)
    # ended_at1 = get_datetime(2024, 6, 7, 8, 0, 0)
    # result1 = get_datadog_logs(started_at1, ended_at1)

    # result = result0
    # write_file(started_at0, result)

    print("Done!")


main()
