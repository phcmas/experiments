import json
import boto3
from botocore.exceptions import ClientError
import os
import logging

from dotenv import dotenv_values

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ENVS = dotenv_values(f"{CURRENT_PATH}/.env")

AWS_REGION = ENVS["AWS_REGION"]
AWS_PROFILE = ENVS["AWS_PROFILE"]
ENDPOINT_URL = ENVS["ENDPOINT_URL"]

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")

boto3.setup_default_session(profile_name=AWS_PROFILE)
s3_client = boto3.client("s3", region_name=AWS_REGION, endpoint_url=ENDPOINT_URL)


def create_bucket(name: str):
    try:
        response = s3_client.create_bucket(
            Bucket=name, CreateBucketConfiguration={"LocationConstraint": AWS_REGION}
        )
    except ClientError:
        logger.exception("Could not create S3 bucket locally")
        raise
    except Exception as error:
        logger.error(error)
        raise

    return response


def main():
    bucket_name = "hands-on-cloud-localstack-bucket"
    logger.info("Creating S3 bucket locally using localstack")
    s3 = create_bucket(bucket_name)
    logger.info("S3 bucket create")
    logger.info(json.dumps(s3, indent=4) + "\n")


main()
