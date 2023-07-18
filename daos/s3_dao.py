import os
import boto3
import logging


class S3Dao:
    """對 S3 進行操作
    
    流程:
    1. 建立 boto3 客戶端物件
    2. 使用此客戶端物件進行功能操作
    """
    # 讀取環境變數
    env = os.getenv('ENV')

    if env == 'development':
        print('S3開發階段')
        # 連接到 LocalStack 的 S3
        s3 = boto3.client(
            's3',
            endpoint_url='http://localstack:4566',
            region_name='us-east-1',  
            aws_access_key_id='test',
            aws_secret_access_key='test',
        )
    elif env == 'production':
        # 連接到 AWS 生產環境的 S3
        # 注意：請確保在此環境下，AWS 的訪問金鑰和秘密金鑰已通過其他方式設定（例如，透過 AWS CLI 或環境變數）
        s3 = boto3.client('s3', region_name='ap-northeast-1') 
    
    @classmethod
    def check_s3_connection(cls):
        """測試是否成功連線
        
        流程:
        1. 使用 s3 物件的列出值區的方法
        2. 若成功列出, 回傳「成功連線到 S3」
        3. 若報出錯誤, 回傳「無法連線到 S3」
        """
        # 測試是否成功連線
        try:
            response = cls.s3.list_buckets()["Buckets"]
            print(f"值區清單: {response}")
            print("成功連線到 S3")
            return "成功連線到 S3"
        except Exception as e:
            print("無法連線到 S3", str(e))
            return "無法連線到 S3" + str(e)
    
    # 新增值區
    @classmethod
    def create_bucket(cls, bucket_name, region=None):
        """創建 S3 值區
        
        使用 s3 物件創建值區, 並傳入要創建的桶子名稱
        若報出錯誤, 回傳 False
        若成功, 最後回傳 True
        """
        import sys
        sys.path.append('..')
        from app import app
        try:

            if cls.env == 'development':
                cls.s3.create_bucket(Bucket=bucket_name)
            else:
                cls.s3.create_bucket(Bucket=bucket_name, 
    CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-1'},
    )



            app.logger.info("創建值區成功")
        except Exception as e:
            print(e)
            app.logger.info("創建值區失敗"+str(e))
            return False

        return True

    # 在特定值區新增物件
    @classmethod
    def upload_bytes(cls, bucket_name, object_name, data):
        """上傳 S3 物件到特定值區
        
        流程: 
        1. 使用 s3 物件的上傳物件方法, 傳入桶子名稱、物件名稱與物件 byte
        2. 若出錯, 回傳 False
        3. 若成功, 最後還傳 True
        """
        try:
            # 將 Bytes 資料寫入 S3 物件
            cls.s3.put_object(Bucket=bucket_name, Key=object_name, Body=data)
        except Exception as e:
            print(e)
            return False
        return True

    # 查詢、獲取物件
    @classmethod
    def download_file(cls, bucket_name, object_name, file_name):
        """下載檔案至程式碼所在的專案資料夾
        
        流程:
        1. 使用 S3 物件的下載方法, 傳入值區名稱、物件名稱與下載的路徑名稱
        2. 若有出錯, 回傳 False
        3. 若成功, 最後回傳 True
        """
        try:
            cls.s3.download_file(Bucket=bucket_name, Key=object_name, Filename=file_name)
        except Exception as e:
            print(e)
            return False

        return True

    # 更新物件
    @classmethod
    def update_object(cls, bucket_name, object_name, data):
        """更新 S3 物件
        
        流程:
        1. 使用 S3 物件的 head_object 方法, 傳入值區名稱與物件名稱
        2. 確認物件是否存在
        存在, 更新物件, 回傳結果
        不存在, 回傳 False
        """
        try:
            response = cls.s3.head_object(Bucket=bucket_name, Key=object_name)
            print(response)
            print(f"{object_name} 物件存在")
            return cls.upload_bytes(bucket_name, object_name, data)
        except Exception as e:
            print(f"{object_name} 物件不存在")
            return False

    # 刪除物件
    @classmethod
    def delete_object(cls, bucket_name, object_name):
        """刪除 S3 特定值區的物件
        
        流程: 
        1. 使用 S3 物件的刪除方法並傳入值區名稱與物件名稱
        2. 回傳「刪除成功」
        """
        
        # 刪除物件
        response = cls.s3.delete_object(Bucket=bucket_name, Key=object_name)
        return "刪除成功" 

    # 列出指定值區與路徑下的所有物件
    @classmethod
    def get_all_object_names_by_bucket_name_and_directory(cls, bucket_name, prefix):
        """獲取所有物件的名稱

        流程:
        1. 使用 S3物件的 list_objects_v2 方法並傳入桶子名稱與路徑開頭
        2. 若成功, 取出所有路徑名稱, 並做成清單
        3. 若失敗, 回傳 []
        """
        try:
            response = cls.s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        except :
            return []
        if 'Contents' not in response:
            return []
        return [content['Key'] for content in response['Contents']]
