import requests

from customerService.base import Base
from customerService.constants import API
from customerService.page_params import PageParams


# inspection
class inspection(Base):
    """inspection management

    usage ::

        auth = Auth(app_key='your-app-key', app_secret='your-app-secret')
        inspection = inspection(auth)

    """

    def batch_pieces(
        self, *, pageParam: PageParams, orderId: str, batchNo: str = None, **args
    ):
        """Batch Acceptance List (Piece)

        usage ::

            page = PageParams()
            page.size = 1
            page.page_size = 10
            batch_pieces = inspection.batch_pieces(pageParam=page, orderId='orderId', batchNo='batchNo')['responseList']
            print(batch_pieces)

        :param pageParam:
        :param batchNo:
        :param orderId:
        :param args:
        :return:
        """
        url = self.host + API.BATCH_ACCEPTANCE_LIST_PIECE.format(orderId=orderId)
        params = {
            "orderId": orderId,
            "batchNo": batchNo,
            "page": pageParam.page,
            "pageSize": pageParam.page_size,
        }
        response = requests.get(url, headers=self.get_header(**params), params=params)
        if response.json()["status"] != 200:
            raise Exception(response.json())
        return response.json()

    def batch_piece(self, pageParam: PageParams, batchNo: str, orderId: str, **args):
        """Batch Acceptance Details (Piece)

        usage ::

            page = PageParams()
            page.size = 1
            page.page_size = 10
            batch_pieces = inspection.batch_piece(pageParam=page, batchNo='batchNo', orderId='orderId')['responseList']
            print(batch_pieces)

        :param pageParam:
        :param batchNo:
        :param orderId:
        :param args:
        :return:
        """
        url = self.host + API.BATCH_ACCEPTANCE_DETAILS_PIECE.format(
            orderId=orderId, batchNo=batchNo
        )
        params = {
            "orderId": orderId,
            "batchNo": batchNo,
            "page": pageParam.page,
            "pageSize": pageParam.page_size,
        }
        response = requests.get(url, headers=self.get_header(**params), params=params)
        if response.json()["status"] != 200:
            raise Exception(response.json())
        return response.json()

    def batch_piece_end(
        self, batchNo: str, batchStatus: str, message: str, orderId: str
    ):
        """Batch Acceptance Completed (Piece)

        usage ::

            inspection.batch_piece_end(batchNo='batchNo', batchStatus='batchStatus', message='message',
            orderId='orderId')

        :param batchNo:
        :param batchStatus:
        :param message:
        :param orderId:
        :return:
        """
        url = self.host + API.BATCH_ACCEPTANCE_COMPLETED_PIECE.format(
            orderId=orderId, batchNo=batchNo
        )
        form = {"batchNo": batchNo, "batchStatus": batchStatus, "message": message}
        response = requests.post(url, headers=self.get_header(**form), data=form)
        if response.json()["status"] != 200:
            raise Exception(response.json())
        return response.json()

    def batch_packages(self, pageParam: PageParams, batchNo: str, orderId: str, **args):
        """Batch Acceptance List (Package)

        usage ::

            page = PageParams()
            page.size = 1
            page.page_size = 10
            batch_packages = inspection.batch_packages(pageParam=page, batchNo='batchNo', orderId='orderId')['responseList']
            print(batch_packages)

        :param pageParam:
        :param batchNo:
        :param orderId:
        :param args:
        :return:
        """
        url = self.host + API.BATCH_ACCEPTANCE_LIST_PACKAGE.format(orderId=orderId)
        params = {
            "orderId": orderId,
            "batchNo": batchNo,
            "page": pageParam.page,
            "pageSize": pageParam.page_size,
        }
        response = requests.get(url, headers=self.get_header(**params), params=params)
        if response.json()["status"] != 200:
            raise Exception(response.json())
        return response.json()

    def batch_package_packages(
        self,
        pageParam: PageParams,
        batchNo: str,
        orderId: str,
        packageId: str = None,
        **args
    ):
        """Batch Acceptance Package List (Package)

        usage ::

            page = PageParams() page.size = 1 page.page_size = 10 batch_package_packages =
            inspection.batch_package_packages(pageParam=page, batchNo='batchNo', orderId='orderId',
            packageId='packageId')['responseList'] print(batch_package_packages)

        :param pageParam:
        :param batchNo:
        :param orderId:
        :param packageId:
        :param args:
        :return:
        """
        url = self.host + API.BATCH_ACCEPTANCE_PACKAGE_LIST.format(
            orderId=orderId, batchNo=batchNo
        )
        params = {
            "orderId": orderId,
            "batchNo": batchNo,
            "packageId": packageId,
            "page": pageParam.page,
            "pageSize": pageParam.page_size,
        }
        response = requests.get(url, headers=self.get_header(**params), params=params)
        if response.json()["status"] != 200:
            raise Exception(response.json())
        return response.json()

    def batch_package(
        self, pageParam: PageParams, batchNo: str, orderId: str, packageId: str, **args
    ):
        """Batch Acceptance Details (Package)

        usage ::

            page = PageParams()
            page.size = 1
            page.page_size = 10
            batch_package = inspection.batch_package(pageParam=page, batchNo='batchNo', orderId='orderId', packageId='packageId')['responseList']
            print(batch_package)

        :param pageParam:
        :param batchNo:
        :param orderId:
        :param packageId:
        :param args:
        :return:
        """
        url = self.host + API.BATCH_ACCEPTANCE_DETAILS_PACKAGE.format(
            orderId=orderId, batchNo=batchNo, packageId=packageId
        )
        params = {
            "orderId": orderId,
            "batchNo": batchNo,
            "packageId": packageId,
            "page": pageParam.page,
            "pageSize": pageParam.page_size,
        }
        response = requests.get(url, headers=self.get_header(**params), params=params)
        if response.json()["status"] != 200:
            raise Exception(response.json())
        return response.json()

    def batch_package_end(
        self, batchNo: str, orderId: str, batchStatus: str, message: str, **args
    ):
        """Batch Acceptance Completed (Package)

        usage ::

            inspection.batch_package_end(batchNo='batchNo', orderId='orderId', batchStatus='batchStatus', message='message')

        :param batchNo:
        :param orderId:
        :param batchStatus:
        :param message:
        :param args:
        :return:
        """
        url = self.host + API.Batch_Acceptance_Completed_Package.format(
            orderId=orderId, batchNo=batchNo
        )
        form = {
            "orderId": orderId,
            "batchNo": batchNo,
            "batchStatus": batchStatus,
            "message": message,
        }
        response = requests.post(url, headers=self.get_header(**form), data=form)
        if response.json()["status"] != 200:
            raise Exception(response.json())
        return response.json()
