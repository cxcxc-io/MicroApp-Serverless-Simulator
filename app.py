from flask import Flask, request, send_file
from flask_cors import CORS

import logging
from controllers.controller import Controller

# 創建了一個 Flask 應用程式物件，並指定了靜態檔案的 URL 路徑和儲存位置。
app = Flask(__name__, static_url_path="/", static_folder="web")
# 啟用了跨來源資源共享 (CORS)，允許從其他來源的網頁進行請求。
CORS(app)
app.logger.setLevel(logging.INFO)


# 透過 / 目錄, 避免以往資源原先抓取資源的 /index.html 重整頁面後卻找不到網頁
@app.route("/")
def open_index_html():
    """當用戶直接訪問 /web 目錄，直接回傳網頁"""
    return send_file('web/index.html')

# 建立了一個路由（route），將根目錄 '/' 對應到一個名為 hello() 的函式。
@app.route('/dummy')
def hello():
    """測試 flask api, app 程式是否正常運作"""
    return 'Hello, World!'
 
@app.route('/localstack-connection-status')
def check_connection():
    """確認是否接通 localstack"""
    return Controller.check_localstack_connection()


@app.route('/dynamodb-connection-status')
def check_dynamodb():
    """確認是否接通 dynamodb"""
    return Controller.check_dynamodb_connection()


@app.route('/new-table/<table_name>', methods=["POST"])
def create_table(table_name):
    """建立新的表格"""
    return Controller.create_table(table_name)

@app.route('/table/<table_name>', methods=["POST"])
def insert_data(table_name):
    """在指定表格插入新的值
    
    request data 範例:
    body -> raw data -> JSON
    {
    "ID": "12321",
    "Name": "Tom"
    }
    """
    return Controller.insert_data_into_dynamodb(table_name, request)

@app.route('/table/<table_name>', methods=["GET"])
def scan_table(table_name):
    """獲取指定表格的所有資料"""
    return Controller.scan_dynamodb(table_name)

@app.route('/table/<table_name>/<id>', methods=["GET"])
def query_data(table_name, id):
    """查詢特定表格的特定 id"""
    return Controller.query_db(table_name, id)

@app.route('/table/<table_name>', methods=["PUT"])
def update_dynamodb_data(table_name):
    """更新特定表格的資料"""
    return Controller.update_dynamodb_data(table_name, request)

@app.route('/table/<table_name>/deletion', methods=["PUT"])
def soft_delete(table_name):
    """軟刪除"""
    return Controller.soft_delete_item(table_name, request)

@app.route('/table/<table_name>/<id>', methods=["DELETE"])
def delete_item(table_name, id):
    """硬刪除"""
    return Controller.delete_item(table_name, id)

@app.route('/s3-connection-status')
def check_s3():
    """確認是否接通 s3"""
    return Controller.check_s3_connection()

@app.route('/s3/bucket/<bucket_name>', methods=["POST"])
def create_s3_bucket(bucket_name):
    """建立特定值區"""
    return Controller.create_s3_bucket(bucket_name)

@app.route('/s3/bucket/<bucket_name>/new-object', methods=["POST"])
def upload_object(bucket_name):
    """在特定值區上傳物件"""
    return Controller.upload_s3_object(bucket_name, request)

@app.route('/s3/bucket/<bucket_name>/object', methods=["GET"])
def download_file(bucket_name):
    """在特定值區下載物件"""
    return Controller.download_file(bucket_name, request)

@app.route('/s3/bucket/<bucket_name>/new-object', methods=["PUT"])
def update_object(bucket_name):
    """在特定值區更新物件"""
    return Controller.update_s3_object(bucket_name, request)

@app.route('/s3/bucket/<bucket_name>/object', methods=["DELETE"])
def delete_object(bucket_name):
    """在特定值區刪除物件"""
    return Controller.delete_s3_object(bucket_name, request)

@app.route('/list_objects', methods=['GET'])
def list_objects():
    """在特定值區指定特定路徑並列出該路徑的所有物件名稱的清單"""
    bucket_name = request.args.get('bucket')
    prefix = request.args.get('prefix')
    return Controller.get_all_object_names_from_bucket_and_directory(bucket_name, prefix)


if __name__ == '__main__':
    """
    檢查是否直接執行這個 Python 模組。
    如果是的話，它會啟動 Flask 應用程式的伺服器，並在所有網路介面上監聽連接請求。這使得 Flask 應用程式可以被從任何裝置或瀏覽器進行訪問。
    伺服器啟動後，會等待並處理傳入的請求，根據路由定義呼叫相應的函式。
    """
    app.run(host="0.0.0.0", debug=True)