# 既知のバグ
確認はしていますが、修正出来ていないバグの一覧です。

## 一部ファイルを実行した際特定の条件下でクラッシュする
large-v3と話者認識を併用した状態で、  
少し多い目のファイルを入力した際、クラッシュすることがあります。

## 一部キャラクターが正常に動作しない
一部のキャラクターが正常に動作しないことがあります。  
大体の場合、[project.json](https://github.com/akazdayo/AutoYukkuri/tree/main#projectjson%E3%81%AE%E6%9B%B8%E3%81%8D%E6%8F%9B%E3%81%88%E6%96%B9)と[items.json](https://github.com/akazdayo/AutoYukkuri/tree/main#itemsjson%E3%81%AE%E6%9B%B8%E3%81%8D%E6%8F%9B%E3%81%88%E6%96%B9)が書き換えられていないことによって、発生します。
