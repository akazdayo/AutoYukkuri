from generate import Process
from clustering import SpeakerClustering
import glob
import json
import platform


class App:
    def __init__(self) -> None:
        self.process = Process()
        self.speaker = SpeakerClustering()
        self.characters = ["ゆっくり霊夢", "ゆっくり魔理沙", "フラン", "トマト",
                           "青い生物", "天の声(霊夢)", "うぷ主", "ゆっくり霊夢(古)", "ゆっくり魔理沙(古)"]

    def run(self, model: str, input_path: str, output_path: str, page) -> None:
        print("音声認識中")
        result = self.process.convert(
            model, input_path)
        print("話者認識中")
        self.speaker.triming(result, input_path)
        if platform.system == "win32":
            files = glob.glob(".\\temp\\*.wav")
        else:
            files = glob.glob("./temp/*.wav")
        users = self.speaker.clustering(files)
        print("出力中")
        proj = self.process.write(result, users[1], self.characters)
        if output_path == None or output_path == "保存したファイルはここに表示されます" or output_path == "キャンセルされました":
            page.session.set("project", proj)
            print("保存待ち")
        else:
            with open(output_path, "w", encoding='utf-8-sig') as file:
                json.dump(proj, file, indent=4, ensure_ascii=False)
            print("保存しました。")
