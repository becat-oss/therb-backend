# therb-backend. 
THERB-backendはTHERB(HASP)のシミュレーション結果を分析、管理するためのwebアプリを構成するAPIサーバーです。
[THERB-UI](https://github.com/becat-oss/therb-UI)をフロントエンドとして、THERB-webを構成します。  
THERB-webには以下のような機能が実装される予定です。

1. THERB-GHからアップロードされた入力データを元にシミュレーションを回し、結果を抽出、データベースに保存.  
2. データベースに保存されているデータをグラフ表示してくれるUI  
3. データを外部と連携するためのAPIインターフェース  

## 機能説明  
3. データを外部と連携するためのAPIインターフェース  

## 環境設定(Windows PCの場合）    
1. command promptを開き、ディレクトリ移動  
2. pipenv shellを叩いて、仮想環境を構築  
3. 以下のコマンドを叩く  
```
set FLASK_APP=run
flask run
```

## 使い方   
1. マテリアル(Material)情報を取得、保存するためのエンドポイント  
http://localhost:5000/materials  

2. 壁体構成(Construction)情報を取得、保存するためのエンドポイント    
http://localhost:5000/constructions   

3. Envelope(Constructionの総体)情報を取得するためのエンドポイント    
http://localhost:5000/results/envelopes    

