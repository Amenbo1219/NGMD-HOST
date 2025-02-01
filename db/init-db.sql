-- データベース作成（存在しない場合のみ）
CREATE DATABASE monitoring;

-- `monitoring` データベースを使用
\c monitoring;

-- `system_metrics` テーブルを作成
CREATE TABLE system_metrics (
    id SERIAL PRIMARY KEY,
    hostname TEXT NOT NULL,
    cpu_usage FLOAT NOT NULL,
    memory_usage BIGINT NOT NULL,
    total_memory BIGINT NOT NULL,
    gpu_name TEXT,  -- GPUの製品名を追加
    gpu_usage FLOAT,
    gpu_memory_usage BIGINT,
    gpu_total_memory BIGINT,
    runner TEXT ,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


