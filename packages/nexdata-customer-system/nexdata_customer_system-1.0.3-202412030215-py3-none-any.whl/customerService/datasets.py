import requests
from loguru import logger
from customerService.base import Base
from customerService.constants import API
from customerService.page_params import PageParams


# dataset
class Datasets(Base):
    """Classes used for creating datasets, obtaining dataset lists, dataset information, updating, and deleting datasets.

    usage ::

        auth = Auth(app_key='your-app-key', app_secret='your-app-secret')
        dataset = Datasets(auth)
    """

    def dataset_list(self, page: PageParams, dataset_state=None):
        """Query existing datasets under the current customer.

        usage ::
            page = PageParams()
            page.page = 1
            page.page_size = 10
            dataset_list = dataset.dataset_list(page=page)['responseList']
            print('My datasets is : ', dataset_list)

        :param page: Current page number
        :param page_size: Quantity per page
        :param dataset_state: Dataset status (00: Unassociated task, 01: Task in progress, 02: Task completed)
        :return:
        """
        params = {
            "page": page.page,
            "pageSize": page.page_size,
            "datasetState": dataset_state,
        }
        response_result = requests.get(
            self.host + API.DATASET_LIST,
            headers=self.get_header(**params),
            params=params,
        )
        response = response_result.json()
        if response["status"] != 200:
            raise Exception(response)
        return response

    def dataset_info(self, dataset_id: str):
        """Obtain detailed information on a dataset under the current customer.

        usage ::

            dataset_info = dataset.dataset_info(dataset_id='your-dataset-id')['responseObject']
            print('My dataset is : ', dataset_info)

        :param dataset_id: Dataset Id
        :return:
        """
        params = {"dataSetId": dataset_id}
        api_addr = API.DATASET_INFO.replace("{dataSetId}", dataset_id)
        response_result = requests.get(
            self.host + api_addr, headers=self.get_header(**params), params=params
        )
        response = response_result.json()
        if response["status"] != 200:
            raise Exception(response)
        return response

    def create_dataset(self, dataset_name: str, order_ids: str, storage_area: str):
        """create a dataset.

        usage ::

            dataset_id = dataset.create_dataset(dataset_name='your-dataset-name',order_ids='order_ids',storage_area='storage_area')['responseObject']
            print('My dataset_id is : ', dataset_id)

        :param dataset_name: Dataset name
        :param order_ids: Order ID, multiple order IDs separated by ','
        :return:
        """
        params = {
            "dataSetName": dataset_name,
            "orderIds": order_ids,
            "storageArea": storage_area,
        }
        response_result = requests.post(
            self.host + API.CREATE_DATASET,
            headers=self.get_header(**params),
            params=params,
        )
        response = response_result.json()
        if response["status"] != 200:
            logger.error(
                f"create {dataset_name} dataset error. response_msg: {response}"
            )
            raise Exception(response)
        return response

    def update_dataset(
        self,
        dataset_id: str,
        dataset_name: str,
        add_order_ids: str,
        remove_order_ids: str,
    ):
        """update dataset.

        usage ::

            dataset.update_dataset(dataset_id='your-dataset-id', dataset_name='dataset_name',
            add_order_ids='add_order_ids', remove_order_ids='remove_order_ids')

        :param dataset_id: Dataset Id
        :param dataset_name: Dataset name
        :param add_order_ids: Add associated order IDs, separate multiple order IDs with ","
        :param remove_order_ids: Remove associated order IDs, separate multiple order IDs with ","
        :return:
        """
        params = {
            "dataSetName": dataset_name,
            "addRelatedOrderIds": add_order_ids,
            "removeRelatedOrderIds": remove_order_ids,
        }
        api_addr = API.UPDATE_DATASET.replace("{dataSetId}", dataset_id)
        response_result = requests.patch(
            self.host + api_addr, headers=self.get_header(**params), params=params
        )
        response = response_result.json()
        if response["status"] != 200:
            raise Exception(response)
        return response

    def delete_dataset(self, dataset_id: str):
        """delete a dataset.

        usage ::

            dataset.delete_dataset(dataset_id='your-dataset-id')

        :param dataset_id: Dataset Id
        :return:
        """
        params = {"dataSetId": dataset_id}
        api_addr = API.DELETE_DATASET.replace("{dataSetId}", dataset_id)
        response_result = requests.delete(
            self.host + api_addr, headers=self.get_header(**params), params=params
        )
        response = response_result.json()
        if response["status"] != 200:
            raise Exception(response)
        return response

    def data_state(self, dataSetId: str, batchId: str, dataId: str = None, **args):
        """retrieve the data processed state of the data set

        usage ::

            data_state_list = dataset.data_state(dataSetId='your-dataset-id',batchId='your-batch-id',
            dataId='your-data-id')['responseList'] print(data_state_list)

        :param dataSetId: dataset_id
        :param batchId: batch_id
        :param dataId: data_id
        :param args:
        :return:
        """
        url = self.host + API.DATA_STATE.format(dataSetId=dataSetId, batchId=batchId)
        params = {"dataSetId": dataSetId, "batchId": batchId, "dataId": dataId}
        response = requests.get(url, headers=self.get_header(**params), params=params)
        if response.json()["status"] != 200:
            raise Exception(response.json())
        return response.json()

    def data_processed_result(
        self, dataSetId: str, batchId: str, dataId: str = None, **args
    ):
        """get the annotation results of the data

        usage ::

            data_processed_result_list = dataset.data_processed_result(dataSetId='your-dataset-id',
            batchId='your-batch-id',dataId='your-data-id')['responseList'] print(data_processed_result_list)

        :param dataSetId: dataset_id
        :param batchId: batch_id
        :param dataId: data_id
        :param args:
        :return:
        """
        url = self.host + API.DATA_PROCESSED_RESULT.format(
            dataSetId=dataSetId, batchId=batchId
        )
        params = {"dataSetId": dataSetId, "batchId": batchId, "dataId": dataId}
        response = requests.get(url, headers=self.get_header(**params), params=params)
        if response.json()["status"] != 200:
            raise Exception(response.json())
        return response.json()

    def data_files(
        self,
        pageParam: PageParams,
        dataSetId: str,
        batchId: str,
        parentPath: str,
        zipName: str,
    ):
        """Get details of the dataset file

        usage :: page = PageParams() page.size = 1 page.page_size = 10 data_file_list = dataset.data_files(
        pageParam=page,dataSetId='your-dataset-id',batchId='your-batch-id',parentPath='parent_path',
        zipName='zip_name')['responseList'] print(data_file_list)

        :param pageParam: page
        :param dataSetId: dataset_id
        :param batchId: batch_id
        :param parentPath: File Path
        :param zipName: Zip package name
        :return:
        """
        url = self.host + API.DATA_FILES.format(dataSetId=dataSetId, batchId=batchId)
        params = {
            "dataSetId": dataSetId,
            "batchId": batchId,
            "parentPath": parentPath,
            "zipName": zipName,
            "page": pageParam.page,
            "pageSize": pageParam.page_size,
        }
        response = requests.get(url, headers=self.get_header(**params), params=params)
        if response.json()["status"] != 200:
            raise Exception(response.json())
        return response.json()

    def data_files_statistics(self, dataSetId: str, batchId: str, zipName: str):
        """Statistics of Batch Data Files within a Dataset

        usage :: data_files_statistics = dataset.data_files(dataSetId='your-dataset-id',batchId='your-batch-id',
        zipName='zip_name')['responseObject'] print(data_files_statistics)

        :param dataSetId: dataset_id
        :param batchId: batch_id
        :param zipName: Zip package name
        :return:
        """

        url = self.host + API.DATA_FILES_STATISTICS.format(
            dataSetId=dataSetId, batchId=batchId
        )
        params = {"dataSetId": dataSetId, "batchId": batchId, "zipName": zipName}
        response = requests.get(url, headers=self.get_header(**params), params=params)
        if response.json()["status"] != 200:
            raise Exception(response.json())
        return response.json()


class DatasetBatchs(Base):
    """dataset batch

    usage ::

        auth = Auth(app_key='your-app-key', app_secret='your-app-secret')
        dataset_batch = DatasetBatchs(auth)
    """

    def dataset_batch_list(self, dataset_id: str, page: PageParams):
        """Obtain all dataset batches for a certain dataset under the current customer.

        usage ::

            page = PageParams()
            page.size = 1
            page.page_size = 10
            dataset_batch_list = dataset_batch.dataset_batch_list(dataset_id='your-dataset-id', page=page)['responseList']
            print(dataset_batch_list)

        :param dataset_id: Dataset Id
        :param page: Current page number
        :param page_size: Quantity per page
        :return:
        """
        params = {"page": page.page, "pageSize": page.page_size}
        api_addr = API.BATCH_LIST.replace("{dataSetId}", dataset_id)
        response_result = requests.get(
            self.host + api_addr, headers=self.get_header(**params), params=params
        )
        response = response_result.json()
        if response["status"] != 200:
            raise Exception(response)
        return response

    def dataset_batch_info(self, dataset_id: str, batch_id: str):
        """Query the detailed information of a specified dataset batch in a dataset under the current customer.

        usage ::

            dataset_batch_info = dataset_batch.dataset_batch_info(dataset_id='your-dataset-id', batch_id='your-batch-id')['responseObject']
            print(dataset_batch_info)

        :param dataset_id: Dataset Id
        :param batch_id: Batch Id
        :return:
        """
        params = {"dataSetId": dataset_id, "batchId": batch_id}
        api_addr = API.BATCH_INFO.replace("{dataSetId}", dataset_id).replace(
            "{batchId}", batch_id
        )
        response_result = requests.get(
            self.host + api_addr, headers=self.get_header(**params), params=params
        )
        response = response_result.json()
        if response["status"] != 200:
            raise Exception(response)
        return response

    def dataset_batch_data_list(
        self, dataset_id: str, batch_id: str, data_id: str = None
    ):
        """Query detailed information of data list under a dataset batch.

        usage ::

            dataset_batch_data_list = dataset_batch.dataset_batch_data_list(dataset_id='your-dataset-id',
            batch_id='your-batch-id',data_id='your-data-id')['responseList'] print(dataset_batch_data_list)

        :param dataset_id: Dataset Id
        :param batch_id: Batch Id
        :param data_id: Data Id
        :return:
        """
        params = {"dataId": data_id}
        api_addr = API.BATCH_DATA_LIST.replace("{dataSetId}", dataset_id).replace(
            "{batchId}", batch_id
        )
        response_result = requests.get(
            self.host + api_addr, headers=self.get_header(**params), params=params
        )
        response = response_result.json()
        if response["status"] != 200:
            raise Exception(response)
        return response

    def create_dataset_batch(
        self, dataset_id: str, batch_name: str, comment: str = None
    ):
        """create a dataset batch.

        usage ::

            dataset_batch = dataset_batch.create_dataset_batch(dataset_id='your-dataset-id',
            batch_name='your-batch-name',comment='comment')['responseList'] print(dataset_batch)

        :param dataset_id: Dataset Id
        :param batch_name: Batch Name
        :param comment: remarks
        :return:
        """
        params = {"dataSetId": dataset_id, "batchName": batch_name, "comment": comment}
        api_addr = API.CREATE_BATCH.replace("{dataSetId}", dataset_id)
        response_result = requests.post(
            self.host + api_addr, headers=self.get_header(**params), params=params
        )
        response = response_result.json()
        if response["status"] != 200:
            raise Exception(response)
        return response

    def delete_dataset_batch(self, dataset_id: str, batch_id: str):
        """Delete the specified dataset batch under the current customer

        usage ::

            dataset_batch.delete_dataset_batch(dataset_id='your-dataset-id', batch_id='your-batch-id')

        :param dataset_id: Dataset Id
        :param batch_id: Batch Id
        :return:
        """
        params = {"dataSetId": dataset_id, "batchId": batch_id}
        api_addr = API.DELETE_BATCH.replace("{dataSetId}", dataset_id).replace(
            "{batchId}", batch_id
        )
        response_result = requests.delete(
            self.host + api_addr, headers=self.get_header(**params), params=params
        )
        response = response_result.json()
        if response["status"] != 200:
            raise Exception(response)
        return response
