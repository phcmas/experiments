import json

import boto3
import boto3.session

from config import load_env, logger

settings = load_env()
boto3.setup_default_session(profile_name=settings.AWS_PROFILE)

sqs_session = boto3.session.Session()
sqs_client = sqs_session.client(
    service_name="sqs",
    region_name=settings.AWS_REGION,
    endpoint_url=settings.ENDPOINT_URL,
)


def send_message(sqs_url: str, payload: dict):
    try:
        response = sqs_client.send_message(QueueUrl=sqs_url, MessageBody=json.dumps(payload))
    except Exception as exc:
        logger.exception(exc)
        raise

    return response


def receive_message(sqs_url: str):
    try:
        response = sqs_client.receive_message(
            QueueUrl=sqs_url,
            MaxNumberOfMessages=2,
            WaitTimeSeconds=1,
        )
    except Exception as exc:
        logger.exception(exc)
        raise

    return response


def main():
    logger.info("sqs message sended")
    sqs_url = settings.SQS_URL
    payload = {"hello": 1}

    send_message(sqs_url, payload)
    send_message(sqs_url, payload)
    send_message(sqs_url, payload)

    response = receive_message(sqs_url)
    response = receive_message(sqs_url)
    response = receive_message(sqs_url)

    logger.info(response)


main()
