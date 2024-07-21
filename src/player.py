import flet as ft
#import winsound


class Player:
    def __init__(self, page: ft.Page, all_path: list, characters: list) -> None:
        self.page = page
        self.path = all_path
        self.chara = characters

    def change_chara(self):
        charalist = []
        for i in self.chara:
            charalist.append(ft.dropdown.Option(i))
        return charalist

    def show(self, number: int):
        self.player_end = True
        self.select_list = []
        self.page.add(ft.Divider(height=30))
        for i in range(number):
            play_button = ft.ElevatedButton(
                icon=ft.icons.PLAY_CIRCLE_OUTLINED,
                text=f"Play User{i}",
                on_click=lambda _, num=i: winsound.PlaySound(
                    self.path[num], winsound.SND_ASYNC)
            )

            chara_select = ft.Dropdown(
                label="モデル",
                width=300,
                options=self.change_chara(),
                value=self.chara[0]
            )

            self.select_list.append(chara_select)

            self.page.add(
                ft.Row(
                    [
                        play_button,
                        chara_select
                    ]
                )
            )

        self.page.add(ft.ElevatedButton(
            "Submit",
            on_click=self.end
        ))
        self.page.update()
        while (self.player_end):
            pass
        return self.select_list

    def end(self, _):
        print("end")
        select = []
        for i in self.select_list:
            select.append(i.value)
        self.select_list = select
        self.player_end = False
