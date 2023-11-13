import whisper
import time
from pykakasi import kakasi
import json
import re


# 読み込み
def read(path):
    with open(path, "r", encoding="utf-8-sig") as file:
        return json.load(file)


class Process:
    def __init__(self) -> None:
        self.kakasi = kakasi()
        self.default_items = read("./default/items.json")
        self.default_project = read("./default/project.json")

    # 数字の変換
    def convert_numbers(self, word):
        pattern = r"\d+"
        matches = re.findall(pattern, word)
        for match in matches:
            word = word.replace(match, f"<NUMK VAL={match}>")
        return word

    # 発音に変換
    def convert_voice(self, word):
        converted = self.kakasi.convert(word)
        result = ""
        for converted_word in converted:
            result += f"{converted_word['hira']}"
        return self.convert_numbers(result)

    def convert(self, use_model, path):
        model = whisper.load_model(use_model)
        print("---変換開始---")
        start = time.time()
        result = model.transcribe(
            path,  # ファイルパス
            verbose=True,
            language="ja",
        )
        end = time.time()
        print(f"---変換終了---\n変換時間{end-start}秒です。")
        return result

    def write(self, result, chara_num: list, chara: list):
        items = []
        project = self.default_project.copy()
        for i, j in enumerate(result["segments"]):
            items.append(self.default_items.copy())
            items[i]["Serif"] = j["text"].replace("!", "")
            items[i]["Hatsuon"] = self.convert_voice(j["text"])
            items[i]["VoiceLength"] = "00:00:" + str(j["end"] - j["start"])
            items[i]["Length"] = int(j["end"] - j["start"]) * 60
            items[i]["Frame"] = int(j["start"] * 60)
            items[i]["CharacterName"] = chara[chara_num[i]]
        project["Timeline"]["Items"] = items
        return project
