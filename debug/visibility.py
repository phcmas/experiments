import requests

# queue_url = "http://sqs.ap-northeast-2.localhost.localstack.cloud:4566/000000000000/common-worker"
queue_url = "https://sqs.ap-northeast-2.amazonaws.com/749960970623/sqs-an2-test-sleep-ai-common-worker-standard"

response = requests.get(
    "http://localhost.localstack.cloud:4566/_aws/sqs/messages",
    params={"QueueUrl": queue_url, "ShowInvisible": True, "ShowDelayed": True},
    headers={"Accept": "application/json"},
)

print(response.json())
