import io
import logging as log

from botocore.client import BaseClient


class VideoRepository:
    _client: BaseClient
    _bucket: str

    def __init__(self, bucket: str, client: BaseClient):
        self._client = client
        self._bucket = bucket

    def upload_file(self, object_name: str, data: str):
        self._client.upload_file(data, self._bucket, object_name)

    def get_file(self, object_name: str, to_filename: str):
        result = self._client.download_file(self._bucket, object_name, to_filename)
        return result
