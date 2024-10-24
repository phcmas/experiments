import time
from multiprocessing.pool import ThreadPool
from tempfile import NamedTemporaryFile, _TemporaryFileWrapper
from typing import List, Tuple


import boto3
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError

from config import load_env, logger

settings = load_env()

boto3.setup_default_session(profile_name=settings.AWS_PROFILE)
s3_client = boto3.client("s3", region_name=settings.AWS_REGION, endpoint_url=settings.ENDPOINT_URL)
keys = [
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
keys = [
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2160_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2161_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2162_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2163_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2164_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2165_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2166_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2167_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2168_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2169_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2170_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2171_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2172_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2173_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2174_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2175_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2176_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2177_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2178_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2179_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2180_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2181_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2182_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2183_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2184_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2185_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2186_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2187_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2188_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2189_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2190_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2191_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2192_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2193_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2194_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2195_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2196_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2197_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2198_mel",
    "G-20240612145829-AJIWZtWSKUwQMbSpmBOZ/20240612145838_y16v6/2199_mel",
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


def download_file(parameter: Tuple) -> _TemporaryFileWrapper:
    try:
        s3_client.download_file(
            parameter[0],
            parameter[1],
            parameter[2].name,
            Config=TransferConfig(preferred_transfer_client="classic"),
        )
        logger.info(f"download completed: {parameter[1]}")
    except Exception as exc:
        logger.error(exc)

    return parameter[2]


def download_files(bucket: str, keys: List[str]) -> List[NamedTemporaryFile]:
    pool = ThreadPool(4)
    parameters = [(bucket, key, NamedTemporaryFile()) for key in keys]

    result_list = pool.map_async(download_file, parameters)
    result_list.wait()

    return result_list.get()


def main():
    bucket = "sleep-sessions-data-live"
    # process = psutil.Process(os.getpid())
    # process.cpu_affinity([0, 1])

    download_files(bucket, keys[0:1])

    # start1 = time.perf_counter()
    # result1 = download_files(bucket, keys[0:10])
    # end1 = time.perf_counter()
    # logger.info(f"count: {len(result1)}, duration: {round(end1-start1,3)}")

    sum = 0

    for i in range(20):
        start1 = time.perf_counter()
        result0 = download_files(bucket, keys)
        end1 = time.perf_counter()

        sum += round(end1 - start1, 3)
        logger.info(f"count: {len(result0)}, duration: {round(end1-start1,3)}")

    logger.info(sum / 20)


main()
