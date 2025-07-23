import flet as ft
from zwp import ZWP 
from time import sleep

from options import Options
import logging

class AppLayout(ft.Container):
    def __init__(self, page):
        super(AppLayout, self).__init__()

        self.logger = logging.getLogger(__name__)
        self.logger.info("Init...")

        self.page = page
        self.expand = True

        self.downloadfolder_path = self.page.client_storage.get("zwiftworkoutparser.download.folder.path")

        self.bar_row = ft.Row(
            controls=[
                 ft.IconButton(ft.Icons.WEB, tooltip="ZWP",icon_color="#c1c1c1", on_click=self.change_content,data="zwp",icon_size=20),
                 ft.IconButton(ft.Icons.PAGEVIEW, tooltip="Whatsonzwift",icon_color="#c1c1c1",on_click=lambda _: self.page.launch_url("https://whatsonzwift.com"),data="zwp",icon_size=20),
                 ft.Container(expand=True),
                 ft.IconButton(ft.Icons.SETTINGS_ROUNDED, tooltip="Options",icon_color="#c1c1c1", on_click=self.change_content,data="options",icon_size=20)
            ],
            height=40
        )
    
        self.pagecontent = ft.Container(
            content="",
            expand=True,
            border_radius= 6,
            animate_opacity=ft.Animation(250),
            opacity=1,
        
            )
    
        self.banner = ft.AlertDialog(
            icon=ft.Image(
                                src=f"icon.png",
                                width=150,
                                height=150,
                            ),
            title=ft.Text("Welcome to ZWP | Zwift Workouts Parser - GUI",text_align=ft.TextAlign.CENTER),
            content=ft.Text("Before you start you have to set your default downloads directory for your parsed workouts.\n\nYou can leave the prefilled directory or choose your own, after that navigate to ZWP in bottom menu and parse your Workouts.",text_align=ft.TextAlign.CENTER),
            alignment=ft.alignment.center,
            on_dismiss=lambda e: print("Dialog dismissed!"),
            title_padding=ft.padding.all(25),
            actions=[
                ft.TextButton("Continue", on_click=self.close_banner),

            ],

        )
  
        """ Check if default download folder is set """
        
        #Debug
        #self.page.client_storage.remove("zwiftworkoutparser.download.folder.path")
        
        if self.page.client_storage.contains_key("zwiftworkoutparser.download.folder.path") == True:  
            self.pagecontent.content = ZWP(self.page)

        else:
            self.logger.info(f"Default download directory not set --> run first start banner...")
            self.page.open(self.banner)
            self.pagecontent.content = Options(self.page)

           
        
        self.pagecontent_container = ft.Container(
                content=self.pagecontent,
                expand=True,
                padding =16,
                #padding= ft.padding.only(top=16,left=16,right=16),
                border_radius= 6,
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=8,
                    color=ft.Colors.OUTLINE_VARIANT,
                    offset=ft.Offset(0, 0),
                    blur_style=ft.ShadowBlurStyle.OUTER,
                ),
                bgcolor=ft.Colors.ON_SECONDARY
        )

        self.layout = ft.Column(
            controls=[
                #self.sidemenu,
                self.pagecontent_container,
                self.bar_row
                
            ],
            expand = True,
            alignment = ft.MainAxisAlignment.START,
            spacing = 16
        )

    def build(self):
        self.logger.info(f"Build...")
        self.content = self.layout

    def change_content(self,e):

        #print(e)
        #print(e.control)
        #print(e.control.data)

        self.logger.info(f"change content to: {e.control.data}")

        def animate_content_change(self,e, content):

            self.pagecontent.opacity = 0
            self.pagecontent.update()
            sleep(0.25)
            self.pagecontent.content = content
            self.pagecontent.opacity = 1
            self.page.update()

        if  e.control.data == "zwp":
            animate_content_change(self,e, ZWP(self.page))
            
        if  e.control.data == "options":
            animate_content_change(self,e, Options(self.page))
            

        #store which was last content maybe we need it later..
        self.last_content = e.control
        self.page.update()

    def close_banner(self,e):
            self.logger.info(f"Close first start wizzard...")
            self.page.close(self.banner)
            #self.pagecontent.content = Options(self.page)
            #self.page.update()