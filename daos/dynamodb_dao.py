import os
import boto3


class DynamoDBDao:
    """對 localstack 的 DynamoDB 服務進行操作"""
    
    
    # 讀取環境變數
    env = os.getenv('ENV')

    if env == 'development':
    # 建立 DynamoDB 客戶端
    # 連接到 LocalStack
        dynamodb = boto3.client(
            'dynamodb',
            endpoint_url='http://localstack:4566',
            region_name='us-east-1',  
            aws_access_key_id='test',
            aws_secret_access_key='test',
        )
    elif env == 'production':
        # 連接到 AWS 生產環境
        # 注意：請確保在此環境下，AWS 的訪問金鑰和秘密金鑰已通過其他方式設定（例如，透過 AWS CLI 或環境變數）
        dynamodb = boto3.client('dynamodb', region_name='ap-northeast-1')

    @classmethod
    def check_dynamodb(cls):
        """確認讀取到 dynamodb
        
        使用 boto3 的客戶端物件, 列出所有表格
        若無法列出, 回傳「False」(bool)
        若列出，回傳「OK」(str)
        """

        # 建立 DynamoDB 客戶端
        dynamodb = boto3.client(
            'dynamodb',
            endpoint_url='http://localstack:4566',
            region_name='us-east-1',
            aws_access_key_id='test',
            aws_secret_access_key='test',
        )

        # 列出所有 DynamoDB 表格
        response = dynamodb.list_tables()
        if response:
            print("已連接到 LocalStack 的 DynamoDB 服務，並列出：")
            print(response)
            return "OK"
        else:
            print("無法連接到 LocalStack 的 DynamoDB 服務。")
            print(response)
            return False
        
    @classmethod
    def create_table(cls,table_name):
        """新增一個表格
        
        流程: 
        1. 定義表格的欄位名稱與屬性
        2. 定義表格的主鍵
        3. 設定表格讀寫的吞吐量
        4. 建立表格
        5. 判定表格是否建立成功, 
        若成功, 回傳 OK
        若失敗, 回傳 False(bool)
        """ 
        # 表格欄位屬性定義
        attribute_definitions = [
            {
                'AttributeName': 'ID',
                'AttributeType': 'S'
            },
        ]
        # 定義表格的主鍵。主鍵可以包括一個分區鍵和一個可選的排序鍵。
        key_schema = [
            {
                'AttributeName': 'ID',
                'KeyType': 'HASH' # 'HASH' 表示這是分區鍵
            },
        ]
        # 設定預期的讀寫容量。讀寫容量表示每秒能處理的讀/寫數量。
        provisioned_throughput = {
            'ReadCapacityUnits': 5, # 每秒的讀取次數
            'WriteCapacityUnits': 5 # 每秒的寫入次數
        }
        # 建立表格
        response = cls.dynamodb.create_table(
            TableName=table_name,
            AttributeDefinitions=attribute_definitions,
            KeySchema=key_schema,
            ProvisionedThroughput=provisioned_throughput
        )
        # 檢查建立表格的回應
        if response['TableDescription']['TableStatus'] == 'ACTIVE':
            print(f"已成功建立 DynamoDB 表格：{table_name}")
            return 'OK'
        else:
            print(f"無法建立 DynamoDB 表格：{table_name}")
            return False
    
    @classmethod
    def insert_into_dynamodb(cls, table_name, data):
        """新增資料到指定的表格
        
        流程:
        1. 將 data 轉換成 dynamodb 上傳表格資料的格式
        2. 上傳資料
        3. 上傳成功, 回傳 「OK」(str)
        4. 上傳失敗, 回傳 「False」(bool)
        """
        # 創建 DynamoDB 客戶端
        dynamodb_data ={k:{'S':v} for k, v in data.items()}

        try:
            # 新增資料
            response = cls.dynamodb.put_item(TableName = table_name, Item=dynamodb_data)
            print("新增資料成功")
            return 'OK'
        except Exception as e:
            print("新增資料出錯")
            print(e)
            return False
    
    @classmethod
    def scan_dynamodb(cls, table_name):
        """查詢特定表格
        
        流程:
        1. 使用 dynamodb 物件讀取特調表格
        2. 取出回應的 items 欄位
        3. 打印出每筆資料驗證
        4. 將資料以字串型式回傳
        5. 若失敗，則告知錯誤訊息，並回傳 None
        """
        try:
            # 掃描資料
            response = cls.dynamodb.scan(TableName=table_name)
            items = response['Items']
            print("items" + str(items))
            print("掃描資料成功")
            _list = []
            for item in items:
                print(item)
                _list.append(item)
            return str(_list)
        except Exception as e:
            print("掃描資料出錯")
            print(e)
            return None
        
    @classmethod
    def query_dynamodb(cls, table_name, id):
        """查詢特定表格的特定 id 資料
        
        流程:
        1. 設定特定 id 主鍵
        2. 用客戶端物件的 query 方法, 查詢特定表格的特定屬性欄位值
        3. 
        若查詢成功, 印出所有欄位
        若失敗, 告知「查詢資料出錯」
        """
        key_condition = f'ID = :id'
        _value = f'{id}'
        try:
            # 查詢單筆資料
            response = cls.dynamodb.query(
                TableName=table_name,
                KeyConditionExpression=key_condition,
                ExpressionAttributeValues={
                    ':id': {'S': _value} # 根據實際情況修改
                }
            )
            items = response['Items']
            print("查詢資料成功")
            _list = []
            for item in items:
                print(item)
                _list.append(item)
                return _list
        except Exception as e:
            print("查詢資料出錯")
            print(e)
            return None
    
    @classmethod
    def update_dynamodb_item(cls, table_name, new_data):
        """更新特定表格的特定資料
        
        流程:
        1. 建立表達式屬性名稱和表達式屬性值
        2. 取出要更新的資料的 ID
        3. 將 ID 欄刪掉，避免寫入
        4. 取出其它的值
        5. 建立更新表達式
        6. 更新資料
        """
        
        # 建立表達式屬性名稱和表達式屬性值
        expression_attribute_names = {}
        expression_attribute_values = {}
        update_expressions = []

        id = new_data.get("ID", "")
        del new_data["ID"]
        for key, value in new_data.items():
            attribute_name_placeholder = '#' + key
            attribute_value_placeholder = ':' + key

            expression_attribute_names[attribute_name_placeholder] = key
            expression_attribute_values[attribute_value_placeholder] = {'S': value}

            update_expressions.append(f'{attribute_name_placeholder} = {attribute_value_placeholder}')

        # 建立更新表達式
        update_expression = 'SET ' + ', '.join(update_expressions)
        print("id: " + id)
        
        response = cls.dynamodb.update_item(
            TableName=table_name,
            Key={'ID': {"S": str(id)}},
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            UpdateExpression=update_expression,
            ReturnValues="UPDATED_NEW"
        )
        return response
    
    @classmethod
    def soft_delete_item(cls,table_name, new_data):
        """軟刪除資料
        
        流程:
        1. 取出要軟刪除的 ID
        2. 刪除該ID
        3. 將該 ID 資料更新 is_deleted=true
        """

        id = new_data.get("ID", "")
        # name = new_data.get("Name", "")
        del new_data["ID"]
        # del new_data["Name"]

        # 將 is_deleted 屬性設為 True
        response = cls.dynamodb.update_item(
            TableName=table_name,
            # Key={'ID': {"S": str(id)}, 'Name':{"S": name}},
            Key={'ID': {"S": str(id)}},
            UpdateExpression="SET is_deleted = :true",
            ExpressionAttributeValues={
                ':true': {'BOOL': True}
            },
            ReturnValues="UPDATED_NEW"
        )
        return response
    
    @classmethod
    def delete_item(cls, table_name, id):
        """直接刪除資料

        流程: 
        1. 取出要刪除的資料的 ID
        2. 使用 dynamodb 物件直接刪除該筆 ID 的資料
        3. 回傳刪除的 response
        """
        key = {'ID': {'S': id}}
        response = cls.dynamodb.delete_item(
            TableName=table_name,
            Key=key  # 主鍵，必須是一個字典，例如：{'ID': {'S': '123'}}
        )
    
        return response