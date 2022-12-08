from os import environ
from botocore.config import Config

my_config = Config(
    region_name = environ.get('AWS_REGION'),
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    },
    s3={"addressing_style": "virtual"}
)

aws_access = {
    "aws_access_key_id": environ.get('AWS_ACCESS_KEY'),
    "aws_secret_access_key":environ.get('AWS_SECRET_KEY'),
    "aws_session_token": environ.get('AWS_SESSION_TOKEN')
}
