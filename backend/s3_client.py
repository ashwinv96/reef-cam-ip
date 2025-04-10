import boto3
from config import S3_ACCESS_KEY, S3_SECRET_KEY, S3_ENDPOINT

# Initialize the S3 client
s3 = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
)