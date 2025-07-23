import time
from datetime import datetime

import pytz
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.content_encoding import ContentEncoding
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem


def create_webhook_log(session_id: str, kst_time: datetime) -> HTTPLogItem:
    utc_time = pytz.timezone("Asia/Seoul").localize(kst_time).astimezone(pytz.utc)
    timestamp_ms = int(utc_time.timestamp() * 1000)

    return HTTPLog(
        [
            HTTPLogItem(
                ddsource="local",
                ddtags="env:test",
                hostname="liam",
                message="webhook sent",
                service="mock_event_notifier",
                value=1,
                session_id=session_id,
                timestamp=timestamp_ms,
            ),
        ]
    )


def create_close_log(session_id: str, kst_time: datetime) -> HTTPLog:
    utc_time = pytz.timezone("Asia/Seoul").localize(kst_time).astimezone(pytz.utc)
    timestamp_ms = int(utc_time.timestamp() * 1000)

    return HTTPLog(
        [
            HTTPLogItem(
                ddsource="local",
                ddtags="env:test",
                hostname="liam",
                message="close request",
                service="mock_ai_api",
                value=0,
                session_id=session_id,
                timestamp=timestamp_ms,
            ),
        ]
    )


def send_custom_logs(log: HTTPLog):
    start_time = datetime.now()
    configuration = Configuration()

    with ApiClient(configuration) as api_client:
        api_instance = LogsApi(api_client)
        api_instance.submit_log(content_encoding=ContentEncoding.DEFLATE, body=log)

        end_time = datetime.now()
        print(f"time taken to submit logs: {(end_time - start_time).total_seconds()}")


if __name__ == "__main__":
    """
    09:00:00 - close request, session id0
    09:00:10 - close request, session id1
    09:00:30 - send webhook, session id0
    09:00:40 - send webhook, session id1
    """

    session_id0, datetime0 = "20250722083824_abcde", datetime(2025, 7, 24, 9, 0, 0)
    session_id1, datetime1 = "20250722083824_12345", datetime(2025, 7, 24, 9, 0, 10)

    # close - session id0
    close_log0 = create_close_log(session_id0, datetime0)
    send_custom_logs(close_log0)
    time.sleep(10)

    # close - session id1
    close_log1 = create_close_log(session_id1, datetime1)
    send_custom_logs(close_log1)
    time.sleep(20)

    # webhook - session id0
    webhook_log0 = create_webhook_log(session_id0, datetime0)
    send_custom_logs(webhook_log0)
    time.sleep(10)

    # webhook - session id1
    webhook_log1 = create_webhook_log(session_id1, datetime1)
    send_custom_logs(webhook_log1)
