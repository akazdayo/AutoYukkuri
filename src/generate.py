import whisper
import time
import json
from hatsuon import Hatsuon


# 読み込み
def read(path):
    with open(path, "r", encoding="utf-8-sig") as file:
        return json.load(file)


class Process:
    def __init__(self) -> None:
        self.default_items = read("./default/items.json")
        self.default_project = read("./default/project.json")

    def convert(self, use_model, path):
        model = whisper.load_model(use_model)
        print("---変換開始---")
        start = time.time()
        print(path)
        result = model.transcribe(
            path,  # ファイルパス
            verbose=True,
            language="ja",
        )
        end = time.time()
        print(f"---変換終了---\n変換時間{end-start}秒です。")
        return result

    def write(self, result, chara_num: list, chara: list):
        hatsuon = Hatsuon()
        items = []
        project = self.default_project.copy()
        for i, j in enumerate(result["segments"]):
            items.append(self.default_items.copy())
            items[i]["Serif"] = j["text"].replace("!", "")
            items[i]["Hatsuon"] = hatsuon.convert(j["text"])
            items[i]["VoiceLength"] = "00:00:" + str(j["end"] - j["start"])
            items[i]["Length"] = int(j["end"] - j["start"]) * 60
            items[i]["Frame"] = int(j["start"] * 60)
            items[i]["CharacterName"] = chara[chara_num[i]]
        project["Timeline"]["Items"] = items
        return project
