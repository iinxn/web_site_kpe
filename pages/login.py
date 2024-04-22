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
                                value="Мастер КПЭ",
                                size=18,
                                color=primary_colors['GREEN'],
                                text_align="center",
                                weight='bold',
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
        try:
            login_value = self.login_box.content.value.replace("'", "''")
            password_value = self.password_box.content.value.replace("'", "''")

            cursor = connection.cursor()
            query_select = f"SELECT login FROM users WHERE login = '{login_value}' AND password = '{password_value}';"
            
            cursor.execute(query_select)
            result = cursor.fetchone()

            if result:
                self.page.session.set("login", result[0])
                self.page.go("/home")
            else:
                self.error_box.content.value = "Вы ввели неверный логин или пароль!"
                self.page.update()

        except Exception as error:
            self.error_box.content.value = "Ошибка при попытке входа!"
            self.page.update()
            print(f"Login error: {error}")
