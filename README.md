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
  <img width="1439" alt="Image" src="https://github.com/user-attachments/assets/c3677828-944c-44a7-a94f-3e733f5f8458" />

- 7日間のログ表示機能: `http://<起動したIP>:5000`
<img width="1437" alt="Image" src="https://github.com/user-attachments/assets/525c47a3-7ad1-4b31-a660-e1a6dfc4348d" />


Citations:
[1] https://github.com/Amenbo1219/NGMD-HOST
