from flet import *
from utils.consts import primary_colors

class Handbook(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.alignment = alignment.center
        self.expand = True
        self.bgcolor = primary_colors['WHITE']
        user_id = self.page.session.get("login")
        
        self.right_handbook_button = None
        self.user_handbook_button = None
        self.scheduled_view_handbook_button = None
        
        if user_id == 'admin':
          self.user_handbook_button = ElevatedButton(
            color=primary_colors['WHITE'],
            bgcolor=primary_colors['GREEN'],
            width=500,
            height=70,
            content=Column(
              horizontal_alignment='center',
              alignment='center',
                controls=[
                  Container(
                    Text(
                      value='Пользователи',
                      size=16,
                      color=primary_colors['WHITE'],
                      text_align='center',
                      weight='bold',
                    )
                  )
                ]
            ),
            on_click=lambda x: x == self.page.go('/users')
          )
          self.right_handbook_button = ElevatedButton(
            color=primary_colors['WHITE'],
            bgcolor=primary_colors['GREEN'],
            width=500,
            height=70,
            content=Column(
              horizontal_alignment='center',
              alignment='center',
                controls=[
                  Container(
                    Text(
                      value='Права доступа',
                      size=16,
                      color=primary_colors['WHITE'],
                      text_align='center',
                      weight='bold',
                    )
                  )
                ]
            ),
            # on_click=lambda x: x == self.page.go('/add')
          )
          self.scheduled_view_handbook_button = ElevatedButton(
            color=primary_colors['WHITE'],
            bgcolor=primary_colors['GREEN'],
            width=500,
            height=70,
            content=Column(
              horizontal_alignment='center',
              alignment='center',
                controls=[
                  Container(
                    Text(
                      value='Плановые показатели',
                      size=16,
                      color=primary_colors['WHITE'],
                      text_align='center',
                      weight='bold',
                    )
                  )
                ]
            ),
            on_click=lambda x: x == self.page.go('/scheduled_handbook')
          )
        else:
          self.user_handbook_button = Container()
          self.right_handbook_button = Container()
          self.scheduled_view_handbook_button = Container()

        #header
        self.content = Column(
            spacing=0,
            controls=[
                Container(
                    width=8000,
                    padding=40,
                    bgcolor=primary_colors['GREEN'],
                    # border_radius=15,
                    content=Column(
                        horizontal_alignment='center',  # Align the text to the right
                        controls=[
                          Container(
                            # alignment='center',
                            content=Row(
                              alignment='spaceBetween',
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
                                      on_click=lambda x: x == self.page.go('/home')
                                  )
                                ),
                                Container(
                                    content=Text(
                                    value='Справочник',
                                    size=18,
                                    color=primary_colors['WHITE'],
                                    text_align='center',
                                  ),
                                ),
                                Container(width=70),
                              ]
                            )
                          )
                        ],
                    )
                ),

                #manual buttons
                Container(
                    expand=True,
                    bgcolor=primary_colors['WHITE'],
                    content=Column(
                      expand=True,
                      # alignment='center',
                      horizontal_alignment='center',
                      controls=[
                          Container(
                            padding=padding.only(left=20),
                            content=Column(
                              # alignment='center',
                              horizontal_alignment='left',
                              controls=[
                                Container(height=40), #space between buttons
#*UNITS OF MEASUREMENT
                                #buttons
                                ElevatedButton(
                                  # text='Заполнить карту КПЭ',
                                  color=primary_colors['WHITE'],
                                  bgcolor=primary_colors['GREEN'],
                                  width=500,
                                  height=70,
                                  content=Column(
                                    horizontal_alignment='center',
                                    alignment='center',
                                      controls=[
                                        Container(
                                          
                                          Text(
                                            value='Единицы измерения',
                                            size=16,
                                            color=primary_colors['WHITE'],
                                            text_align='center',
                                            weight='bold',
                                          )
                                        )
                                      ]
                                  ),
                                  on_click=lambda x: x == self.page.go('/measurement_handbook')
                                ),
#*NAME OF DEPARTMENT BUTTON
                                Container(height=0),
                                ElevatedButton(
                                  color=primary_colors['WHITE'],
                                  bgcolor=primary_colors['GREEN'],
                                  width=500,
                                  height=70,
                                  content=Column(
                                    horizontal_alignment='center',
                                    alignment='center',
                                      controls=[
                                        Container(
                                          Text(
                                            value='Наименование управления',
                                            size=16,
                                            color=primary_colors['WHITE'],
                                            text_align='center',
                                            weight='bold',
                                          )
                                        )
                                      ]
                                  ),
                                  on_click=lambda x: x == self.page.go('/department')
                                ),
#*NAME OF INDICATORS
                                Container(height=0),
                                ElevatedButton(
                                  color=primary_colors['WHITE'],
                                  bgcolor=primary_colors['GREEN'],
                                  width=500,
                                  height=70,
                                  content=Column(
                                    horizontal_alignment='center',
                                    alignment='center',
                                      controls=[
                                        Container(
                                          Text(
                                            value='Наименование показателей',
                                            size=16,
                                            color=primary_colors['WHITE'],
                                            text_align='center',
                                            weight='bold',
                                          )
                                        )
                                      ]
                                  ),
                                  on_click=lambda x: x == self.page.go('/add')
                                ),
#*SPECIALISTS BUTTON
                                Container(height=0),
                                ElevatedButton(
                                  color=primary_colors['WHITE'],
                                  bgcolor=primary_colors['GREEN'],
                                  width=500,
                                  height=70,
                                  content=Column(
                                    horizontal_alignment='center',
                                    alignment='center',
                                      controls=[
                                        Container(
                                          Text(
                                            value='Специалисты',
                                            size=16,
                                            color=primary_colors['WHITE'],
                                            text_align='center',
                                            weight='bold',
                                          )
                                        )
                                      ]
                                  ),
                                  on_click=lambda x: x == self.page.go('/specialists_handbook')
                                ),
#*USERS
                                Container(height=0),
                                self.user_handbook_button,
#*RIGHTS BUTTON
                                Container(height=0),
                                self.right_handbook_button,
#*SCHEDULED VIEW
                                Container(height=0),
                                self.scheduled_view_handbook_button
                              ]
                            )
                          ), 
                      ],
                  )
                ),
            ]
        )