from customerService.auth import Auth
from customerService.datasets import DatasetBatchs, Datasets
from customerService.upload import Upload

# TODO Please replace your app_key (str) and app_secret (str)
app_key = 'your app_key'
app_secret = 'your app_secret'

# auth
auth = Auth(app_key=app_key, app_secret=app_secret)

# Create a dataset
dataset = Datasets(auth)
# TODO Please replace your dataset name (str)
dataset_name = 'your dataset_name'

# Example: My dataset needs to be associated with order A, and the ID of order A is 625
# order_id = 625
# TODO Please replace your order id (int)
order_id = 'your order_id'

# storage area【0： China；1：Singapore-(Asia Pacific) Southeast Asia； 2：The United States-(US) West US；
# 3：Japan-(Asia Pacific) Japan East； 4：Korea-(Asia Pacific) Korea Central；5：Germany-(Europe) Germany West Central】
# Example: my stroage area is Singapore-(Asia Pacific) Southeast Asia
# storage_area = 1
storage_area = 'your storage_area'
dataset_id = dataset.create_dataset(dataset_name=dataset_name, order_ids=order_id, storage_area=storage_area)['responseObject']

# Create dataset batch
batchs = DatasetBatchs(auth)
# TODO Please replace your batch name (str)
batch_name = 'your batch_name'
batch_id = batchs.create_dataset_batch(dataset_id=dataset_id, batch_name=batch_name, comment='')['responseList'][0]['batchId']

# TODO Please replace your file path (str)
# Attention: The file size in the folder cannot exceed 100GB
# Example: file_path = 'D:\code\customer\customer-service-python-sdk\\temp'
file_path = 'your file_path'
upload = Upload(auth=auth, dataset_id=dataset_id, batch_id=batch_id, file_path=file_path,
                region=storage_area)

# execute
upload.execute()
