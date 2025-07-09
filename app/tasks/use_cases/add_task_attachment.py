import uuid

import boto3
import structlog
from mypy_boto3_s3 import S3Client
from pydantic import HttpUrl, BaseModel, ConfigDict

from tasks.domain.attachments.attachment_entity import AttachmentEntity, Filename
from tasks.domain.attachments.repository import AttachmentRepository
from tasks.domain.tasks.repository import TaskRepository
from tasks.models import AttachmentS3MetaModel
from tasks.use_cases.base import Usecase
from tms import settings
from tms_types import BytesStream

logger = structlog.get_logger(__name__)


class AddTaskAttachmentUsecase(Usecase):
    def __init__(
            self,
            task_repo: TaskRepository,
            attachment_s3_uploader: 'AttachmentS3Uploader',
            attachment_repo: AttachmentRepository,
            storage_for_attachment_s3_meta: 'StorageForAttachmentS3Meta',
    ) -> None:
        self._task_repo = task_repo
        self._attachment_s3_uploader = attachment_s3_uploader
        self._attachment_repo = attachment_repo
        self._storage_for_attachment_s3_meta = storage_for_attachment_s3_meta

    def execute(self, task_id: int, filename: str, bytes_stream: BytesStream) -> HttpUrl:
        s3_file_key = self._attachment_s3_uploader.upload(bytes_stream, filename, task_id)

        attachment_entity = AttachmentEntity(filename=Filename(value=filename))
        attachment_id = self._attachment_repo.set(attachment_entity)

        self._storage_for_attachment_s3_meta.set(AttachmentS3Meta(s3_file_key=s3_file_key, attachment_id=attachment_id))

        task_entity = self._task_repo.get(task_id)
        task_entity.add_attachment_id(attachment_id)
        self._task_repo.set(task_entity)

        return self._attachment_s3_uploader.get_file_url(s3_file_key)


class AttachmentS3Uploader:
    _S3_FOLDER = 'task_attachments'

    def __init__(self, s3_gateway: 'S3Gateway') -> None:
        self._s3_gateway = s3_gateway

    def upload(self, bytes_stream: BytesStream, filename: str, task_id: int) -> 'S3FileKey':
        file_key = S3FileKey(f'{self._S3_FOLDER}/{task_id}/{uuid.uuid4()}')
        self._s3_gateway.upload_file(bytes_stream=bytes_stream, file_key=file_key, filename=filename)
        return file_key

    def get_file_url(self, s3_file_key: 'S3FileKey') -> HttpUrl:
        return HttpUrl(f"https://tms-container.s3.ru-7.storage.selcloud.ru/{s3_file_key}")


class S3Gateway:
    _CHUNK_SIZE = 5 * 1024 * 1024

    def __init__(self, s3_client: S3Client) -> None:
        self._s3_client = s3_client

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
        while chunk := bytes_stream.read(self._CHUNK_SIZE):
            part = self._s3_client.upload_part(
                Bucket=settings.SELECTEL_BUCKET,
                Key=key,
                PartNumber=part_number,
                UploadId=upload_id,
                Body=chunk,
            )
            parts.append({'ETag': part['ETag'], 'PartNumber': part_number})
            part_number += 1

        self._s3_client.complete_multipart_upload(
            Bucket=settings.SELECTEL_BUCKET,
            Key=key,
            UploadId=upload_id,
            MultipartUpload={'Parts': parts}
        )


class S3FileKey(str):
    ...


class AttachmentS3Meta(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    s3_file_key: S3FileKey
    attachment_id: int


class StorageForAttachmentS3Meta:
    def set(self, attachment_s3_meta: AttachmentS3Meta) -> None:
        AttachmentS3MetaModel.objects.create(
            s3_file_key=attachment_s3_meta.s3_file_key,
            attachment_id=attachment_s3_meta.attachment_id
        )


def add_task_attachment_usecase_factory() -> AddTaskAttachmentUsecase:
    s3_client: S3Client = boto3.client(
        "s3",
        endpoint_url=settings.SELECTEL_ENDPOINT_URL,
        aws_access_key_id=settings.SELECTEL_AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.SELECTEL_AWS_SECRET_ACCESS_KEY,
    )

    return AddTaskAttachmentUsecase(
        task_repo=TaskRepository(),
        attachment_s3_uploader=AttachmentS3Uploader(S3Gateway(s3_client)),
        attachment_repo=AttachmentRepository(),
        storage_for_attachment_s3_meta=StorageForAttachmentS3Meta(),
    )
