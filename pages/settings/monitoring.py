from flet import *
from utils.consts import primary_colors

class Monitoring(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.theme_mode = ThemeMode.LIGHT
        self.alignment = alignment.center
        self.expand = True
        self.bgcolor = primary_colors['GREEN']
        self.content = Column(
          spacing=0,
          controls=[
            Container(
              width=8000,
              padding=40,
              bgcolor=primary_colors['GREEN'],
              content=Column(
                  horizontal_alignment='center',
                  controls=[
                    Container(
                      content=Row(
                        alignment='spaceBetween',
                        controls=[
                          Container(
                            width=200,
                            content=Row(
                            spacing=10,
                            controls=[
                                Container(
                                  bgcolor=primary_colors['WHITE'],
                                  width=70,
                                  height=70,
                                  border_radius=50,
                                  content=IconButton(
                                      icons.ARROW_BACK_OUTLINED,
                                      icon_color=primary_colors['GREEN'],
                                      icon_size=30,
                                      on_click=lambda x: x == self.page.go('/settings')
                                  )
                                ),
                                Container(
                                  bgcolor=primary_colors['WHITE'],
                                  width=70,
                                  height=70,
                                  border_radius=50,
                                  content=IconButton(
                                      icons.HOME,
                                      icon_color=primary_colors['GREEN'],
                                      icon_size=30,
                                      on_click=lambda x: x == self.page.go('/home')
                                  )
                                ),
                              ]
                            )
                          ),
                          Container(
                            content=Text(
                            value='Мониторинг',
                            size=18,
                            color=primary_colors['WHITE'],
                            text_align='center',
                            ),
                          ),
                          Container(width=200),
                        ]
                      )
                    )
                  ],
              )
            ),
            Container(
              expand=True,
              bgcolor=primary_colors['WHITE'],
              content=Column(
                expand=True,
                horizontal_alignment='center',
                controls=[
                  #! First Row
                  Container(height=50),
                  Container(
                    Row(
                      spacing='50',
                      alignment='center',
                      controls=[
                        #! Columns
                      ]
                    )
                  ),
                  #! Second Row
                  Container(),
                ],
              )
            ),
          ]
      )