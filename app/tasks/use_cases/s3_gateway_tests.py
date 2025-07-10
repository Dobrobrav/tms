from io import BytesIO
from unittest.mock import Mock, call

import pytest
from mypy_boto3_s3 import S3Client

from tasks.use_cases.s3_gateway import S3Gateway, S3FileKey
from tms import settings


class TestS3GatewayUploadsFileMultipart:

    def test__s3_gateway_calls_s3_client_correctly(self) -> None:
        # Arrange
        s3_gateway = S3Gateway(m_s3_client := Mock(spec=S3Client), _chunk_size=5)
        m_s3_client.create_multipart_upload.return_value = {'UploadId': (test_upload_id := 'test_upload_id')}
        m_s3_client.upload_part.side_effect = [{'ETag': f'etag_1'}, {'ETag': f'etag_2'}, {'ETag': f'etag_3'}]

        test_bytes_stream = BytesIO(b'abcdefghijklm')
        test_file_key = S3FileKey('test_key')
        test_filename = 'test_filename'

        # Act
        s3_gateway.upload_file(test_bytes_stream, test_file_key, test_filename)

        # Assert
        m_s3_client.create_multipart_upload.assert_called_once_with(
            Bucket=settings.SELECTEL_BUCKET,
            Key=test_file_key,
            # TODO: what about ContentDisposition?
            ContentDisposition=f'attachment; filename="{test_filename}"'
        )

        assert m_s3_client.upload_part.call_args_list == [
            call(
                Bucket=settings.SELECTEL_BUCKET,
                Key=test_file_key,
                PartNumber=i,
                UploadId=test_upload_id,
                Body=chunk,
            )
            for i, chunk in zip(range(1, 4), [b'abcde', b'fghij', b'klm'])
        ]

        m_s3_client.complete_multipart_upload.assert_called_once_with(
            Bucket=settings.SELECTEL_BUCKET,
            Key=test_file_key,
            UploadId=test_upload_id,
            MultipartUpload={
                'Parts': [
                    {'ETag': 'etag_1', 'PartNumber': 1},
                    {'ETag': 'etag_2', 'PartNumber': 2},
                    {'ETag': 'etag_3', 'PartNumber': 3},
                ]
            }
        )

    def test__s3_gateway_aborts_upload__if_gets_exception_during_upload(self) -> None:
        # Arrange
        m_s3_client = Mock(spec=S3Client)
        test_upload_id = 'test_upload_id'
        m_s3_client.create_multipart_upload.return_value = {'UploadId': test_upload_id}
        test_exception = RuntimeError
        m_s3_client.upload_part.side_effect = [
            {'ETag': f'etag_1'},
            test_exception,  # arbitrary exception
        ]

        s3_gateway = S3Gateway(m_s3_client, _chunk_size=5)

        test_bytes_stream = BytesIO(b'abcdefghijklm')
        test_file_key = S3FileKey('test_key')
        test_filename = 'test_filename'

        # Act & Assert
        with pytest.raises(test_exception):
            s3_gateway.upload_file(test_bytes_stream, test_file_key, test_filename)

        # Assert
        m_s3_client.create_multipart_upload.assert_called_once_with(
            Bucket=settings.SELECTEL_BUCKET,
            Key=test_file_key,
            ContentDisposition=f'attachment; filename="{test_filename}"'
        )

        assert m_s3_client.upload_part.call_args_list == [
            call(
                Bucket=settings.SELECTEL_BUCKET,
                Key=test_file_key,
                PartNumber=1,
                UploadId=test_upload_id,
                Body=b'abcde',
            ),
            call(
                Bucket=settings.SELECTEL_BUCKET,
                Key=test_file_key,
                PartNumber=2,
                UploadId=test_upload_id,
                Body=b'fghij',
            ),
        ]

        m_s3_client.abort_multipart_upload.assert_called_once_with(
            Bucket=settings.SELECTEL_BUCKET,
            Key=test_file_key,
            UploadId=test_upload_id,

        )
