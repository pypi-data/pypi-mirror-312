class Constants:
    ZIP_SUFFIX = "zip"
    CSV_SUFFIX = "csv"
    FILE_PATH = 'Default'
    UPLOAD_KEY = 'customer.dataset'

    OSS = "OSS"
    REGION_HOME = 0
    AZURE_BLOB = "AZURE_BLOB"
    BLOCK_SIZE = 5 * 1024 * 1024
    MAX_FILE_SIZE = 100 * 1024 * 1024 * 1024
    MAX_DELAY = 32
    MAX_RETRIES = 5


class API:
    """api interface address

    """

    DATASET_LIST = '/crowd-customer/v1.0/datasets'
    DATASET_INFO = '/crowd-customer/v1.0/datasets/{dataSetId}'
    CREATE_DATASET = '/crowd-customer/v1.0/datasets'
    UPDATE_DATASET = '/crowd-customer/v1.0/datasets/{dataSetId}'
    DELETE_DATASET = '/crowd-customer/v1.0/datasets/{dataSetId}'
    DATA_STATE = '/crowd-customer/v1.0/datasets/{dataSetId}/batchs/{batchId}/data/state'
    DATA_PROCESSED_RESULT = '/crowd-customer/v1.0/datasets/{dataSetId}/batchs/{batchId}/data/processed/result'
    DATA_FILES = '/crowd-customer/v1.0/datasets/{dataSetId}/batch/{batchId}/zips/files'
    DATA_FILES_STATISTICS = '/crowd-customer/v1.0/datasets/{dataSetId}/batch/{batchId}/zips/files/statistics'

    BATCH_LIST = '/crowd-customer/v1.0/datasets/{dataSetId}/batchs'
    BATCH_DATA_LIST = '/crowd-customer/v1.0/datasets/{dataSetId}/batchs/{batchId}/data'
    BATCH_INFO = '/crowd-customer/v1.0/datasets/{dataSetId}/batchs/{batchId}'
    CREATE_BATCH = '/crowd-customer/v1.0/datasets/{dataSetId}/batchs'
    DELETE_BATCH = '/crowd-customer/v1.0/datasets/{dataSetId}/batchs/{batchId}'

    STORAGE_AUTH = '/crowd-customer/zone/storage/auth'
    ACCESS_SIGNED = '/crowd-customer/zone/storage/getAccessSigned'
    UPLOAD_BEGIN = '/crowd-customer-dataset-alone/dataset/{dataSetId}/batch/{batchId}/{fileName}/begin'
    UPLOAD_END = '/crowd-customer-dataset-alone/dataset/{dataSetId}/batch/{batchId}/{fileName}/end'
    UPLOAD_PROGRESS = '/crowd-customer-dataset-alone/v1.0/datasets/{dataSetId}/batchs/{batchId}/upload/progress'
    UPLOAD_COMPLETE = '/crowd-customer-dataset-alone/v1.0/datasets/{dataSetId}/batchs/{batchId}/upload/complete'

    ORDER_LIST = '/crowd-customer/v1.0/orders'
    ORDER_DETAIL = '/crowd-customer/v1.0/orders/detail'
    ORDER_DATASET_LIST = '/crowd-customer/v1.0/orders/{orderId}/datasets'
    DELIVERY_BATCH_DETAILS = '/crowd-customer/v1.0/orders/{orderId}/deliveries/{batchId}'
    DELIVERY_BATCH_RESULT = '/crowd-customer/v1.0/orders/{orderId}/deliveries/{batchId}/result'
    DELIVERIES = '/crowd-customer/v1.0/orders/{orderId}/deliveries'
    ORDER_PROGRESS = '/crowd-customer/v1.0/{orderId}/progress'
    TASK_PROGRESS_LIST = '/crowd-customer/v1.0/orders/{orderId}/task/progress'

    BATCH_ACCEPTANCE_LIST_PIECE = '/crowd-customer/v1.0/orders/{orderId}/piece/inspection'
    BATCH_ACCEPTANCE_DETAILS_PIECE = '/crowd-customer/v1.0/orders/{orderId}/piece/inspection/{batchNo}'
    BATCH_ACCEPTANCE_COMPLETED_PIECE = '/crowd-customer/v1.0/orders/{orderId}/piece/inspection/{batchNo}'
    BATCH_ACCEPTANCE_LIST_PACKAGE = '/crowd-customer/v1.0/orders/{orderId}/package/inspection'
    BATCH_ACCEPTANCE_PACKAGE_LIST = '/crowd-customer/v1.0/orders/{orderId}/package/inspection/{batchNo}'
    BATCH_ACCEPTANCE_DETAILS_PACKAGE = '/crowd-customer/v1.0/orders/{orderId}/package/inspection/{batchNo}/packages/{packageId}'
    Batch_Acceptance_Completed_Package = '/crowd-customer/v1.0/orders/{orderId}/package/inspection/{batchNo}'
