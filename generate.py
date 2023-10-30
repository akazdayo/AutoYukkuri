import whisper
import time
from pykakasi import kakasi
import json
import re
import PySimpleGUI as sg
import threading

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
    def convert_numbers(self,word):
        pattern = r"\d+"
        matches = re.findall(pattern, word)
        for match in matches:
            word = word.replace(match, f"<NUMK VAL={match}>")
        return word

    # 発音に変換
    def convert_voice(self,word):
        converted = self.kakasi.convert(word)
        result = ""
        for converted_word in converted:
            result += f"{converted_word['hira']}"
        return self.convert_numbers(result)

    def convert(self,use_model,path):
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

    def write(self,result):
        items = []
        project = self.default_project.copy()
        for i, j in enumerate(result["segments"]):
            items.append(self.default_items.copy())
            items[i]["Serif"] = j["text"].replace("!", "")
            items[i]["Hatsuon"] = self.convert_voice(j["text"])
            items[i]["VoiceLength"] = "00:00:" + str(j["end"] - j["start"])
            items[i]["Length"] = int(j["end"] - j["start"]) * 60
            items[i]["Frame"] = int(j["start"] * 60)
            items[i]["CharacterName"] = str("ゆっくり霊夢")
        project["Timeline"]["Items"] = items
        return project

class App:
    def __init__(self) -> None:
        self.process = Process()

        file_input_col = [sg.Text('ファイル'),
                        sg.InputText(key='INPUT_FILE', enable_events=True, size=(45,1)),
                        sg.FileBrowse('参照', file_types=(('mp3', '*.mp3'), ('mp4', '*.mp4'),('wav','*.wav')))]
        model_col = [sg.Text('モデル'),
                        sg.Listbox(values=('tiny', 'base', 'small', 'medium', 'large', 'large-v2'),
                                    size=(30, 6),key='MODEL',enable_events=True,default_values='small')]
        save_path = [[sg.Text('保存先を入力')],
                    [sg.Input(), sg.FileSaveAs(file_types=(('YMMP Files', '*.ymmp'),),key='SAVE_PATH')]]
        
        self.status = [sg.Text('待機中',key='STATUS')]
        self.layout = [  file_input_col,
                    model_col,
                    self.status,
                    save_path,
                    [sg.Submit()]]

    def run_process(self,val):
        result = self.process.convert(val['MODEL'][0],val['INPUT_FILE'])
        self.status[0].update('出力中')
        self.proj = self.process.write(result)
        self.status[0].update('完了')

    def loop(self):
        window = sg.Window('Auto Yukkuri', self.layout)
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
                thread = threading.Thread(target=self.run_process, args=(values,))
                thread.start()
        # ウィンドウクローズ処理
        window.close()

if __name__ == '__main__':
    app = App()
    app.loop()