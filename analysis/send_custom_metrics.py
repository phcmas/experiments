from datetime import datetime
import time

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.metrics_api import MetricsApi
from datadog_api_client.v2.model.metric_intake_type import MetricIntakeType
from datadog_api_client.v2.model.metric_payload import MetricPayload
from datadog_api_client.v2.model.metric_point import MetricPoint
from datadog_api_client.v2.model.metric_resource import MetricResource
from datadog_api_client.v2.model.metric_series import MetricSeries


def create_metric_payload(session_id: str, value: int, timestamp: int) -> MetricPayload:
    return MetricPayload(
        series=[
            MetricSeries(
                metric="session.webhook_sent",
                type=MetricIntakeType.GAUGE,
                points=[MetricPoint(timestamp=timestamp, value=value)],
                resources=[MetricResource(name=session_id, type="session_id")],
            ),
        ],
    )


def send_custom_metrics(payload: MetricPayload):
    start_time = datetime.now()
    configuration = Configuration()

    with ApiClient(configuration) as api_client:
        api_instance = MetricsApi(api_client)
        response = api_instance.submit_metrics(payload)

        end_time = datetime.now()
        print(f"time taken to submit metrics: {(end_time - start_time).total_seconds()}")
        print(response)


def main():
    """
    09:00:00 - close request, session id0
    09:00:10 - close request, session id1
    09:00:30 - send webhook, session id0
    09:00:40 - send webhook, session id1
    """

    session_id0, timestamp0 = "20250722083824_m9ng8", int(datetime.now().timestamp())
    session_id1, timestamp1 = "20250722083824_1a2b3", int(datetime.now().timestamp())

    # close request - session id0
    payload1 = create_metric_payload(session_id0, 1, timestamp0)
    send_custom_metrics(payload1)
    time.sleep(30)

    # close request - session id1
    payload1 = create_metric_payload(session_id1, 0, timestamp1)
    send_custom_metrics(payload1)
    time.sleep(20)

    # send webhook - session id0
    payload2 = create_metric_payload(session_id0, 1, timestamp0)
    send_custom_metrics(payload2)
    time.sleep(10)

    # send webhook - session id1
    payload3 = create_metric_payload(session_id1, 1, timestamp1)
    send_custom_metrics(payload3)


if __name__ == "__main__":
    main()
