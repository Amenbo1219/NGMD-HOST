from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from datetime import datetime
import pytz
import psycopg2
import os

# FastAPI のインスタンス
app = FastAPI()

# PostgreSQL の接続情報
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "monitoring")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

# PostgreSQL 接続関数
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )

# リクエストデータのスキーマ
class Metrics(BaseModel):
    hostname: str
    cpu_usage: float
    memory_usage: int
    total_memory: int
    gpu_name: str = None
    gpu_usage: float = None
    gpu_memory_usage: int = None
    gpu_total_memory: int = None
    runner: str
    ip: str = None
# 監視データを受信・保存
@app.post("/monitor")
def receive_metrics(metrics: Metrics, request: Request):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # HostヘッダーのIPを取得
        host_header = request.headers.get("host", "")
        client_ip = host_header.split(":")[0] if ":" in host_header else host_header  # ポートが含まれていたらIPだけ取得

        # クライアントが IP を送信しない場合、取得した IP を使用
        ip_address = metrics.ip if metrics.ip else client_ip

        # JST での現在時刻を取得
        jst_time = datetime.now(pytz.UTC).astimezone(pytz.timezone('Asia/Tokyo'))

        cur.execute("""
            INSERT INTO system_metrics (hostname, cpu_usage, memory_usage, total_memory,
                                        gpu_name, gpu_usage, gpu_memory_usage, gpu_total_memory, runner, ip, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (metrics.hostname, metrics.cpu_usage, metrics.memory_usage, metrics.total_memory,
              metrics.gpu_name, metrics.gpu_usage, metrics.gpu_memory_usage, metrics.gpu_total_memory,
              metrics.runner, ip_address, jst_time))

        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Metrics received", "client_ip": client_ip}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# 最新の監視データを取得
@app.get("/metrics")
def get_latest_metrics():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
        SELECT  hostname, cpu_usage, memory_usage, total_memory, gpu_name, gpu_usage,
                   gpu_memory_usage, gpu_total_memory, runner, ip, timestamp
        FROM system_metrics
        WHERE timestamp >= NOW() - INTERVAL '7 days'
        ORDER BY hostname, timestamp DESC
        """)
        data = cur.fetchall()
        cur.close()
        conn.close()

        # JST に変換
        jst_timezone = pytz.timezone('Asia/Tokyo')
        return [{"hostname": row[0], "cpu_usage": row[1], "memory_usage": row[2],
                 "total_memory": row[3], "gpu_name": row[4], "gpu_usage": row[5],
                 "gpu_memory_usage": row[6], "gpu_total_memory": row[7],
                 "runner": row[8],"ip":row[9], "timestamp": row[10].astimezone(jst_timezone).strftime('%Y-%m-%d %H:%M:%S')}
                for row in data]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/history")
def get_history():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
        SELECT hostname, cpu_usage, memory_usage, total_memory, gpu_name, gpu_usage,
               gpu_memory_usage, gpu_total_memory, runner, ip, timestamp
        FROM system_metrics
        WHERE timestamp >= NOW() - INTERVAL '7 days'
        ORDER BY hostname, timestamp
        """)
        data = cur.fetchall()
        cur.close()
        conn.close()

        jst_timezone = pytz.timezone("Asia/Tokyo")
        return [{"hostname": row[0], "cpu_usage": row[1], "memory_usage": row[2],
                 "total_memory": row[3], "gpu_name": row[4], "gpu_usage": row[5],
                 "gpu_memory_usage": row[6], "gpu_total_memory": row[7],
                 "runner": row[8], "ip": row[9], "timestamp": row[10].astimezone(jst_timezone).strftime("%Y-%m-%d %H:%M:%S")}
                for row in data]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

