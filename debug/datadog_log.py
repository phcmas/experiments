from config import load_settings, logger
import requests
import json

settings = load_settings()

response = requests.request(
    method="POST",
    url="https://api.datadoghq.com/api/v2/logs/events/search",
    headers={
        "Content-Type": "application/json",
        "DD-API-KEY": settings.DATADOG_API_KEY,
        "DD-APPLICATION-KEY": settings.DATADOG_APP_KEY,
    },
    data=json.dumps(
        {
            "filter": {"from": "2024-06-07T00:00:00+00:00", "to": "2024-06-07T00:15:00+00:00", "query": "PERFORMANCE"},
            "page": {"limit": 2},
        }
    ),
)

logger.info(response.json())
logger.info(response.json())
