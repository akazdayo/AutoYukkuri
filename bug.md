# 既知のバグ
確認はしていますが、修正出来ていないバグの一覧です。

## 一部ファイルを実行した際特定の条件下でクラッシュする
large-v3と話者認識を併用した状態で、
少し大きめのファイルを入力した際、クラッシュすることがあります。

## 一部キャラクターが正常に動作しない
一部のキャラクターが正常に動作しないことがあります。
大抵の場合、[project.json](https://github.com/akazdayo/AutoYukkuri/tree/main#projectjson%E3%81%AE%E6%9B%B8%E3%81%8D%E6%8F%9B%E3%81%88%E6%96%B9)と[items.json](https://github.com/akazdayo/AutoYukkuri/tree/main#itemsjson%E3%81%AE%E6%9B%B8%E3%81%8D%E6%8F%9B%E3%81%88%E6%96%B9)が正しく書き換えられていないことによって、発生します。

## Numpy is not available
Powershellで`pip install numpy==1.26.4`を実行してください。

## Failed to import pytorch fbgemm.dll or one of its dependencies is missing
依存しているパッケージのバグです。  
私は[このスレッド](https://discuss.pytorch.org/t/failed-to-import-pytorch-fbgemm-dll-or-one-of-its-dependencies-is-missing/201969/21)の方法で直りました。

## よくわからない警告が沢山出る
警告は無視しても問題ありません。動いていればOKです！  
もし、エラーが発生した場合は警告と共に[バグ報告](#バグ報告)をお願いします。


# バグ報告
バグを発見した場合は、[Issues](https://github.com/akazdayo/AutoYukkuri/issues)または、[Twitter](https://twitter.com/akazdayo)にて報告してください。
