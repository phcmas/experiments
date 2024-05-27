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
