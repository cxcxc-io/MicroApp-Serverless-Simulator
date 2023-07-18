import sys
sys.path.append('/home/coder/project')
from controllers.controller import Controller
from flask import Flask
import pytest

# 創建一個 Flask 應用程式實例
app = Flask(__name__)


def test_check_localstack_connection():
    """測試函式，檢查是否成功連線到 LocalStack"""
    response = Controller.check_localstack_connection()
    # 上述程式碼為測試函式，對相應功能進行測試並進行斷言檢查，確保程式的正確性和預期結果。
    assert response == "成功連線到 LocalStack！"

def test_get_all_object_names_from_bucket_and_directorya():
    """測試函式，從指定的存儲桶和目錄中獲取所有物件名稱"""
    with app.test_request_context():
        response = Controller.get_all_object_names_from_bucket_and_directory("cxcxc", "")
    print(response.json)
    assert type(response.json) == list