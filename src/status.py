import flet as ft


class StatusUpdater:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.status = page.session.get("status_component")  # セッションに入れてみる
        self.old_status = ""

    def update(self, now_status) -> None:
        self.status.value = now_status
        self.status.update()

    def checker(self, status) -> None:
        now_status = status
        if now_status != self.old_status:
            self.update(now_status)
            self.old_status = now_status
