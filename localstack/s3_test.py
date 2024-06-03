import json

import boto3
from botocore.exceptions import ClientError

from config import load_settings, logger

settings = load_settings()

boto3.setup_default_session(profile_name=settings.AWS_PROFILE)
s3_client = boto3.client("s3", region_name=settings.AWS_REGION, endpoint_url=settings.ENDPOINT_URL)


def create_bucket(name: str):
    try:
        response = s3_client.create_bucket(
            Bucket=name, CreateBucketConfiguration={"LocationConstraint": settings.AWS_REGION}
        )
    except ClientError:
        logger.exception("Could not create S3 bucket locally")
        raise

    return response


def main():
    bucket_name = "liam"
    logger.info("Creating S3 bucket locally using localstack")
    s3 = create_bucket(bucket_name)
    logger.info("S3 bucket create")
    logger.info(json.dumps(s3, indent=4) + "\n")


main()
