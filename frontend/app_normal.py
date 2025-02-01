from flask import Flask, render_template
import requests
from datetime import datetime
import pytz
from collections import defaultdict

app = Flask(__name__)

API_URL = "http://api:8000/metrics"

# 時間をJSTに変換する関数
def format_timestamp(timestamp):
    
    #date_str = "2025-01-30T14:39:31.433372"
    date_obj = datetime.fromisoformat(timestamp)
    return date_obj
    # timestampを整数に変換（文字列の場合）
    #timestamp = int(float(timestamp)) if isinstance(timestamp, str) else int(timestamp)
    
    #utc_time = datetime.utcfromtimestamp(timestamp)
    #jst = pytz.timezone('Asia/Tokyo')
    #utc_time = pytz.utc.localize(utc_time)  # UTCを認識させる
    #jst_time = utc_time.astimezone(jst)
    #return jst_time.strftime('%Y-%m-%d %H:%M:%S')

@app.route("/")
def index():
    try:
        response = requests.get(API_URL)
        data = response.json()
    except Exception as e:
        data = []
        print(f"Error fetching metrics: {e}")

    # ホスト名ごとの最新データを抽出
    latest_metrics = defaultdict(dict)

    # ホスト名ごとに最新データを選択
    for metric in data:
        hostname = metric['hostname']
        # 最新のデータを選ぶ
        if hostname not in latest_metrics or metric['timestamp'] > latest_metrics[hostname]['timestamp']:
            latest_metrics[hostname] = metric

    # 最新データだけのリストを作成
    latest_data = list(latest_metrics.values())

    # 各データにJSTの形式で時間をフォーマット
    for row in latest_data:
        row["timestamp"] = format_timestamp(row["timestamp"])

    return render_template("index.html", metrics=latest_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

