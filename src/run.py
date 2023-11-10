import flet as ft
import app


def create_app(page: ft.Page):
    lt = app.Layout()
    run = app.App()

    # ダイアログをオーバーレイで非表示にする
    page.overlay.extend([lt.pick_files_dialog])
    page.overlay.extend([lt.save_files_dialog])

    page.add(
        lt.model,
        ft.Row(
            [
                ft.ElevatedButton(
                    "参照",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda _: lt.pick_files_dialog.pick_files(
                    ),
                    color=ft.colors.PURPLE
                ),
                lt.selected_files,
            ]
        ),
        ft.Row([
            ft.ElevatedButton("Run", color=ft.colors.GREEN, on_click=run.run),
            ft.ElevatedButton(
                "File Picker Test",
                icon=ft.icons.UPLOAD_FILE,
                on_click=lambda _: lt.save_files_dialog.save_file(
                    file_name="hoge"
                ),
            ),
            lt.save_file_path
        ]),
    )


ft.app(target=create_app)
