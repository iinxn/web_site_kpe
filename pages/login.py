from flet import *
from service.connection import *
from utils.consts import primary_colors

class Login(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.theme_mode = ThemeMode.LIGHT
        self.alignment = alignment.center
        self.expand = True
        self.bgcolor = primary_colors['GREEN']

        self.login_box = Container(
            content=TextField(
                content_padding=padding.only(top=0, bottom=0, right=20, left=20),
                hint_style=TextStyle(size=12, color=primary_colors['MANATEE']),
                label="Логин",
                cursor_color=primary_colors['MANATEE'],
                text_style=TextStyle(
                    size=14,
                    color="black",
                ),
                on_submit=self.login
            ),
        )
        self.password_box = Container(
            content=TextField(
                content_padding=padding.only(top=0, bottom=0, right=20, left=20),
                hint_style=TextStyle(size=12, color=primary_colors['MANATEE']),
                label="Пароль",
                cursor_color=primary_colors['MANATEE'],
                text_style=TextStyle(
                    size=14,
                    color="black",
                ),
                password=True,
                can_reveal_password=True,
                on_submit=self.login
            ),
        )
        self.error_box = Container(
            alignment=alignment.center,
            content=Text(value="", color=primary_colors['RED']),
        )
        self.content = Column(
            alignment="center",
            horizontal_alignment="center",
            controls=[
                Container(
                    width=500,
                    padding=40,
                    bgcolor=primary_colors['WHITE'],
                    border_radius=15,
                    content=Column(
                        horizontal_alignment="center",
                        controls=[
                            Text(
                                value="Название сайта",
                                size=18,
                                color="black",
                                text_align="center",
                            ),
                            self.login_box,
                            self.password_box,
                            Container(height=0),
                            ElevatedButton(
                                bgcolor=primary_colors['GREEN'],
                                width=450,
                                height=60,
                                text="Войти",
                                color=primary_colors['WHITE'],
                                on_click=self.login,
                            ),
                            self.error_box,
                        ],
                    ),
                )
            ],
        )

    def login(self, e):
        cursor = connection.cursor()
        query_select = "SELECT user_id, login, password FROM users;"
        cursor.execute(query_select)
        results = cursor.fetchall()
        for row in results:
            if (self.login_box.content.value == row[1] and self.password_box.content.value == row[2]):
                self.page.session.set("user_id", row[1])
                self.page.go("/home")
            else:
                self.error_box.content.value = "Вы ввели неверный логин или пароль!"
                if self.page is not None:
                    self.page.update()