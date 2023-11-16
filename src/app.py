from generate import Process
from clustering import SpeakerClustering
import glob
import json
import platform
import flet as ft
from status import StatusUpdater as updater
from player import Player


class App:
    def __init__(self) -> None:
        self.process = Process()
        self.speaker = SpeakerClustering()

    def run(self, model: str, input_path: str, output_path: str, page: ft.Page) -> None:
        self.characters = page.client_storage.get("characters")
        self.status_checker = updater(page)
        print("音声認識中")
        self.status_checker.checker("音声認識中")
        result = self.process.convert(
            model, input_path)
        print("話者認識中")
        self.status_checker.checker("話者認識中")
        self.speaker.triming(result, input_path)
        if platform.system == "win32":
            files = glob.glob(".\\temp\\*.wav")
        else:
            files = glob.glob("./temp/*.wav")
        users = self.speaker.clustering(files)
        play = Player(page, users[0], self.characters)
        self.characters = play.show(len(users[0]))
        print("出力中")
        self.status_checker.checker("出力中")
        proj = self.process.write(result, users[1], self.characters)
        if output_path == None or output_path == "保存したファイルはここに表示されます" or output_path == "キャンセルされました":
            page.session.set("project", proj)
            print("保存待ち")
            self.status_checker.checker("保存待ち")
        else:
            with open(output_path, "w", encoding='utf-8-sig') as file:
                json.dump(proj, file, indent=4, ensure_ascii=False)
            print("保存しました。")
            self.status_checker.checker("保存しました")
