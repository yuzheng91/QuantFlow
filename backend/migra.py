import pandas as pd
from sqlalchemy import create_engine
import sqlite3

# SQLite 舊資料
sqlite_conn = sqlite3.connect("db.sqlite3")
sqlite_cursor = sqlite_conn.cursor()

# MySQL 新資料庫
mysql_engine = create_engine("mysql+pymysql://root:ad20020418@127.0.0.1:3306/mydb")

# 抓所有資料表
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in sqlite_cursor.fetchall()]

for table in tables:
    print(f"📤 搬資料表：{table}")
    try:
        df = pd.read_sql(f"SELECT * FROM {table}", sqlite_conn)

        # 若表格為空，就跳過
        if df.empty:
            print(f"⚠️ 表 {table} 是空的，跳過")
            continue

        # 檢查主鍵欄位（如果沒有 id，就不要用 index=False）
        if 'id' in df.columns and df['id'].isnull().any():
            df = df[df['id'].notnull()]  # 移除 id 為 None 的 row

        df.to_sql(table, mysql_engine, if_exists='append', index=False)
        print(f"✅ 表 {table} 搬成功")
    except Exception as e:
        print(f"❌ 表 {table} 搬失敗：{e}")

sqlite_conn.close()
