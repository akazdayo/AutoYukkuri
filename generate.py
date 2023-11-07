import whisper
import time
from pykakasi import kakasi
import json
import re
import PySimpleGUI as sg
import threading
from pprint import pprint
from utils.clustering import SpeakerClustering as cluster
import glob
from utils.popup import AudioCheck
import shutil
import os


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
        pprint(f"---変換終了---\n変換時間{end-start}秒です。")
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


class App:
    def __init__(self) -> None:
        self.process = Process()
        self.speaker = cluster()
        self.checker = AudioCheck()

        file_input_col = [sg.Text('ファイル'),
                          sg.InputText(key='INPUT_FILE', enable_events=True, size=(45, 1)),
                          sg.FileBrowse('参照', file_types=(('mp3', '*.mp3'), ('mp4', '*.mp4'), ('wav', '*.wav')))]
        model_col = [sg.Text('モデル'),
                     sg.Listbox(values=('tiny', 'base', 'small', 'medium', 'large', 'large-v2'),
                                size=(30, 6), key='MODEL', enable_events=True, default_values='small')]
        save_path = [[sg.Text('保存先を入力')],
                     [sg.Input(), sg.FileSaveAs(file_types=(('YMMP Files', '*.ymmp'),), key='SAVE_PATH')]]

        self.status = [sg.Text('待機中', key='STATUS')]
        self.layout = [file_input_col,
                       model_col,
                       self.status,
                       save_path,
                       [sg.Submit()]]

    def run_process(self, val):
        characters = ["ゆっくり霊夢", "ゆっくり魔理沙", "フラン", "トマト", "青い生物", "天の声(霊夢)", "うぷ主", "ゆっくり霊夢(古)", "ゆっくり魔理沙(古)"]
        result = self.process.convert(val['MODEL'][0], val['INPUT_FILE'])
        self.status[0].update('話者認識中')
        self.speaker.triming(result, val['INPUT_FILE'])
        files = glob.glob(".\\temp\\*.wav")
        users = self.speaker.clustering(files)
        self.status[0].update('出力中')
        print(users[0])
        self.checker.create(users[0], characters)
        vals = self.checker.loop()
        characters = self.checker.chara_list(vals)
        pprint(characters)
        self.proj = self.process.write(result, users[1], characters)
        self.status[0].update('完了')

    def loop(self):
        window = sg.Window('Auto Yukkuri', self.layout, keep_on_top=True)
        self.proj = None
        # イベントのループ
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == 'Submit':
                with open(values['SAVE_PATH'], "w", encoding='utf-8-sig') as file:
                    json.dump(self.proj, file, indent=4, ensure_ascii=False)
                    self.status[0].update('保存完了')
            elif values['INPUT_FILE'] != '':
                self.status[0].update('音声認識中')
                # thread = threading.Thread(target=self.run_process, args=(values,))
                # thread.start()
                self.run_process(values)
        # ウィンドウクローズ処理
        window.close()


if __name__ == '__main__':
    app = App()
    app.loop()
