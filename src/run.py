import os
import shutil
import flet as ft
from app import App
import json
from status import StatusUpdater as updater


class AddCharacter:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        # self.page.client_storage.clear()
        if not self.page.client_storage.contains_key("characters"):
            self.page.client_storage.set("characters", ["ゆっくり霊夢", "ゆっくり魔理沙"])
        self.characters: list = self.page.client_storage.get("characters")

    def change_chara(self):
        charalist = []
        for i in self.characters:
            charalist.append(ft.dropdown.Option(i))
        return charalist

    def find_option(self, option_name, d: ft.Dropdown):
        for option in d.options:
            if option_name == option.key:
                return option
        return None

    def add_clicked(self, e, d: ft.Dropdown, option_textbox: ft.TextField):
        d.options.append(ft.dropdown.Option(option_textbox.value))
        d.value = option_textbox.value
        self.characters.append(option_textbox.value)
        option_textbox.value = ""
        self.page.client_storage.set("characters", self.characters)
        print(self.page.client_storage.get("characters"))
        self.page.update()

    def delete_clicked(self, e, d: ft.Dropdown):
        option = self.find_option(d.value, d)
        if option != None:
            d.options.remove(option)
            self.characters.remove(d.value)
            self.page.client_storage.set("characters", self.characters)
            print(self.page.client_storage.get("characters"))
            self.page.update()


class Layout:
    def __init__(self, page: ft.Page) -> None:
        self.app = App()
        self.page = page
        self.updater = updater(page)
        self.chara = AddCharacter(page)

    def items(self):
        self.pick_files_dialog = ft.FilePicker(
            on_result=lambda e: self.pick_files_result(e, self.run_button))

        self.save_files_dialog = ft.FilePicker(
            on_result=self.save_file_result)
        self.input_file = ft.Text("選択したファイルはここに表示されます")
        self.output_file = ft.Text("保存したファイルはここに表示されます")

        self.status = ft.Text("待機中")
        self.page.session.set("status_component", self.status)

        self.input_button = ft.ElevatedButton(
            "参照",
            icon=ft.icons.UPLOAD_FILE,
            on_click=lambda _: self.pick_files_dialog.pick_files(
            ),
            color=ft.colors.PURPLE
        )

        self.save_button = ft.ElevatedButton(
            "保存",
            icon=ft.icons.DOWNLOAD,
            on_click=lambda _: self.save_files_dialog.save_file(
                file_name="Auto.ymmp"
            ),
        )

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
                ft.dropdown.Option("large-v3"),
            ],
            value="small",
        )

        self.run_button = ft.ElevatedButton(
            "Run",
            color=ft.colors.GREEN,
            on_click=lambda _: self.app.run(
                model=self.model.value,
                input_path=self.input_file.value,
                output_path=self.output_file.value,
                page=self.page,
            ),
            disabled=True
        )
        chara_option = self.chara.change_chara()
        self.d = ft.Dropdown(label="キャラクターリスト", width=300,
                             options=chara_option)
        self.option_textbox = ft.TextField(hint_text="キャラクター名を入力")
        self.add = ft.ElevatedButton(
            "追加", on_click=lambda e: self.chara.add_clicked(e, self.d, self.option_textbox))
        self.delete = ft.OutlinedButton(
            "選択中のゆっくりを削除", on_click=lambda e: self.chara.delete_clicked(e, self.d))

    # ファイル選択ダイアログ
    def pick_files_result(self, e: ft.FilePickerResultEvent, button: ft.ElevatedButton):
        self.input_file.value = (
            ", ".join(map(lambda f: f.path, e.files))
            if e.files else "キャンセルされました")
        self.input_file.update()
        button.disabled = False
        button.update()

    def save_file_result(self, e: ft.FilePickerResultEvent):
        self.output_file.value = e.path if e.path else "キャンセルされました"
        self.output_file.update()
        if self.output_file.value != "キャンセルされました" and self.output_file.value != "保存したファイルはここに表示されます" and self.page.session.contains_key("project"):
            with open(self.output_file.value, "w", encoding='utf-8-sig') as file:
                json.dump(self.page.session.get("project"),
                          file, indent=4, ensure_ascii=False)
            self.page.session.remove("project")
            self.status.value = "保存しました"
            self.status.update()
            print("保存しました。")


class CloseEvent:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.page.window_prevent_close = True
        self.page.on_window_event = self.window_event
        self.confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("確認"),
            content=ft.Text(
                "本当にAuto Yukkuriを終了してよろしいですか？\n実行中の場合、作業内容が保存されない場合があります。"),
            actions=[
                ft.ElevatedButton("はい", on_click=self.yes_click),
                ft.OutlinedButton("いいえ", on_click=self.no_click),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def window_event(self, e):
        if e.data == "close":
            self.page.dialog = self.confirm_dialog
            self.confirm_dialog.open = True
            self.page.update()

    def yes_click(self, e):
        self.page.window_destroy()

    def no_click(self, e):
        self.confirm_dialog.open = False
        self.page.update()


def create_app(page: ft.Page):
    layout = Layout(page)
    layout.items()  # 初期化
    CloseEvent(page)
    # tempフォルダが存在した場合削除
    if os.path.exists("./temp"):
        shutil.rmtree("./temp")

    # ダイアログをオーバーレイで非表示にする
    page.overlay.extend([layout.pick_files_dialog])
    page.overlay.extend([layout.save_files_dialog])
    page.scroll = True

    page.add(
        layout.model,
        layout.status,
        ft.Row(
            [
                layout.input_button,
                layout.input_file,
            ]
        ),
        ft.Row(
            [
                layout.run_button,
                layout.save_button,
                layout.output_file,
            ]
        ),
        ft.Divider(height=50),
        ft.Text("ゆっくりを追加", style=ft.TextThemeStyle.TITLE_LARGE),
        layout.d,
        ft.Row(
            [
                layout.option_textbox,
                layout.add,
                layout.delete
            ]
        )
    )


ft.app(target=create_app)
