import flet as ft
from antenna_setting_view import AntennaSettingView


def main(page: ft.Page):

    page.views.append(AntennaSettingView())
    page.update()

ft.app(main)
