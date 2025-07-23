import flet as ft

class HelpTile(ft.ExpansionTile):
    def __init__(self, title, icon, file_path):
        self.title = title
        self.icon = icon
        self.file_path = file_path

        self.info_file = open(file_path)
        self.info = self.info_file.read()
        self.info_file.close()   

        super(HelpTile, self).__init__(
            title=ft.Text(self.title, color=ft.Colors.PRIMARY,weight=ft.FontWeight.W_600,size=20),
            icon_color=ft.Colors.PRIMARY,
            bgcolor=ft.Colors.ON_INVERSE_SURFACE,
            collapsed_bgcolor=ft.Colors.TRANSPARENT,
            leading=ft.Icon(self.icon, color=ft.Colors.PRIMARY),
            trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN,color=ft.Colors.PRIMARY),
            collapsed_text_color=ft.Colors.ON_SECONDARY_CONTAINER,
            controls_padding=ft.padding.all(10),
            collapsed_shape=ft.RoundedRectangleBorder(radius=5),
            controls=[ft.Markdown(
                            self.info,
                            selectable=True,
                            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                            code_theme="GITHUB_GIST",
                            code_style_sheet=ft.MarkdownStyleSheet(
                                code_text_style=ft.TextStyle(font_family="RobotoMono")
                            ),
                            on_tap_link=lambda e: self.page.launch_url(e.data),
                        )],
             
        )


