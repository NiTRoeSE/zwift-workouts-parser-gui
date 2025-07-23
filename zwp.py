import flet as ft
from helper import HelpTile
import validators
#import zwift_parser as zp
import subprocess
from showinfm import show_in_file_manager
import logging
import platform,os

import zwift_parser.zwift_parser as zp

class ZWP(ft.Column):

    def __init__(self, page):
        super(ZWP, self).__init__()

        # Get a logger for your current module
        self.logger = logging.getLogger(__name__)
        self.logger.info("Init...")

        self.expand = True
        self.page = page

        self.downloadfolder_path = self.page.client_storage.get("zwiftworkoutparser.download.folder.path")

        self.url_input = ft.TextField(label="URL",border_color=ft.Colors.ON_TERTIARY_CONTAINER,fill_color=ft.Colors.ON_TERTIARY_CONTAINER,hover_color=ft.Colors.TRANSPARENT,col={"sm":12}, prefix_icon=ft.Icons.ADD_CHART, on_submit=self.run_script)
       
        self.input = ft.ResponsiveRow(
                    controls=[self.url_input],
                    expand=True
                    )
        
        self.response_list = ft.ListView(expand=True, spacing=6, padding=10, auto_scroll=True,controls=[])
        self.response_list_container = ft.Container(
                                        content=self.response_list,
                                        border=ft.border.all(1, ft.Colors.ON_TERTIARY_CONTAINER),
                                        border_radius= 6,
                                        bgcolor = ft.Colors.TERTIARY_CONTAINER,
                                        expand=1
                                )
        
        self.snackbar = ft.SnackBar(
                            content=ft.Text("snack placeholder"),
                            bgcolor=ft.Colors.RED_400,
                            shape=ft.RoundedRectangleBorder(radius=5),
                            
                    )


    def build(self):
 
        self.logger.info("Build zwp layout...")
        self.controls = [
                
                    ft.Container(
                    expand = True,
                    content=ft.Column(
                                controls=[
                                    #ft.Divider(height=50, thickness=0, color=ft.Colors.TRANSPARENT),
                                    HelpTile("Zwift Workout Parser",ft.Icons.ALIGN_VERTICAL_BOTTOM,"help_files/zwp-help.md"),
                                    self.url_input,
                                    #ft.Row(self.script_option_chips,scroll=True), 
                                    self.response_list_container,
                                    #ft.Divider(height=20, thickness=0, color=ft.Colors.TRANSPARENT),
                                ],
                                #scroll=True,
                                spacing=20,
                            ),
                            
                            
                ),
                
            ]
        
    def run_script(self, url):

        progressbar = ft.ProgressBar(bar_height=3)
       
        self.url_input_value = self.url_input.value
        self.url_input_value = f'{self.url_input_value}'

        def run_zwp(url):
            self.validation = validators.url(url)
            if self.validation == True:
                self.logger.info(f'Parsing url: {url}')

                self.list_tile = ft.ListTile(
                            leading=ft.Icon(ft.Icons.ANALYTICS_OUTLINED,color=ft.Colors.PRIMARY),
                            title=ft.Text(
                                f"Parsing: {url}",
                                style = ft.TextStyle(font_family="Roboto",size=16,weight=ft.FontWeight.BOLD)
                            ),
                            bgcolor=ft.Colors.ON_TERTIARY_CONTAINER,
                            shape=ft.RoundedRectangleBorder(radius=6),
                            is_three_line=True,
                            subtitle=progressbar,
                            on_click=self.open_file_in

                        )
                
                self.response_list.controls.append(self.list_tile)
                self.response_list.update()

                try:
                    #self.zp_module_path = f'{' '.join(zp.__path__)}/zwift_parser.py'
                    #self.logger.info(f'ZP Module path: {self.zp_module_path}')

                    result = zp.Parser(self.downloadfolder_path,[url])
                    result = result.get_result([url])
                    """
                        ['- Parsing workout (1/1)', '-- Parsed workout Zwift-Camp-Inside-Out/Short/5-Climb-On-Lite (Parsed)']
                    """
                    #print(f"****{result}****")


                    if result:
                        #print(result.stdout.encode(encoding="utf-8") )

                        if "Parsing workout (1/1)" in result and len(result) == 2:
                            self.logger.info(f'detect single workout mode')

                            tile_text = result
                            tile_text = tile_text[1]
                            tile_text = tile_text.replace("--","")
                            tile_text = tile_text.replace("(Parsed)", "successful.")
                            tile_text = tile_text.strip()
                            self.logger.info(tile_text)
                            tile_text = f'\n{tile_text}' # newline for space between heading and result

                            zwp_subfolder = tile_text.strip()
                            zwp_subfolder = zwp_subfolder.replace("Parsed workout","")
                            zwp_subfolder = zwp_subfolder.strip()
                            zwp_subfolder = zwp_subfolder.split("/")
                            self.zwp_subfolder = zwp_subfolder[0]
                        
                            self.zwp_workout_name = f'{zwp_subfolder[1].replace(" successful.","")}.zwo'

                            tile_text = f'{tile_text}\nSaved file in {self.downloadfolder_path}/{self.zwp_subfolder}/{self.zwp_workout_name}'

                        else:
                            self.logger.info(f'detect training plan mode - parse multiple workouts at once')
                            tile_text = result
                            tile_text_multi = ""

                            for parse in tile_text:

                                successful_parsed = False

                                if parse != None and "Parsing url" not in parse and "- Parsing workout" not in parse and parse != '' and parse != '\n':
                                    print(parse.encode(encoding="utf-8") )
                                   
                                    parse = parse.replace("--","")
                                    parse = parse.replace("(Parsed)", "successful.")
                                    parse = parse.strip()

                                    self.logger.info(parse)

                                    zwp_subfolder = parse.strip()
                                    zwp_subfolder = zwp_subfolder.replace("Parsed workout","")
                                    zwp_subfolder = zwp_subfolder.strip()
                                    zwp_subfolder = zwp_subfolder.split("/")
                                    self.zwp_subfolder = zwp_subfolder[0]

                                    tile_text_multi = f'{tile_text_multi}\n{parse}'
                                    successful_parsed = True
                                    save_text = f'Saved training plan workouts in {self.downloadfolder_path}/{self.zwp_subfolder}'
                                
                                if successful_parsed == False and parse != None:
                                    """ zwift-workouts-parser only prints - Parsing workout (16/35) and nothing more if not possible to parse"""
                                    self.zwp_subfolder = ""
                                    tile_text_multi = f'{tile_text_multi}\n{parse} failed.'
                                    save_text = f'Could not parse workout plan, nothing to save.'
                                    self.logger.warning(f'{parse} failed.')
                            
                            tile_text = tile_text_multi 
                            tile_text = f'{tile_text}\n{save_text}'

                        self.list_tile.subtitle = ft.Text(tile_text,style = ft.TextStyle(font_family="Roboto",size=12))
                        self.list_tile.data = {"path":self.downloadfolder_path, "subfolder":self.zwp_subfolder}
                        if successful_parsed == True:
                            self.list_tile.leading = ft.Icon(ft.Icons.ANALYTICS_OUTLINED,color=ft.Colors.GREEN_400)
                        else:
                            self.list_tile.leading = ft.Icon(ft.Icons.ANALYTICS_OUTLINED,color=ft.Colors.RED_400)
                        self.url_input.value = ""
                        self.url_input.update()
                       
                    else:
                        self.list_tile.leading = ft.Icon(ft.Icons.WORK_OUTLINE,color=ft.Colors.RED_400)
                        self.list_tile.data = {"path":False, "subfolder":False}
                        self.list_tile.subtitle = ft.Text(result)
                    self.response_list.update()

                except Exception as zp_error:
                    print(zp_error)
                    self.list_tile.leading = ft.Icon(ft.Icons.WORK_OUTLINE,color=ft.Colors.RED_400)
                    self.list_tile.data = {"path":False, "subfolder":False}
                    self.list_tile.subtitle = ft.Text(zp_error)
                    self.response_list.update()
                    self.logger.error(f'Parsing error: {zp_error}')

            else:

                self.page.overlay.append(self.snackbar)
                self.snackbar.open = True
                self.snackbar.content = ft.Text(f"The URL you entered is not valid, enter a valid url and try again...")
                self.page.update()
                self.page.overlay.remove(self.snackbar)


        if self.url_input.value != None and self.url_input.value != "" and  self.url_input.value != " ":

            if " " in self.url_input.value:
                """ multiple urls"""
                self.urls = self.url_input.value.split(" ")

                for url in self.urls:
                    if url != " ":
                        run_zwp(url)
            else:
                """ single url """
                run_zwp(self.url_input.value)

            
    def open_file_in(self,e):
        #print(e)
        print(e.control.data)

        path = e.control.data["path"]
        subfolder = e.control.data["subfolder"]
        if path != False:
            if platform.system() == 'Windows':
                path = f'{path}\\{subfolder}'

            if platform.system() == 'Darwin':
                path = f'{path}/{subfolder}'

            self.logger.info(f"Open parsed file: {path}")
            show_in_file_manager(path)
