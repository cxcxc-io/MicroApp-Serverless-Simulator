import boto3

from flask import jsonify

from daos.dynamodb_dao import DynamoDBDao
from daos.s3_dao import S3Dao


class Controller:
    """接收API輸入並處理、控制流程與調用組件"""
    
    @classmethod
    def check_localstack_connection(cls):
        """確認 localstack 是否成功串接
        
        呼叫 boto3 客戶端物件, 用此物件讀取 S3, 取得所有值區名稱
        若成功讀取, 回傳「成功連線到 LocalStack！」
        若失敗, 回傳「無法連線到 LocalStack： error」
        """
        # 創建 s3 客戶端
        s3 = boto3.client('s3',
            region_name='us-east-1',  # 指定區域，localstack-pro 的默認區域是 us-east-1
            endpoint_url='http://localstack:4566',  # localstack-pro 的 S3 服務 URL localstack 是 docker compose 的 container 服務名稱
            aws_access_key_id='test',  # 測試用的 AWS 存取金鑰 ID
            aws_secret_access_key='test' # 測試用的 AWS 秘密存取金鑰
            )  
        
        # 測試是否成功連線
        try:
            response = s3.list_buckets()["Buckets"]
            print(f"值區清單: {response}")
            print("成功連線到 LocalStack！")
            return "成功連線到 LocalStack！"
        except Exception as e:
            print("無法連線到 LocalStack：", str(e))
            return "無法連線到 LocalStack：" + str(e)
 
    @classmethod
    def check_dynamodb_connection(cls):
        """確認 dynamodb 是否成功串接
        
        使用 dynamodb dao, 讀取 dynamodb 服務, 列出所有表格
        若成功, 回傳「已連接到 LocalStack 的 DynamoDB 服務」
        若失敗，回傳「無法連接到 LocalStack 的 DynamoDB 服務」
        """
 
        dynamodb_tables  =  DynamoDBDao.check_dynamodb()
        
        if dynamodb_tables:
            return "已連接到 LocalStack 的 DynamoDB 服務"
        else:
            return "無法連接到 LocalStack 的 DynamoDB 服務"
        
    @classmethod
    def create_table(cls, table_name):
        """建立新表格
        
        使用 DynamoDBDao 創建表格, 
        若成功創建, 回傳「表格 {table_name} 建立成功」
        若失敗, 回傳「表格 {table_name} 建立失敗」
        """
        response = DynamoDBDao.create_table(table_name)

        if response:
            return f"表格 {table_name} 建立成功"
        else:
            return f"表格 {table_name} 建立失敗"
    
    @classmethod
    def insert_data_into_dynamodb(cls, table_name, request_data):
        """插入資料到資料表
        
        使用 DynamoDBDao 插入一筆資料，並傳入要插入的表格名稱
        若有回應，則回傳「插入資料成功」
        若無回應，則回傳「插入資料失敗」
        """
        data = request_data.get_json()
        response = DynamoDBDao.insert_into_dynamodb(table_name, data)
        
        if response:
            return "插入資料成功"
        else:
            return "插入資料失敗"
    
    @classmethod
    def scan_dynamodb(cls, table_name):
        """查詢特定表格的內容

        使用 DynamoDBDao 的查詢資料表功能
        若成功, 則回傳「查詢的結果」
        若失敗, 則回傳「查詢資料表 {table_name} 失敗」
        """
        response = DynamoDBDao.scan_dynamodb(table_name)
        if response:
            return response
        else:
            return f"查詢資料表 {table_name} 失敗"
        
    @classmethod
    def query_db(cls, table_name, id):
        """查詢特定表格的特定 id 資料

        使用 DynamoDBDao 的查詢資料功能, 查詢特定表格的特定主鍵的值
        若成功, 回傳該值
        若失敗, 回傳「查無資料」
        """
        response = DynamoDBDao.query_dynamodb(table_name, id)

        if response:
            return response
        else:
            return "查無資料"
    
    @classmethod
    def update_dynamodb_data(cls, table_name, new_request_data):
        """更新特定表格的特定資料

        取出 用戶傳的資料
        使用 DynamoDBDao 的更新資料方法, 傳入表格名稱與資料
        回傳結果
        """
        data = new_request_data.get_json()
        response = DynamoDBDao.update_dynamodb_item(table_name, data)
        return response
    
    @classmethod
    def soft_delete_item(cls, table_name, request_data):
        """軟刪除資料
        
        取出用戶傳的資料
        使用 DynamoDBDao 的 軟刪除功能, 並傳入表格名稱與資料
        """
        data = request_data.get_json()
        response = DynamoDBDao.soft_delete_item(table_name, data)
        return response
    
    @classmethod
    def delete_item(cls, table_name, id):
        """直接刪除資料

        使用 DynamoDBDao 的刪除方法並傳入表格名稱與特定 ID 進行刪除
        """
        response = DynamoDBDao.delete_item(table_name, id)
        return str(response)
    
    # S3
    @classmethod
    def check_s3_connection(cls):
        """確認 S3 是否可以串接, 並回傳結果"""
        return S3Dao.check_s3_connection()
    
    @classmethod
    def create_s3_bucket(cls, bucket_name):
        """創建 S3 值區
        
        使用 S3Dao 的創建值區方法,
        若成功, 回傳「成功建立 {bucket_name} 值區」
        若失敗, 回傳「值區建立失敗」
        """
        response = S3Dao.create_bucket(bucket_name)
        if response:

            return f"成功建立 {bucket_name} 值區"
        else:
            return "值區建立失敗"
        
    @classmethod
    def upload_s3_object(cls, bucket_name, data_request):
        """上傳 S3 物件到特定值區

        接收用戶傳過來的物件名稱與檔案 byte
        使用 S3Dao 的上傳物件方法, 
        若成功, 回傳「上傳成功」, 
        若失敗, 回傳「上傳失敗」        
        """
        object_name = data_request.form["object_name"]
        print(object_name)
        data_byte = data_request.files["file"].read()
        print("data_byte")
        print(data_byte)
        response = S3Dao.upload_bytes(bucket_name, object_name, data_byte)
        
        if response:
            return "上傳成功"
        else:
            return "上傳失敗"
        
    @classmethod
    def download_file(cls, bucket_name, data_request):
        """下載檔案至程式碼所在的專案資料夾
        
        獲取用戶傳的物件名稱與檔案名稱
        使用 S3Dao 的下載檔案功能, 將檔案下載到程式碼所在的專案資料夾
        若成功, 回傳「下載成功」
        若失敗, 回傳「下載失敗」
        """
        object_name = data_request.form["object_name"]
        file_name = data_request.form["file_name"]
        response = S3Dao.download_file(bucket_name, object_name, file_name)
        if response:
            return "下載成功"
        else:
            return "下載失敗"
        
    @classmethod
    def update_s3_object(cls, bucket_name, data_request):
        """更新 S3 物件
        
        獲取用戶傳的物件名稱、檔案 byte
        使用 S3Dao 的更新物件方法, 傳入值區名稱、物件名稱與物件的 byte
        若成功, 回傳「更新成功」
        若失敗, 回傳「更新失敗」
        """
        object_name = data_request.form["object_name"]
        print(object_name)
        data_byte = data_request.files["file"].read()
        print("data_byte")
        # print(data_byte)
        response = S3Dao.update_object(bucket_name, object_name, data_byte)
        
        if response:
            return "更新成功"
        else:
            return "更新失敗"
    
    @classmethod
    def delete_s3_object(cls, bucket_name, data_request):
        """刪除 S3 特定值區的物件
        
        獲取用戶要刪除的物件名稱
        使用 S3Dao 刪除用戶指定的物件
        """
        object_name = data_request.form["object_name"]
        return S3Dao.delete_object(bucket_name, object_name)
    
    @classmethod
    def get_all_object_names_from_bucket_and_directory(cls, bucket_name, prefix):
        """獲取所有物件的名稱

        使用 S3Dao 的方法 - 獲取特定值區的特定路徑的所有物件名稱
        回傳所有物件名稱的清單
        """
        file_list = S3Dao.get_all_object_names_by_bucket_name_and_directory(bucket_name, prefix)
        
        return jsonify(file_list)