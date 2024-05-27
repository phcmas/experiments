import json
import sys
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

PATH = Path(__file__).parent.resolve().parent.resolve()
sys.path.append(str(PATH))

from config import load_environments, logger

environments = load_environments()

boto3.setup_default_session(profile_name=environments.AWS_PROFILE)
s3_client = boto3.client(
    "s3", region_name=environments.AWS_REGION, endpoint_url=environments.ENDPOINT_URL
)


def create_bucket(name: str):
    try:
        response = s3_client.create_bucket(
            Bucket=name, CreateBucketConfiguration={"LocationConstraint": environments.AWS_REGION}
        )
    except ClientError:
        logger.exception("Could not create S3 bucket locally")
        raise
    except Exception as error:
        logger.error(error)
        raise

    return response


def main():
    bucket_name = "liam"
    logger.info("Creating S3 bucket locally using localstack")
    s3 = create_bucket(bucket_name)
    logger.info("S3 bucket create")
    logger.info(json.dumps(s3, indent=4) + "\n")


main()
