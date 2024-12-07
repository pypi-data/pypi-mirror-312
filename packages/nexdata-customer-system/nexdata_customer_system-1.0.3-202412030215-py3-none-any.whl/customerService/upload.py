import concurrent
import json
import os
import queue
import random
import threading
import time
from datetime import datetime

from loguru import logger
import oss2
import requests
from oss2 import determine_part_size, SizedFileAdapter

from customerService.auth import Auth
from customerService.base import Base
from customerService.constants import Constants, API
from azure.storage.blob import BlobServiceClient


# file upload
class Upload(Base):
    """Handling file uploads

    usage ::
        auth = Auth(app_key='your-app-key', app_secret='your-app-secret')
        upload = Upload(auth=auth, dataset_id='dataset_id', batch_id='batch_id', file_path='file_path', region='storage_area')
    """

    def __init__(
        self, auth: Auth, dataset_id: str, batch_id: str, file_path: str, region: str
    ):
        self.auth = auth
        self.region = region
        super().__init__(auth)
        self.batch_id = batch_id
        self.file_path = file_path
        self.dataset_id = dataset_id

    def execute(self):
        """Handling file upload methods

        usage ::

            upload.execute()

        :return:
        """
        if not os.path.exists(self.file_path):
            raise RuntimeError("file not found:", self.file_path)
        if not os.path.isdir(self.file_path):
            raise RuntimeError("not a folder:", self.file_path)

        total_size = 0
        files = self._walk_file()
        # create sync queue
        file_queue = queue.Queue(len(files))
        relative_position = self.file_path.rfind(os.sep) + 1
        for file in files:
            # file absolute path
            absolute_path = file
            file_size = os.path.getsize(file)

            total_size += file_size
            # intercept relative path
            relative_path = os.path.basename(absolute_path)
            if not absolute_path.endswith(".zip") and not absolute_path.endswith(
                ".csv"
            ):
                relative_path = os.path.join(
                    Constants.FILE_PATH, relative_path
                ).replace("\\", "/")

            # join to queue
            file_queue.put([absolute_path, relative_path])

        if total_size > Constants.MAX_FILE_SIZE:
            logger.error("The total file size cannot exceed 100G")
            raise Exception("The total file size cannot exceed 100G")
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            while not file_queue.empty():
                file = file_queue.get()
                self.file_path = file[0]
                self.file_name = file[1]

                upload = MultipartUpload(
                    self.auth,
                    self.dataset_id,
                    self.batch_id,
                    self.file_path,
                    self.file_name,
                    self.region,
                )
                upload.multipart_upload()

            # Call processing tool
            self.upload_complete()

    # Call processing tool
    def upload_complete(self):
        # If it is a CSV upload, there is no need to call data processing
        if self.file_name.endswith(Constants.CSV_SUFFIX):
            return

        params = {"clusterId": self.dataset_id, "uploadId": self.batch_id}
        api_addr = API.UPLOAD_COMPLETE.replace("{dataSetId}", self.dataset_id).replace(
            "{batchId}", self.batch_id
        )
        response_result = requests.post(
            self.host + api_addr, headers=self.get_header(**params), params=params
        )
        response = response_result.json()
        if response["status"] != 200:
            raise Exception("get storage auth failed. ", response)
        logger.info(
            "Call processing tool ---> end，dataset_id={}，batch_id={}",
            self.dataset_id,
            self.batch_id,
        )

    # iterate over files
    def _walk_file(self):
        all_files = []
        for root, dirs, files in os.walk(self.file_path):
            for f in files:
                # exclude hidden files
                if not f.startswith("."):
                    all_files.append(os.path.join(root, f))
        return all_files


class MultipartUpload(Base):

    def __init__(
        self,
        auth: Auth,
        dataset_id: str,
        batch_id: str,
        file_path: str,
        file_name: str,
        region: str,
    ):
        self.auth = auth
        self.region = region
        super().__init__(auth)
        self.batch_id = batch_id
        self.file_name = file_name
        self.file_path = file_path
        self.dataset_id = dataset_id

    def multipart_upload(self):
        # Preparation before uploading
        self.init_upload()

        # multipart upload
        storage = StorageFactory().create_storage(
            self.auth,
            self.dataset_id,
            self.batch_id,
            self.file_path,
            self.file_name,
            self.region,
        )
        auth_path = storage.multipart_upload()

        # Processing after upload completion
        self.end_upload(auth_path)

    # Preparation before uploading
    def init_upload(self):
        file_name = self.file_name.rsplit("/")[-1]
        file_length = os.path.getsize(self.file_path)
        params = {"fileLength": file_length, "fileName": file_name}
        api_addr = (
            API.UPLOAD_BEGIN.replace("{dataSetId}", self.dataset_id)
            .replace("{batchId}", self.batch_id)
            .replace("{fileName}", file_name)
        )
        response_result = requests.post(
            self.host + api_addr, headers=self.get_header(**params), params=params
        )
        response = response_result.json()
        if response["status"] != 200:
            raise Exception("get storage auth failed. ", response)
        logger.info(
            "Preparation before uploading ---> end，dataset_id={}，batch_id={}，file_name={}",
            self.dataset_id,
            self.batch_id,
            self.file_name,
        )

    # Processing after upload completion
    def end_upload(self, auth_path: str):
        result_url = self.get_access_signed(auth_path)
        file_name = self.file_name.rsplit("/")[-1]
        file_length = os.path.getsize(self.file_path)
        params = {
            "size": file_length,
            "fileName": file_name,
            "resultUrl": result_url,
            "remotePath": auth_path,
        }
        api_addr = (
            API.UPLOAD_END.replace("{dataSetId}", self.dataset_id)
            .replace("{batchId}", self.batch_id)
            .replace("{fileName}", file_name)
        )
        response_result = requests.post(
            self.host + api_addr, headers=self.get_header(**params), params=params
        )
        response = response_result.json()
        if response["status"] != 200:
            raise Exception("get storage auth failed. ", response)
        logger.info(
            "Processing after upload completion ---> end，dataset_id={}，batch_id={}，file_name={}",
            self.dataset_id,
            self.batch_id,
            self.file_name,
        )

    # Obtain file signature
    def get_access_signed(self, auth_path: str):
        params = {"authPath": auth_path, "region": self.region}
        response_result = requests.get(
            self.host + API.ACCESS_SIGNED,
            headers=self.get_header(**params),
            params=params,
        )
        response = response_result.json()
        if response["status"] != 200:
            raise Exception("get storage auth failed. ", response.json())
        return response["responseObject"]

    # Get file type
    def get_file_type(self):
        return str(self.file_name.rsplit(".", 1)[-1]).lower()


class StorageFactory:

    @staticmethod
    def create_storage(
        auth: Auth,
        dataset_id: str,
        batch_id: str,
        file_path: str,
        file_name: str,
        region: str,
    ):
        if Constants.REGION_HOME == region:
            return Oss(auth, dataset_id, batch_id, file_path, file_name, region)
        else:
            return Blob(auth, dataset_id, batch_id, file_path, file_name, region)

    def get_storage_auth(
        self, auth: Auth, dataset_id: str, batch_id: str, file_name: str, region: str
    ):
        """Obtain and upload temporary key"""
        params = {
            "clusterId": dataset_id,
            "uploadId": batch_id,
            "region": region,
            "key": Constants.UPLOAD_KEY,
            "fileName": file_name,
        }
        base = Base(auth)
        response_result = requests.get(
            base.host + API.STORAGE_AUTH,
            headers=base.get_header(**params),
            params=params,
        )
        response = response_result.json()
        if response["status"] != 200:
            raise Exception("get storage auth failed. ", response.json())
        response_object = response["responseObject"]
        storage = response_object["storage"]
        if storage == Constants.OSS:
            auth_token = json.loads(response_object["authToken"])
            auth_token["authPath"] = os.path.join(
                response_object["authPath"], file_name
            ).replace("\\", "/")
            auth_token["storage"] = response_object["storage"]
        elif storage == "BLOB":
            response_object["storage"] = Constants.AZURE_BLOB
            auth_token = response_object
        return auth_token

    def update_upload_progress(
        self,
        upload_size: int,
        total_size: int,
        auth: Auth,
        dataset_id: str,
        batch_id: str,
    ):
        """update upload progress

        :param upload_size: file uploaded size
        :param total_size:  tile total size
        :return:
        """
        try:
            if upload_size == total_size:
                return
            progress = round(upload_size / total_size, 2)
            params = {"progress": progress}
            base = Base(auth)
            api_addr = API.UPLOAD_PROGRESS.replace("{dataSetId}", dataset_id).replace(
                "{batchId}", batch_id
            )
            response_result = requests.put(
                auth.host + api_addr, headers=base.get_header(**params), params=params
            )
            response = response_result.json()
            if response["status"] != 200:
                raise Exception("get storage auth failed. ", response)
            logger.info(
                "update upload progress ---> dataset_id={}，batch_id={}，progress={}",
                dataset_id,
                batch_id,
                progress,
            )
        except Exception as ex:
            logger.info("update upload progress failed:", ex)

    # Verify if the token has expired
    def token_expiration(self, expiration: str):
        if not expiration:
            return False
        timestamp = datetime.strptime(expiration, "%Y-%m-%dT%H:%M:%SZ")
        current_time = datetime.utcnow()
        if timestamp < current_time:
            return False
        else:
            return True


class Oss(StorageFactory):
    def __init__(
        self,
        auth: Auth,
        dataset_id: str,
        batch_id: str,
        file_path: str,
        file_name: str,
        region: str,
    ):
        self.auth = auth
        self.bucket = None
        self.region = region
        self.auth_path = None
        self.expiration = None
        self.batch_id = batch_id
        self.file_name = file_name
        self.file_path = file_path
        self.dataset_id = dataset_id

    def multipart_upload(self):
        # Obtain the unique event ID for uploading shards
        upload_id = self._init_multipart_upload()

        # OSS shard upload
        parts = self._upload(upload_id)

        # complete
        self._complete(upload_id, parts)

        return self.auth_path

    def _init_multipart_upload(self):
        return self.get_bucket().init_multipart_upload(self.auth_path).upload_id

    def _upload(self, upload_id):
        # OSS shard upload
        part_size = determine_part_size(
            oss2.defaults.multipart_threshold, preferred_size=Constants.BLOCK_SIZE
        )
        total_size = os.path.getsize(self.file_path)
        parts = []

        with open(self.file_path, "rb") as fileobj:
            offset = 0
            part_number = 1
            while offset < total_size:

                retries = 0
                num_to_upload = min(part_size, total_size - offset)
                while retries < Constants.MAX_RETRIES:
                    try:
                        result = self.get_bucket().upload_part(
                            self.auth_path,
                            upload_id,
                            part_number,
                            SizedFileAdapter(fileobj, num_to_upload),
                        )
                        parts.append(oss2.models.PartInfo(part_number, result.etag))

                        offset += num_to_upload
                        part_number += 1
                        retries = Constants.MAX_RETRIES
                        logger.info("oss multipart uploading....")
                    except Exception as e:
                        logger.error(
                            f"The {retries + 1}th request for fragment upload failed  :",
                            str(e),
                        )
                        delay = 2**retries + random.uniform(0, 1)
                        delay = min(delay, Constants.MAX_DELAY)
                        time.sleep(delay)
                        retries += 1
                        if retries < Constants.MAX_RETRIES:
                            offset += num_to_upload

        return parts

    def get_bucket(self):
        # If the token expires, renew it
        if not self.token_expiration(self.expiration):
            # Retrieve temporary key for storing objects
            storage_auth = self.get_storage_auth(
                self.auth, self.dataset_id, self.batch_id, self.file_name, self.region
            )
            endpoint = storage_auth["endpoint"]
            sts_token = storage_auth["SecurityToken"]
            self.expiration = storage_auth["Expiration"]
            sts_access_key_id = storage_auth["AccessKeyId"]
            sts_access_key_secret = storage_auth["AccessKeySecret"]
            # Initialize OSS client
            auth = oss2.StsAuth(sts_access_key_id, sts_access_key_secret, sts_token)

            bucket_name = storage_auth["Bucket"]
            self.auth_path = storage_auth["authPath"]
            self.bucket = oss2.Bucket(auth, endpoint, bucket_name)
        return self.bucket

    def _complete(self, upload_id: str, parts: list):
        # complete
        self.get_bucket().complete_multipart_upload(self.auth_path, upload_id, parts)
        logger.info("file {} complete end", self.auth_path)


class Blob(StorageFactory):
    def __init__(
        self,
        auth: Auth,
        dataset_id: str,
        batch_id: str,
        file_path: str,
        file_name: str,
        region: str,
    ):

        self.auth = auth
        self.region = region
        self.auth_path = None
        self.expiration = None
        self.blob_client = None
        self.batch_id = batch_id
        self.file_path = file_path
        self.blob_name = file_name
        self.dataset_id = dataset_id

    def multipart_upload(self):

        offset = 0
        block_list = []
        block_id_prefix = "block-"
        block_size = Constants.BLOCK_SIZE
        total_size = os.path.getsize(self.file_path)

        with open(self.file_path, "rb") as f:
            index = 0
            while True:
                data = f.read(block_size)
                if not data:
                    break

                retries = 0
                num_to_upload = min(block_size, total_size - offset)
                while retries < Constants.MAX_RETRIES:
                    try:
                        block_id = block_id_prefix + "{:06d}".format(index)
                        self.get_blob_client().stage_block(block_id, data)
                        logger.info(f"Block {block_id} staged successfully.")
                        block_list.append(block_id)
                        index += 1
                        offset += num_to_upload

                        retries = Constants.MAX_RETRIES
                        logger.info("blob multipart uploading....")
                    except Exception as e:
                        logger.error(
                            f"The {retries + 1}th request for fragment upload failed  :",
                            str(e),
                        )
                        delay = 2**retries + random.uniform(0, 1)
                        delay = min(delay, Constants.MAX_DELAY)
                        time.sleep(delay)
                        retries += 1
                        if retries < Constants.MAX_RETRIES:
                            offset += num_to_upload

        try:
            self.get_blob_client().commit_block_list(block_list)
            logger.info(f"Blob {self.blob_name} uploaded successfully.")
        except Exception as ex:
            logger.info("Failed to commit block list:", ex)
        return self.auth_path

    def get_blob_client(self):
        if not self.blob_client:
            storage_auth = self.get_storage_auth(
                self.auth, self.dataset_id, self.batch_id, self.blob_name, self.region
            )
            account_url = storage_auth["endpoint"]
            credential = storage_auth["authToken"]
            container_name = storage_auth["container"]
            # Create a BlobServiceClient using the STS token
            blob_service_client = BlobServiceClient(account_url, credential)
            container_client = blob_service_client.get_container_client(container_name)
            # Get a client to the blob

            self.auth_path = storage_auth["authPath"]
            self.blob_client = container_client.get_blob_client(
                blob=storage_auth["authPath"]
            )
        return self.blob_client
