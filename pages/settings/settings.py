from flet import *
from utils.colors import * 

class Settings(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.alignment = alignment.center
        self.expand = True
        self.bgcolor = tea_green
        
        #header
        self.content = Column(
            spacing=0,
            controls=[
                Container(
                    width=8000,
                    padding=40,
                    bgcolor='#5B7553',
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
                                ),
                                Container(
                                    content=Text(
                                    value='Настройки',
                                    size=18,
                                    color='white',
                                    text_align='center',
                                  ),
                                ),
                                Container(
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
                    bgcolor='white',
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
                                
                                #buttons
                                ElevatedButton(
                                  # text='Заполнить карту КПЭ',
                                  color=white,
                                  bgcolor='#5B7553',
                                  width=500,
                                  height=70,
                                  content=Column(
                                    horizontal_alignment='center',
                                    alignment='center',
                                      controls=[
                                        Container(
                                          
                                          Text(
                                            value='Смена темы',
                                            size=16,
                                            color=white,
                                            text_align='center',
                                            weight='bold',
                                          )
                                        )
                                      ]
                                  ),
                                  # on_click=lambda x: x == self.page.go('/card')
                                ),
                                
                                Container(height=0),
                                ElevatedButton(
                                  color=white,
                                  bgcolor='#5B7553',
                                  width=500,
                                  height=70,
                                  content=Column(
                                    horizontal_alignment='center',
                                    alignment='center',
                                      controls=[
                                        Container(
                                          Text(
                                            value='Согласование',
                                            size=16,
                                            color=white,
                                            text_align='center',
                                            weight='bold',
                                          )
                                        )
                                      ]
                                  ),
                                  # on_click=lambda x: x == self.page.go('/login')
                                ),
                                
                                Container(height=0),
                                ElevatedButton(
                                  color=white,
                                  bgcolor='#5B7553',
                                  width=500,
                                  height=70,
                                  content=Column(
                                    horizontal_alignment='center',
                                    alignment='center',
                                      controls=[
                                        Container(
                                          Text(
                                            value='Мониторинг',
                                            size=16,
                                            color=white,
                                            text_align='center',
                                            weight='bold',
                                          )
                                        )
                                      ]
                                  ),
                                  on_click=lambda x: x == self.page.go('/monitoring')
                                ),
                              ]
                            )
                          ), 
                      ],
                  )
                ),
            ]
        )