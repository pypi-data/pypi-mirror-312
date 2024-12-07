import requests

# order
from customerService.base import Base
from customerService.constants import API
from customerService.page_params import PageParams


class order(Base):
    """Order management

    usage ::

        auth = Auth(app_key='your-app-key', app_secret='your-app-secret')
        order = order(auth)

    """

    def orders(self, pageParam: PageParams, **args):
        """get order list

        usage ::

            page = PageParams()
            page.size = 1
            page.page_size = 10
            order_list = order.orders(pageParam=page)['responseList']
            print(order_list)

        :param pageParam: Paging parameters
        :param args:
        :return:
        """
        url = self.host + API.ORDER_LIST
        params = {"page": pageParam.page, "pageSize": pageParam.page_size}
        response = requests.get(url, headers=self.get_header(**params), params=params)
        if response.json()["status"] != 200:
            raise Exception(response.json())
        return response.json()

    def order_details(self, pageParam: PageParams, orderId: str, **args):
        """Order detail (Batch Detail)

        usage ::

            page = PageParams()
            page.size = 1
            page.page_size = 10
            order_details = order.order_details(pageParam=page, orderId='order_id')['responseList']
            print(order_details)

        :param pageParam:
        :param orderId:
        :param args:
        :return:
        """
        url = self.host + API.ORDER_DETAIL
        params = {
            "orderId": orderId,
            "page": pageParam.page,
            "pageSize": pageParam.page_size,
        }
        response = requests.get(url, headers=self.get_header(**params), params=params)
        if response.json()["status"] != 200:
            raise Exception(response.json())
        return response.json()

    def order_datasets(self, pageParam: PageParams, orderId: str, **args):
        """Order Dataset List

        usage ::

            page = PageParams()
            page.size = 1
            page.page_size = 10
            order_datasets = order.order_datasets(pageParam=page, orderId='order_id')['responseList']
            print(order_datasets)

        :param pageParam:
        :param orderId:
        :param args:
        :return:
        """
        url = self.host + API.ORDER_DATASET_LIST.format(orderId=orderId)
        params = {
            "orderId": orderId,
            "page": pageParam.page,
            "pageSize": pageParam.page_size,
        }
        response = requests.get(url, headers=self.get_header(**params), params=params)
        if response.json()["status"] != 200:
            raise Exception(response.json())
        return response.json()

    def order_deliveries(self, pageParam: PageParams, orderId: str, **args):
        """Delivery Batch List

        usage ::

            page = PageParams()
            page.size = 1
            page.page_size = 10
            order_deliveries = order.order_deliveries(pageParam=page, orderId='order_id')['responseList']
            print(order_deliveries)

        :param pageParam:
        :param orderId:
        :param args:
        :return:
        """
        url = self.host + API.DELIVERIES.format(orderId=orderId)
        params = {
            "orderId": orderId,
            "page": pageParam.page,
            "pageSize": pageParam.page_size,
        }
        response = requests.get(url, headers=self.get_header(**params), params=params)
        if response.json()["status"] != 200:
            raise Exception(response.json())
        return response.json()

    def order_deliveries_detail(self, orderId: str, batchId: str, **args):
        """Delivery Batch Details

        usage ::

            order_deliveries_detail = order.order_deliveries_detail(orderId='order_id', batchId='batch_id')[
            'responseObject'] print(order_deliveries_detail)

        :param orderId:
        :param batchId:
        :param args:
        :return:
        """
        url = self.host + API.DELIVERY_BATCH_DETAILS.format(
            orderId=orderId, batchId=batchId
        )
        params = {"orderId": orderId, "batchId": batchId}
        response = requests.get(url, headers=self.get_header(**params), params=params)
        if response.json()["status"] != 200:
            raise Exception(response.json())
        return response.json()

    def order_deliveries_result(
        self, orderId: str, batchId: str, cursor: str, size: int, **args
    ):
        """Delivery Batch Result

        usage ::

            order_deliveries_result = order.order_deliveries_result(orderId='order_id', batchId='batch_id',
            cursor='cursor', size='size')['responseObject'] print(order_deliveries_result)

        :param orderId: order_id
        :param batchId: batch_id
        :param cursor: The cursor for pagination query is initially passed empty, and then the next cursor value in the return parameter is passed
        :param size: Page length, default value 50, maximum value 100
        :param args:
        :return:
        """
        url = self.host + API.DELIVERY_BATCH_RESULT.format(
            orderId=orderId, batchId=batchId
        )
        size = 50 if not size else size
        params = {
            "orderId": orderId,
            "batchId": batchId,
            "cursor": cursor,
            "size": size,
        }
        response = requests.get(url, headers=self.get_header(**params), params=params)
        if response.json()["status"] != 200:
            raise Exception(response.json())
        return response.json()

    def order_progress(self, orderId: str, **args):
        """Order Progress

        usage ::

            order_progress = order.order_progress(orderId='order_id')['responseObject']
            print(order_progress)

        :param orderId:
        :param args:
        :return:
        """
        url = self.host + API.ORDER_PROGRESS
        params = {"orderId": orderId}
        response = requests.get(url, headers=self.get_header(**params), params=params)
        if response.json()["status"] != 200:
            raise Exception(response.json())
        return response.json()

    def order_task_progress(self, orderId: str, **args):
        """Task Progress List

        usage ::

            order_task_progress = order.order_task_progress(orderId='order_id')['responseList']
            print(order_task_progress)

        :param orderId: orderId
        :param args:
        :return:
        """
        url = self.host + API.TASK_PROGRESS_LIST.format(orderId=orderId)
        params = {"orderId": orderId}
        response = requests.get(url, headers=self.get_header(**params), params=params)
        if response.json()["status"] != 200:
            raise Exception(response.json())
        return response.json()
