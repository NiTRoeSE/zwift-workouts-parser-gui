import flet as ft

import sys
import platform
from time import sleep
from datetime import datetime

from pathlib import Path
import logging

from layout import AppLayout
from options import Options

today = datetime.today().strftime('%Y-%m-%d')
home = Path.home()
documents_path = home / "Documents" / "zwift-workout-parser-logs"
logfile_path = documents_path / f"zwp-{today}.log"
# create logdirectory if not present
documents_path.mkdir(parents=False, exist_ok=True)
format = "%(asctime)s : %(levelname)s : %(module)s : %(message)s"

file_handler = logging.FileHandler(filename=logfile_path)
stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [file_handler, stdout_handler]
logging.basicConfig(level=logging.INFO,format=format,handlers=handlers)

# Get a logger for your current module
logger = logging.getLogger(__name__)


def main(page: ft.Page):
    
    
    page.title = "ZWP | Zwift Workouts Parser - GUI"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.window.width = 1440
    page.window.height = 1024
    page.window.min_height = 980
    page.window.center()
    page.window.icon = "icon.png"

    page.window.resizable = True

    page.fonts = {

        "RobotoMono": "fonts/RobotoMono-VariableFont_wght.ttf",
        "Kanit": "fonts/Kanit-Bold.ttf",
    }

    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(thickness=0.0),
        color_scheme=ft.ColorScheme(
            primary = "#5487B0",
            primary_container= "#b9cedf",
            on_primary = "#ffffff",
            surface_tint = "#ecf2f9", # hover in menu etc.
            on_inverse_surface="#f2f2f3",
            secondary_container="#dde5f4", # sidemenu selected.. etc
            on_secondary_container="#5487B0",
            on_tertiary= "#FDFDFD", # used for textfield backgrounds
            on_tertiary_container=ft.Colors.SURFACE_CONTAINER_HIGHEST,  # lines , divider etc
            tertiary_container = "#FEFEFE" # used for responselist background
           
        ),
        bottom_sheet_theme=ft.BottomSheetTheme(
            bgcolor=ft.Colors.ON_PRIMARY

        ),
        #scaffold_bgcolor="RED" # background
        #font_family="RobotoMono",
    )

    page.dark_theme = ft.Theme(

        scrollbar_theme=ft.ScrollbarTheme(thickness=0.0),
        color_scheme=ft.ColorScheme(

            primary = "#779cbb", #color displayed most frequently across your app’s screens and components
            primary_container="#5487B0", # slider thumb
            on_primary = "#ffffff", #color of elements which are on controls with primary color as background color
            on_secondary = "#343434",
            secondary_container="#5487B0", # sidemenu selected.. etc
            outline_variant="#313131",
            surface_tint = "#3a3e43", # hover in menu etc.
            on_tertiary="#393939", # used for textfield backgrounds
            on_tertiary_container="#4a4a4a", # lines , divider etc
            tertiary_container="#303030" # used for responselist background
           
        ),
        bottom_sheet_theme=ft.BottomSheetTheme(
            bgcolor="#343434"

        ),
        scaffold_bgcolor="#1f1f1f" #background
    
        #font_family="RobotoMono",
    )

   
    page.theme.page_transitions.macos = ft.PageTransitionTheme.FADE_FORWARDS #macos
    page.theme.page_transitions.windows = ft.PageTransitionTheme.FADE_FORWARDS #windows
    page.theme.use_material3 = True
    page.theme_mode = "dark"
    page.theme = page.theme

    page.appbar_home = ft.AppBar(
        bgcolor=ft.Colors.ON_SECONDARY,
        leading_width=40,
        elevation_on_scroll=0,
        actions=[
            #ft.IconButton(ft.Icons.ACCOUNT_CIRCLE_ROUNDED, tooltip="Options",icon_color="#c1c1c1", on_click=lambda _: page.go("/options"),icon_size=20),
        ],
    )


    if platform.system() == 'Darwin':
        page.window.title_bar_hidden = True
        page.add(page.appbar_home)

    page.main_content = AppLayout(page)
    page.add(page.main_content)
    page.update()



ft.app(target=main, assets_dir="assets", view=ft.AppView.FLET_APP_HIDDEN)