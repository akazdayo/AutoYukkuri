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

声素材: 効果音ラボ

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
3. [project.jsonの書き換え方](#projectjsonの書き換え方)に沿って変更
4. [items.jsonの書き換え方](#itemsjsonの書き換え方)に沿って変更
5. ``python generate.py``

### ZIPファイル
1. 右上のCodeボタンからDownload ZIPを選択してダウンロード
2. ダウンロードしたZIPファイルを解凍
3. 解凍したフォルダをコマンドプロンプト等で開く
4. ``pip install -r requirements.txt``を実行する
5. [project.jsonの書き換え方](#projectjsonの書き換え方)に沿って変更
6. [items.jsonの書き換え方](#itemsjsonの書き換え方)に沿って変更
7. ``python generate.py``を実行する

### project.jsonの書き換え方
1. YMM4を起動する
2. 使用する予定のキャラクターの立ち絵すべてをタイムラインに配置する
3. defaultフォルダのproject.jsonに上書き保存する

### items.jsonの書き換え方
1. YMM4を起動する
2. 好きなキャラクターで一言だけ喋らせる
3. defaultフォルダのitems.jsonに上書き保存する
4. items.jsonを開く
5. TimelineのItemsのみを残し、それ以外を削除
6. VoiceCacheの中を空の文字列にする

以下の様になっていたら成功です。
```json
{
  "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
  "IsWaveformEnabled": false,
  "CharacterName": "ゆっくり魔理沙",
  "Serif": "こんばんは",
  "Decorations": [],
  "Hatsuon": "こんばんわ",
...
```

## アンインストール方法
フォルダを消しただけでは残骸ファイルが残ってしまうので、以下の方法で削除してください。
### 通常の削除
1. ``C:\Users\ユーザー名\.cache\whisper``を削除
2. このフォルダを削除する
### Pythonが不要な場合
1. ``C:\Users\ユーザー名\.cache\whisper``を削除
2. このフォルダを削除する
3. Pythonとpipを削除する方法を検索し、削除する