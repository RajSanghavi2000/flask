import logging
import os

from boto3 import client
from boto3.exceptions import S3UploadFailedError
from botocore.exceptions import ClientError
from azure.storage.blob import BlobServiceClient

from .enum import StorageProvider
from .utility import storage_provider_host_address


class CloudStorageService:
    """ Cloud Storage Service """

    def __init__(self):
        self.storage_provider = os.environ.get('STORAGE_PROVIDER')
        self.aws_region_name = os.environ.get('AWS_SERVICE_REGION_NAME')
        self.storage_client = self.get_client(self.storage_provider)

    def get_client(self, storage_provider):
        """ Get client by storage provider configuration """
        return {
            StorageProvider.S3.value: self.get_s3_client,
            StorageProvider.GCP.value: self.get_gcp_client,
            StorageProvider.LOCAL_STORAGE.value: self.get_local_storage_client,
            StorageProvider.AZURE.value: self.get_azure_client,
        }.get(storage_provider)()

    def get_s3_client(self):
        """ Get S3 client """
        return client(
            StorageProvider.S3.value,
            aws_access_key_id=os.environ.get("AWS_SERVICE_ACCESS_KEY"),
            aws_secret_access_key=os.environ.get("AWS_SERVICE_SECRET_KEY"),
            region_name=self.aws_region_name
        )

    @staticmethod
    def get_gcp_client():
        """ Get GCP client """
        return client(
            StorageProvider.S3.value,
            region_name=StorageProvider.REGION.value,
            endpoint_url=StorageProvider.GCP_ENDPOINT_URL.value,
            aws_access_key_id=os.environ.get("GOOGLE_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("GOOGLE_ACCESS_KEY_SECRET")
        )

    @staticmethod
    def get_azure_client():
        """ Get GCP client """
        return BlobServiceClient.from_connection_string(os.environ.get('AZURE_STORAGE_CONNECTION_STRING'))

    @staticmethod
    def get_local_storage_client():
        """ Get Local storage client """
        return os.environ.get("LOCAL_STORAGE_LOCATION")

    def upload_file_object(self, stream, bucket, content_type, filename, location=''):
        """ Upload file object """
        try:
            if isinstance(self.storage_client, str) and self.storage_client == os.environ.get('LOCAL_STORAGE_LOCATION'):
                file_location = self.get_location_with_filename(filename, bucket, self.storage_client, location)
                with open(file_location, 'wb') as writer:
                    writer.write(stream)
                # Generate location for local storage
                bucket = os.path.join(bucket, location)
            elif self.storage_provider == StorageProvider.AZURE.value:
                filename = os.path.join(location, filename)
                blob_client = self.storage_client.get_blob_client(container=bucket, blob=filename)
                blob_client.upload_blob(stream, overwrite=True, content_type=content_type)
            else:
                # Generate location to store
                filename = os.path.join(location, filename)
                self.storage_client.put_object(Body=stream, Bucket=bucket, Key=filename, ContentType=content_type)

            return storage_provider_host_address(bucket, self.storage_provider, self.aws_region_name, filename)

        except (ClientError, S3UploadFailedError) as e:
            msg = 'CloudStorageException -File Upload {}'.format(e)
            logging.exception(msg)
        except Exception as e:
            msg = 'StorageException -File Upload {}'.format(e)
            logging.exception(msg)

    def get_location_with_filename(self, filename, bucket, storage_location, location):
        """ Get location with filename """
        self.create_directory_if_not_exists(storage_location, bucket, location)
        return os.path.join(storage_location, bucket, location, filename)

    @staticmethod
    def create_directory_if_not_exists(storage_location, bucket, location):
        """ Create directory if the location directory is not exists """
        path = os.path.join(storage_location, bucket, location)
        if not os.path.exists(path):
            os.makedirs(path)
