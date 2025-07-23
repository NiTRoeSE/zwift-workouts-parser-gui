import flet as ft
import platform,os
from helper import HelpTile
import logging

try:
    from versions import version, commit
except:
    version = '..could not get version'
    commit = '..could not get commit hash'

class Options(ft.Column):
    def __init__(self, page):
        super(Options, self).__init__(expand=True)
    

        self.logger = logging.getLogger(__name__)
        self.logger.info("Init...")

        self.page = page
        self.check_results = {}

        if platform.system() == 'Windows':
            self.username = os.getenv('username')
            self.default_downloadfolder_path = f'C:\\Users\\{self.username}\\Downloads'
            
        if platform.system() == 'Darwin':
            self.username = os.environ.get('USER')
            self.default_downloadfolder_path =  f'/Users/{self.username}/Downloads'
            
        if self.page.client_storage.contains_key("zwiftworkoutparser.download.folder.path") == True:
            self.downloadfolder_path = self.page.client_storage.get("zwiftworkoutparser.download.folder.path")
        else:
            self.downloadfolder_path = self.default_downloadfolder_path
            self.page.client_storage.set("zwiftworkoutparser.download.folder.path", self.default_downloadfolder_path)
       

        self.filepick_downloadsfolder= ft.FilePicker(on_result=self.pick_files_result_downloadfolder)
        self.page.overlay.append(self.filepick_downloadsfolder)

        self.downloadfolder_path_textfield = ft.TextField(label="DOWNLOAD DIRECTORY", disabled=True, value=self.downloadfolder_path, color=ft.Colors.GREY_400,border_color=ft.Colors.ON_TERTIARY_CONTAINER,fill_color=ft.Colors.ON_TERTIARY,expand=2,show_cursor=True)

        self.downloadfolder_path_button =  ft.IconButton(
                                        icon=ft.Icons.FOLDER_OUTLINED,
                                        icon_color=ft.Colors.SECONDARY,
                                        tooltip="Select your download folder.",
                                        icon_size= 35,
                                        style=ft.ButtonStyle(
                                                    shape=ft.RoundedRectangleBorder(radius=10)
                                                ),
                                        on_click=lambda _: self.filepick_downloadsfolder.get_directory_path()
                                    )
        
        self.downloadfolder_path_row = ft.Row(
                                spacing=4, 
                                controls=[
                                    self.downloadfolder_path_textfield,
                                    self.downloadfolder_path_button

                                ])

        self.bs_img = ft.Row(
                        controls=[
                            ft.Image(
                                src=f"icon.png",
                                width=150,
                                height=150,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
      
        self.bs_text = ft.Row(
                        controls = [
                            ft.Text("ZWP | Zwift-Workout-Parser GUI",
                            text_align= ft.TextAlign.JUSTIFY,
                            style = ft.TextStyle(font_family="Kanit",size=30),
                        
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
        
        self.bs_content = ft.Column(
                            controls=[
                                self.bs_img,
                                self.bs_text,
                                ft.Row(
                                    controls=[
                                        ft.Text(
                                            f"version: {version}",
                                            text_align= ft.TextAlign.JUSTIFY,
                                            style = ft.TextStyle(font_family="RobotoMono",size=12),
                                        ),
                                        
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Text(
                                            f"Hash: {commit}",
                                            text_align= ft.TextAlign.JUSTIFY,
                                            style = ft.TextStyle(font_family="RobotoMono",size=12),
                                            selectable = True 
                                        ),
                                        
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Text(
	                                            "© NiTRoSoft",
                                            text_align= ft.TextAlign.JUSTIFY,
                                            style = ft.TextStyle(font_family="RobotoMono",size=12),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                
                                ),
                                ft.Divider(color=ft.Colors.TRANSPARENT,height=5),
                                ft.Column(
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                ft.Text(
                                                        "This project is possible thanks to: ",
                                                    text_align= ft.TextAlign.JUSTIFY,
                                                    style = ft.TextStyle(font_family="RobotoMono",size=14,color=ft.Colors.PRIMARY,weight=ft.FontWeight.BOLD),
                                                ),
                                                
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                        
                                        ),
                                        ft.Row(controls=[ft.TextButton("Flet", url="https://github.com/flet-dev/flet"),], alignment=ft.MainAxisAlignment.CENTER,),
                                        ft.Row(controls=[ft.TextButton("Zwift-Workouts-Parser", url="https://github.com/alexshpunt/zwift_workouts_parser"),], alignment=ft.MainAxisAlignment.CENTER,),
                                        
                                    ],
                                    alignment=ft.CrossAxisAlignment.CENTER
                                ),
                                

                            ],
                            expand=True,
                            #height=page.height,
                            #width=page.width,
                            alignment=ft.MainAxisAlignment.CENTER
                           
                    )     



        self.bs_button =  ft.Row(
                            controls=[
                                 ft.TextButton(text="About",on_click=lambda _: self.page.open(self.bs)),
                            ],
                           
                            
                            alignment=ft.MainAxisAlignment.CENTER,
                            height=50

                        )
        
        self.bs = ft.BottomSheet(
                #on_dismiss=self.handle_dismissal,
                content=ft.Container(
                    padding=50,
                    content=ft.Column(
                        tight=True,
                        #expand=True,
                        controls=[
                            self.bs_content,
                        ],
                    ),
                   
                ),
            )
        

                                   
        
    def build(self):
        self.logger.info("Build...")
        self.controls = [ft.Container(
                            expand=True,
                            content = ft.Column(controls=[
                                HelpTile("Options",ft.Icons.SETTINGS_APPLICATIONS_OUTLINED,"help_files/options.md"),
                                self.downloadfolder_path_row,
                                ft.Placeholder(expand=True, color=ft.Colors.TRANSPARENT),
                                self.bs_button,

                                ],
                                spacing=20
                            )

                )]
    
   
    def pick_files_result_downloadfolder(self, e: ft.FilePickerResultEvent):

        self.file_path_1 = e.path
        if self.file_path_1 != "Cancelled!":
            self.logger.info(f"Set download directory to: {self.file_path_1}")
            self.downloadfolder_path_textfield.value = self.file_path_1
            self.page.client_storage.set("zwiftworkoutparser.download.folder.path", self.file_path_1)
            self.downloadfolder_path_textfield.update()
        else:
            self.logger.info("Pick download directory cancelled...")

    def handle_dismissal(self,e):
        print(f'Bottomsheet dismissed')