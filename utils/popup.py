import PySimpleGUI as sg
import winsound


class AudioCheck:
    def __init__(self) -> None:
        pass

    def create(self, file_list, options):
        # 初期化
        self.file_list = file_list
        select_box_content = options
        select_boxes = []

        # レイアウトの設定
        layout = [[sg.Text("対応音声の設定")]]
        for i, file in enumerate(self.file_list):
            select_box = sg.Combo(select_box_content, default_value=select_box_content[0], key=f'COMBO{i}', size=[30, 1])
            select_boxes.append(select_box)
            layout.append([sg.Listbox(values=[file], size=(15, 1), key=f'FILE{i}', select_mode=sg.LISTBOX_SELECT_MODE_SINGLE), select_box])
        layout.append([sg.Button('再生'), sg.Button('停止')])
        layout.append([sg.Button('完了')])
        self.window = sg.Window('Audio Checker', layout, keep_on_top=True)

    def chara_list(self, val):
        # "COMBO"を含むキーの辞書を作成します
        combo_dict = {k: v for k, v in val.items() if "COMBO" in k}
        return [i for i in combo_dict.values()]

    def loop(self):
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED:
                break
            elif event == '再生':
                for i, file in enumerate(self.file_list):
                    if values.get(f'FILE{i}') and values[f'FILE{i}'][0]:
                        print("----")
                        print(file)
                        winsound.PlaySound(file, winsound.SND_ASYNC)
            elif event == '停止':
                winsound.PlaySound(None, winsound.SND_PURGE)
            elif event == '完了':
                self.window.close()
                return values

        self.window.close()


if __name__ == "__main__":
    audio = AudioCheck()
    audio.create(['temp/0.wav', 'temp/1.wav'], ["ゆっくり霊夢", "ゆっくり魔理沙"])
    a = audio.loop()
    print(a)
