# NGMD-HOST: Nvidia GPU Monitoring Dashboard API Host

## 概要

NGMD-HOSTは、NvidiaのGPUモニタリングダッシュボード用のAPIホストです。このツールを使用することで、GPUの使用状況を効率的に監視し、データを視覚化することができます。

## クライアント

クライアントアプリケーションは別リポジトリで提供されています：
[NGMD-client](https://github.com/Amenbo1219/NGMD-client)

このクライアントを使用することで、NGMD-HOSTと連携してGPUモニタリングダッシュボードを完全に機能させることができます。

## セットアップと起動

### ビルド
```
docker-compose build
```

### 初期起動
データベースの初期化が必要です：
```
bash mkdb.sh
```

### 通常起動
```
docker-compose up -d
```

## 機能確認

リクエストが正しく表示されるか確認するには：
```
bash req.sh
```

## アクセス

- モニタリング機能: `http://<起動したIP>:5000`
- 7日間のログ表示機能: `http://<起動したIP>:5000`



Citations:
[1] https://github.com/Amenbo1219/NGMD-HOST
