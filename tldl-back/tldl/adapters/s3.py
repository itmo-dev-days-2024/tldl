import boto3
import boto3.s3


def create_boto_client(endpoint: str, access_key: str, secret_key: str):
    return boto3.client(
        service_name="s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
