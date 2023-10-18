"""
プロジェクトを合成できます。
例えば、霊夢と魔理沙で別の音声ファイルを使用する場合など
(3つ以上のプロジェクトの合成はできません)
"""

import json


# 読み込み
def read(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


# 書き込み
def save(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


file_1 = read("./export/kaiwa.ymmp")
file_2 = read("./export/kaiwa2.ymmp")

del file_2["Timeline"]["Items"][-1]

for i in range(len(file_2)):
    file_2["Timeline"]["Items"][i]["Layer"] = 1

file_1["Timeline"]["Items"].extend(file_2["Timeline"]["Items"])

save("./export/Merge.ymmp", file_1)
