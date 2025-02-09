from flask import Flask, render_template, Response
import requests
import csv
from datetime import datetime
import pytz
from collections import defaultdict
import io

app = Flask(__name__)

API_URL = "http://api:8000/metrics"
HISTORY_API_URL = "http://api:8000/history"

# JST に変換する関数
def format_timestamp(timestamp):
    date_obj = datetime.fromisoformat(timestamp)
    jst = pytz.timezone('Asia/Tokyo')
    return date_obj.astimezone(jst).strftime('%Y-%m-%d %H:%M:%S')

@app.route("/")
def index():
    try:
        response = requests.get(API_URL)
        data = response.json()
    except Exception as e:
        data = []
        print(f"Error fetching metrics: {e}")

    latest_metrics = defaultdict(dict)
    for metric in data:
        hostname = metric["hostname"]
        if hostname not in latest_metrics or metric["timestamp"] > latest_metrics[hostname]["timestamp"]:
            latest_metrics[hostname] = metric

    latest_data = list(latest_metrics.values())

    for row in latest_data:
        row["timestamp"] = format_timestamp(row["timestamp"])

    return render_template("index.html", metrics=latest_data,refresh_interval=10,static_url_path='/static', datetime=datetime)


@app.route("/history")
def history():
    try:
        response = requests.get(HISTORY_API_URL)
        data = response.json()
    except Exception as e:
        data = []
        print(f"Error fetching history: {e}")

    formatted_data = defaultdict(list)
    for entry in data:
        entry["timestamp"] = format_timestamp(entry["timestamp"])
        formatted_data[entry["hostname"]].append(entry)

    # 各ホストについて、タイムスタンプ順にソートした上で、
    # 件数が20件を超える場合は等間隔に20点抽出する
    for host, records in formatted_data.items():
        # タイムスタンプ順に昇順でソート
        records.sort(key=lambda x: x["timestamp"])
        if len(records) > 20:
            n = len(records)
            # 20点抽出するための比率
            step = n / 20
            sampled = [records[int(i * step)] for i in range(20)]
            formatted_data[host] = sampled

    return render_template("history.html", history_data=formatted_data, static_url_path='/static')

@app.route("/history/download")
def download_history():
    try:
        response = requests.get(HISTORY_API_URL)
        data = response.json()
    except Exception as e:
        return Response("Error fetching history", status=500)

    output = io.StringIO()
    csv_writer = csv.writer(output)
    csv_writer.writerow(["hostname", "timestamp", "cpu_usage", "memory_usage", "gpu_usage", "gpu_memory_usage", "runner", "ip"])

    for row in data:
        csv_writer.writerow([
            row["hostname"], row["timestamp"], row["cpu_usage"],
            row["memory_usage"], row["gpu_usage"], row["gpu_memory_usage"], row["runner"], row["ip"]
        ])

    output.seek(0)
    return Response(output, mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=history.csv"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
