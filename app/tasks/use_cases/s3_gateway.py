import structlog
from mypy_boto3_s3 import S3Client

from tms import settings
from tms_types import BytesStream

logger = structlog.get_logger(__name__)


class S3Gateway:

    def __init__(
            self,
            s3_client: S3Client,
            *,
            _chunk_size: int = 5 * 1024 * 1024,  # _chunk_size used FOR TESTS ONLY!
    ) -> None:
        self._s3_client = s3_client
        self._chunk_size = _chunk_size

    def upload_file(self, bytes_stream: BytesStream, file_key: 'S3FileKey', filename: str) -> None:
        logger.info('start uploading file', file_key=file_key)
        upload_id = self._s3_client.create_multipart_upload(
            Bucket=settings.SELECTEL_BUCKET,
            Key=file_key,
            ContentDisposition=f'attachment; filename="{filename}"',
        )['UploadId']

        try:
            self._upload_stream_multipart(bytes_stream, file_key, upload_id)
        except Exception as e:
            self._s3_client.abort_multipart_upload(Bucket=settings.SELECTEL_BUCKET, Key=file_key, UploadId=upload_id)
            raise e

        logger.info('finished uploading file', file_key=file_key)

    def _upload_stream_multipart(self, bytes_stream: BytesStream, key: 'S3FileKey', upload_id: str) -> None:
        parts = []
        part_number = 1
        while chunk := bytes_stream.read(self._chunk_size):
            e_tag = self._s3_client.upload_part(
                Bucket=settings.SELECTEL_BUCKET,
                Key=key,
                PartNumber=part_number,
                UploadId=upload_id,
                Body=chunk,
            )['ETag']
            parts.append({'ETag': e_tag, 'PartNumber': part_number})
            part_number += 1

        self._s3_client.complete_multipart_upload(
            Bucket=settings.SELECTEL_BUCKET,
            Key=key,
            UploadId=upload_id,
            MultipartUpload={'Parts': parts}
        )


class S3FileKey(str):
    ...
