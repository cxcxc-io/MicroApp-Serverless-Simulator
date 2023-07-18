''' 需要在 tests/ 資料夾下執行 pytest'''
import sys
sys.path.append('/home/coder/project')
from daos.dynamodb_dao import DynamoDBDao
import boto3
import json

# 建立 dynamodb 物件
dynamodb = boto3.client(
        'dynamodb',
        endpoint_url='http://localstack:4566',
        region_name='us-east-1',
        aws_access_key_id='test',
        aws_secret_access_key='test',
    )


def test_check_dynamodb():
    """測試函式，檢查是否成功連線到 DynamoDB"""
    response = DynamoDBDao.check_dynamodb()
    # 程式碼為測試函式，對 DynamoDB 相關功能進行測試並進行斷言檢查，確保程式的正確性和預期結果。
    assert response == "OK"

def test_create_table():
    """測試函式，創建 DynamoDB 資料表"""
    response = DynamoDBDao.create_table("cxcxc")
    dynamodb.delete_table(TableName="cxcxc")
    assert response == "OK"


def test_insert_into_dynamodb():
    """測試函式，將資料插入到 DynamoDB"""
    DynamoDBDao.create_table("cxcxc")
    response = DynamoDBDao.insert_into_dynamodb("cxcxc",{
            "ID": "12321",
            "Name": "Tom"
    })
    dynamodb.delete_table(TableName="cxcxc")
    assert response == 'OK'

def test_scan_dynamodb():
    """測試函式，從 DynamoDB 掃描資料"""
    DynamoDBDao.create_table("cxcxc")
    response = DynamoDBDao.scan_dynamodb("cxcxc")
    dynamodb.delete_table(TableName="cxcxc")
    assert response == '[]'

def test_query_dynamodb():
    """測試函式，從 DynamoDB 查詢資料"""
    DynamoDBDao.create_table("cxcxc")
    DynamoDBDao.insert_into_dynamodb("cxcxc",{
            "ID": "12321",
            "Name": "Tom"
    })
    response = DynamoDBDao.query_dynamodb("cxcxc", "12321")
    dynamodb.delete_table(TableName="cxcxc")
    assert response ==  [{'ID': {'S': '12321'}, 'Name': {'S': 'Tom'}}]

def test_update_dynamodb_item():
    """測試函式，更新 DynamoDB 中的資料項目"""
    DynamoDBDao.create_table("cxcxc")
    DynamoDBDao.insert_into_dynamodb("cxcxc",{
            "ID": "12321",
            "Name": "Tom"
    })
    response = DynamoDBDao.update_dynamodb_item("cxcxc", {
            "ID": "12321",
            "Name": "Amy"
    })
    dynamodb.delete_table(TableName="cxcxc")
    assert response["Attributes"]["Name"]["S"] == "Amy"

def test_soft_delete_item():
    """測試函式，軟刪除 DynamoDB 中的資料項目"""
    DynamoDBDao.create_table("cxcxc")
    DynamoDBDao.insert_into_dynamodb("cxcxc",{
            "ID": "12321",
            "Name": "Tom"
    })
    DynamoDBDao.soft_delete_item("cxcxc",{
        "ID": "12321",
    })
    query = DynamoDBDao.query_dynamodb("cxcxc", "12321")
    dynamodb.delete_table(TableName="cxcxc")
    assert query == [{'is_deleted': {'BOOL': True}, 'ID': {'S': '12321'}, 'Name': {'S': 'Tom'}}]

def test_delete_item():
    """測試函式，刪除 DynamoDB 中的資料項目"""
    DynamoDBDao.create_table("cxcxc")
    DynamoDBDao.insert_into_dynamodb("cxcxc",{
            "ID": "12321",
            "Name": "Tom"
    })
    DynamoDBDao.delete_item("cxcxc", "12321")
    query = DynamoDBDao.query_dynamodb("cxcxc", "12321")
    dynamodb.delete_table(TableName="cxcxc")
    assert query == None
