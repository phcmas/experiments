from datetime import datetime, timezone
from multiprocessing.pool import ThreadPool
import operator
from tempfile import NamedTemporaryFile
import tempfile
from typing import List

import boto3
from botocore.exceptions import ClientError

from config import load_settings, logger

settings = load_settings()

boto3.setup_default_session(profile_name=settings.AWS_PROFILE)
s3_client = boto3.client("s3", region_name=settings.AWS_REGION, endpoint_url=settings.ENDPOINT_URL)
files = [
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/530_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/531_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/532_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/533_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/534_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/535_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/536_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/537_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/538_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/539_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/540_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/541_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/542_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/543_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/544_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/545_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/546_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/547_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/548_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/549_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/550_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/551_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/552_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/553_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/554_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/555_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/556_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/557_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/558_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/559_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/560_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/561_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/562_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/565_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/566_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/567_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/568_mel",
    "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/569_mel",
]


def create_bucket(name: str):
    try:
        response = s3_client.create_bucket(
            Bucket=name, CreateBucketConfiguration={"LocationConstraint": settings.AWS_REGION}
        )
    except ClientError:
        logger.exception("Could not create S3 bucket locally")
        raise

    return response


def download_file(bucket: str, key: str, temp_file: NamedTemporaryFile):
    s3_client.download_file(bucket, key, temp_file.name)
    return temp_file


def download_files(self, buckets: str, file_paths: List[str]) -> List[NamedTemporaryFile]:
    pool = ThreadPool(4)
    result_list = pool.map_async(download_file, buckets)
    result_list.wait()

    return [item[0] for item in sorted([value for value in result_list.get()], key=operator.itemgetter(1))]


def main():
    bucket = "sleep-sessions-data-live"
    key = "G-20240610233246-FLlfiIBmhnsMxCjroRWy/20240613030859_6xxrb/569_mel"
    temp_file = NamedTemporaryFile()

    result = download_file(bucket, key, temp_file)

    logger.info(result)

    # logger.info("Creating S3 bucket locally using localstack")
    # logger.info("S3 bucket create")
    # logger.info(json.dumps(s3, indent=4) + "\n")


main()
