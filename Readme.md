# 使用方式
1.查看 .env 設定是否成功 (若無依照指定環境進行設定，請編輯.env)
```
docker compose config
```

2.透過Docker-Compose啟動服務
```
docker compose up -d
```

3.瀏覽 localhost:8080 -> 打開Web版的VSCode介面 -> 輸入密碼 (依照docker-compose.yml中設定)

4.執行主程式
```
python3 app.py
```

5.執行測試程式 (在專案資料夾根層執行)
會自動跑 tests 內部資料夾中的所有 test_ 開頭的方法以進行測試
```
pytest -s -v
```

------------

# .env
LOCALSTACK_API_KEY={localstack-pro-api-key}
開發環境  `ENV=development`
生產環境  `ENV=production`