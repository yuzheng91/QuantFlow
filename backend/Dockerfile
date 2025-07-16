FROM python:3.13

# 安裝系統依賴（用 wheel 就不需要 build-essential）
RUN apt-get update && apt-get install -y wget curl && rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /app

# 安裝 numpy（先裝，因為 ta-lib 依賴 numpy）
RUN pip install --upgrade pip
RUN pip install numpy==2.3.1 --prefer-binary

# 下載並安裝預編譯的 ta-lib .whl（你也可以事先放到專案資料夾）
RUN wget https://github.com/chenin-wang/ta-lib-python-wheel/releases/download/v0.6.3/ta_lib-0.6.3-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
RUN pip install ta_lib-0.6.3-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

# 安裝你的其他 Python 依賴
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install cryptography

# 複製專案程式碼
COPY . /app


# 啟動 Django 伺服器（如需改為 gunicorn 可調整）
CMD ["python", "manage.py", "runserver", "0.0.0.0:8888"]



