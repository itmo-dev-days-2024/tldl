import io
import logging as log

from minio import Minio
from minio.helpers import ObjectWriteResult


class VideoRepository:
    _client: Minio
    _bucket: str

    def __init__(self, bucket: str, client: Minio):
        self._client = client
        self._bucket = bucket

    def upload_file(self, object_name: str, data: io.BytesIO) -> ObjectWriteResult:
        result = self._client.put_object(
            bucket_name=self._bucket, object_name=object_name, data=data
        )
        return result

    def get_file(self, object_name: str) -> io.BytesIO:
        result = self._client.get_object(
            bucket_name=self._bucket, object_name=object_name
        )
        return result.data
