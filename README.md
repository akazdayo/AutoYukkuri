# Auto Yukkuri 
## 概要
あなたが生声で実況した動画から自動でYMM4プロジェクト(ゆっくり実況)を作成します。
```
生声実況動画
　　　　↘
　　　音声認識
　　　　↙
YMM4プロジェクト
　　　　↘
　　　微調整
　　　　↙
＿人人人人＿
＞　完成　＜
￣Y^Y^Y^Y^￣
```

### 変換前
https://github.com/akazdayo/AutoYukkuri/assets/82073147/0662fcf1-1f2e-4239-8b73-907cbbb6f424

### 変換後
https://github.com/akazdayo/AutoYukkuri/assets/82073147/1b4d91e8-2850-4f66-9513-94e279967d40

## 事前にインストールが必要なもの
| もの | バージョン |
|------|-----------|
|Python| 3.8 ~ 3.11|

## インストールと実行
[モデル一覧](https://github.com/openai/whisper#available-models-and-languages)  
精度が良くない場合はモデルを変更してみてください。
### コマンドライン
1. ``git clone https://github.com/akazdayo/auto-yukkuri.git``
2. ``pip install -r requirements.txt``
3. defaultフォルダに含まれるパスをすべてご自身のものに書き換えてください。
4. ``python generate.py ファイルパス モデル(small推奨)``

### Zipファイル
1. GithubのReleasesからZipをインストールする
2. フォルダを解凍
3. 解凍したフォルダをコマンドライン等で開く
4. ``pip install -r requirements.txt``を実行する
5. defaultフォルダに含まれるパスをすべてご自身のものに書き換えてください。
6. ``python generate.py ファイルパス モデル(small推奨)``を実行する
