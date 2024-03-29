from flet import *
from utils.consts import primary_colors

class Home(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.alignment = alignment.center
        self.expand = True
        self.bgcolor = primary_colors['GREEN']
        
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
                        horizontal_alignment='center',
                        controls=[
                          Container(
                            content=Row(
                              alignment='spaceBetween',
                              controls=[
                                Container(
                                  bgcolor=primary_colors['WHITE'],
                                  
                                  border_radius=30,
                                  padding=20,
                                  content=Text(
                                    value='Добро пожаловать user',
                                    size=16,
                                    color=primary_colors['GREEN'],
                                    text_align='center',
                                    weight='bold',
                                  ),
                                ),
                                Container(
                                    content=Text(
                                    value='Название сайта',
                                    size=18,
                                    color='white',
                                    text_align='center',
                                  ),
                                ),
                                Container(
                                    ElevatedButton(
                                    color=primary_colors['WHITE'],
                                    bgcolor=primary_colors['WHITE'],
                                    width=200,
                                    height=70,
                                    content=Column(
                                      horizontal_alignment='center',
                                      alignment='center',
                                        controls=[
                                          Container(
                                            
                                            Text(
                                              value='Настройки',
                                              size=16,
                                              color=primary_colors['GREEN'],
                                              text_align='center',
                                              weight='bold',
                                            )
                                          )
                                        ]
                                    ),
                                    on_click=lambda x: x == self.page.go('/settings')
                                  ),
                                ),
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
                            Column(
                              alignment='center',
                              horizontal_alignment='center',
                              controls=[
                                Container(height=200), #space between buttons
                                
                                #buttons
                                ElevatedButton(
                                  # text='Заполнить карту КПЭ',
                                  color=primary_colors['WHITE'],
                                  bgcolor=primary_colors['GREEN'],
                                  width=700,
                                  height=70,
                                  content=Column(
                                    horizontal_alignment='center',
                                    alignment='center',
                                      controls=[
                                        Container(
                                          
                                          Text(
                                            value='Заполнить карту КПЭ',
                                            size=16,
                                            color=primary_colors['WHITE'],
                                            text_align='center',
                                            weight='bold',
                                          )
                                        )
                                      ]
                                  ),
                                  on_click=lambda x: x == self.page.go('/card')
                                ),
                                
                                Container(height=0),
                                ElevatedButton(
                                  color=primary_colors['WHITE'],
                                  bgcolor=primary_colors['GREEN'],
                                  width=700,
                                  height=70,
                                  content=Column(
                                    horizontal_alignment='center',
                                    alignment='center',
                                      controls=[
                                        Container(
                                          Text(
                                            value='Отчеты',
                                            size=16,
                                            color=primary_colors['WHITE'],
                                            text_align='center',
                                            weight='bold',
                                          )
                                        )
                                      ]
                                  ),
                                  on_click=lambda x: x == self.page.go('/report')
                                ),
                                
                                Container(height=0),
                                ElevatedButton(
                                  color=primary_colors['WHITE'],
                                  bgcolor=primary_colors['GREEN'],
                                  width=700,
                                  height=70,
                                  content=Column(
                                    horizontal_alignment='center',
                                    alignment='center',
                                      controls=[
                                        Container(
                                          Text(
                                            value='Справочник',
                                            size=16,
                                            color=primary_colors['WHITE'],
                                            text_align='center',
                                            weight='bold',
                                          )
                                        )
                                      ]
                                  ),
                                  on_click=lambda x: x == self.page.go('/handbook')
                                ),
                              ]
                            )
                          ),
                          Container(
                            content=Row(
                              controls=[
                                Container(
                                  bgcolor='black'
                                )
                              ]
                            )
                          )  
                      ],
                  )
                ),
            ]
        )