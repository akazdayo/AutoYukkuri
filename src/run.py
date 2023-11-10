import flet as ft
from app import App


class Layout:
    def __init__(self) -> None:
        self.app = App()

    def items(self):
        self.pick_files_dialog = ft.FilePicker(
            on_result=self.pick_files_result)

        self.save_files_dialog = ft.FilePicker(
            on_result=self.save_file_result)
        self.input_file = ft.Text("選択したファイルはここに表示されます")
        self.output_file = ft.Text("保存したファイルはここに表示されます")

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
            ],
            value="small",
        )

        self.run_button = ft.ElevatedButton(
            "Run", color=ft.colors.GREEN, on_click=self.run)

    def run(self, e) -> None:
        self.app.run(
            model=self.model.value,
            input_path=self.input_file.value,
            output_path=self.output_file.value)

    # ファイル選択ダイアログ
    def pick_files_result(self, e: ft.FilePickerResultEvent):
        self.input_file.value = (
            ", ".join(map(lambda f: f.path, e.files)
                      ) if e.files else "キャンセルされました！"
        )
        self.input_file.update()

    def save_file_result(self, e: ft.FilePickerResultEvent):
        self.output_file.value = e.path if e.path else "保存がキャンセルされました！"
        self.output_file.update()


def create_app(page: ft.Page):
    layout = Layout()

    layout.items()  # 初期化

    # ダイアログをオーバーレイで非表示にする
    page.overlay.extend([layout.pick_files_dialog])
    page.overlay.extend([layout.save_files_dialog])

    page.add(
        layout.model,
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
    )


ft.app(target=create_app)
