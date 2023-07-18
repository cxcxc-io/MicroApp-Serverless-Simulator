''' 需要在 tests/ 資料夾下執行 pytest'''

import boto3
import json
from io import BytesIO
import os
import sys
sys.path.append('/home/coder/project')
from daos.s3_dao import S3Dao
# from ..daos.s3_dao import S3Dao


def test_check_s3_connection():
    """測試 S3 物件的連線"""
    response = S3Dao.check_s3_connection()
    # 程式碼為測試函式，對 S3 相關功能進行測試並進行斷言檢查，確保程式的正確性和預期結果
    assert response == "成功連線到 S3"

def test_create_bucket():
    """測試函式，創建 S3 存儲桶"""
    response = S3Dao.create_bucket("cxcxc")
    assert response == True

def test_upload_bytes():
    """測試函式，上傳位元組到 S3"""
    filename = "123.txt"
    # 檢查檔案是否存在
    if not os.path.exists(filename):
        # 如果檔案不存在，則建立它並寫入 "testfile"
        with open(filename, 'w') as f:
            f.write("testfile")
    with open('123.txt', 'rb') as file:
        file_content = file.read()
        response = S3Dao.upload_bytes("cxcxc", "123.txt", 
            BytesIO(file_content)
        )
    
    assert response == True
    os.remove("123.txt")

def test_download_file():
    """測試函式，從 S3 下載檔案"""
    response = S3Dao.download_file("cxcxc", "123.txt", "abc.txt")
    os.remove("abc.txt")
    assert response == True

def test_update_object():
    """測試函式，更新 S3 中的物件"""
    filename = "xxx.txt"
    # 檢查檔案是否存在
    if not os.path.exists(filename):
        # 如果檔案不存在，則建立它並寫入 "testfile"
        with open(filename, 'w') as f:
            f.write("updatefile")
    with open('xxx.txt', 'rb') as file:
        file_content = file.read()
        response = S3Dao.update_object("cxcxc", "123.txt", 
            BytesIO(file_content)
        )
    os.remove("xxx.txt")
    assert response == True

def test_get_all_object_names_by_bucket_name_and_directory():
    """測試函式，獲取指定存儲桶和目錄下的所有物件名稱"""
    response = S3Dao.get_all_object_names_by_bucket_name_and_directory("cxcxc", "")
    assert "123.txt" in response


def test_delete_object():
    """測試函式，刪除 S3 中的物件"""
    response = S3Dao.delete_object("cxcxc", "123.txt")
    assert response == '刪除成功'