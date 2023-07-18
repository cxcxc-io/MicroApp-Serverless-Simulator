# 第一階段：建構環境與測試
FROM python:3.11

# 指定環境
ARG ENV

# 切換至指定工作目錄
WORKDIR /app
ENV PYTHONPATH=/app

# 安裝相依套件
COPY requirements.txt .
RUN pip install -r requirements.txt

# 複製程式碼到容器中
COPY . .

# 執行 Pytest 測試
RUN pytest -s -v

# 執行程式
CMD ["python3", "app.py"]