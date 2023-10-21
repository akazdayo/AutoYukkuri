import whisper
import time
import budoux
from pykakasi import kakasi
import json
import re
import sys


# 読み込み
def read(path):
    with open(path, "r", encoding="utf-8-sig") as file:
        return json.load(file)


# 書き込み
def save(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# 数字変換
def convert_numbers(word):
    pattern = r"\d+"
    matches = re.findall(pattern, word)
    for match in matches:
        word = word.replace(match, f"<NUMK VAL={match}>")
    return word


# ひらがなに変換
def convert_hiragana(word):
    kks = kakasi()
    converted = kks.convert(word)
    result = ""
    for converted_word in converted:
        result += f"{converted_word['hira']}"
    return convert_numbers(result)


# 入力
args = sys.argv

# 初期化
parser = budoux.load_default_japanese_parser()
model = whisper.load_model(args[2])
default_items = read("./default/items.json")
default_project = read("./default/project.json")  # .copy()
chara = read("./default/chara.json")

# 処理
print("---変換開始---")
start = time.time()
result = model.transcribe(
    args[1],  # ファイルパス
    verbose=True,
    language="ja",
)
end = time.time()
print(f"---変換終了---\n変換時間{end-start}秒です。")


# 書き出し
items = []
for i, j in enumerate(result["segments"]):
    items.append(default_items.copy())
    items[i]["Serif"] = j["text"].replace("!", "")
    items[i]["Hatsuon"] = convert_hiragana(j["text"])
    items[i]["VoiceLength"] = "00:00:" + str(j["end"] - j["start"])
    items[i]["Length"] = int(j["end"] - j["start"]) * 60
    items[i]["Frame"] = int(j["start"] * 60)
    items[i]["CharacterName"] = str(sys.argv[3])

chara["Length"] = items[-1]["Length"] + items[-1]["Frame"]
chara["CharacterName"] = str(sys.argv[3])

default_project["Timeline"]["Items"] = items

# 立ち絵の自動表示を行いたい場合は以下を有効化する
# default_project["Timeline"]["Items"].append(chara)

file_path = input("---書き出し完了---\nファイル名: ")
save(f"./export/{file_path}.ymmp", default_project)
