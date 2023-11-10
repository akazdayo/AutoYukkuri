import flet as ft
from generate import Process
from clustering import SpeakerClustering
import glob
import json
import queue

q = queue.Queue()


class Layout:
    def __init__(self) -> None:
        self.pick_files_dialog = ft.FilePicker(
            on_result=self.pick_files_result)

        self.save_files_dialog = ft.FilePicker(
            on_result=self.save_file_result)
        self.selected_files = ft.Text("選択したファイルはここに表示されます")
        self.save_file_path = ft.Text("保存したファイルはここに表示されます")

        # ドロップダウンメニュー
        self.model = ft.Dropdown(
            label="モデル",
            hint_text="使用するモデルを設定してください",
            options=[
                ft.dropdown.Option("tiny"),
                ft.dropdown.Option("base"),
                ft.dropdown.Option("small"),
                ft.dropdown.Option("medium"),
                ft.dropdown.Option("large"),
                ft.dropdown.Option("large-v2"),
            ],
            value="small",
            on_change=self.return_dropdown
        )

        self.select_dropdown = None

        # ボタン
        self.save_button = ft.ElevatedButton(
            "Save As...", color=ft.colors.BLUE)
        # self.run_button = ft.ElevatedButton("Run", color=ft.colors.GREEN,on_click=)

    def return_dropdown(self, e):
        self.select_dropdown = self.model.value
        q.put(self.model.value)
        print(self.model.value)

    # ファイル選択ダイアログ
    def pick_files_result(self, e: ft.FilePickerResultEvent):
        self.selected_files.value = (
            ", ".join(map(lambda f: f.path, e.files)
                      ) if e.files else "キャンセルされました！"
        )
        self.selected_files.update()

    def save_file_result(self, e: ft.FilePickerResultEvent):
        self.save_file_path.value = e.path if e.path else "保存がキャンセルされました！"
        self.save_file_path.update()


class App:
    def __init__(self) -> None:
        self.process = Process()
        self.layout = Layout()
        self.speaker = SpeakerClustering()
        self.characters = ["ゆっくり霊夢", "ゆっくり魔理沙", "フラン", "トマト",
                           "青い生物", "天の声(霊夢)", "うぷ主", "ゆっくり霊夢(古)", "ゆっくり魔理沙(古)"]

    def run(self, e):
        print("音声認識中")
        a = q.get()
        print(a)
        result = self.process.convert(
            a, self.layout.selected_files.value)
        print("話者認識中")
        self.speaker.triming(result, self.layout.selected_files.value)
        files = glob.glob(".\\temp\\*.wav")
        users = self.speaker.clustering(files)
        print("出力中")
        self.proj = self.process.write(result, users[1], self.characters)
        with open(self.layout.save_file_path.value, "w", encoding='utf-8-sig') as file:
            json.dump(self.proj, file, indent=4, ensure_ascii=False)
