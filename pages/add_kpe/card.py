from flet import *
from utils.consts import primary_colors 

class Card(Container):
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
                        horizontal_alignment='center',  # Align the text to the right
                        controls=[
                          Container(
                            # alignment='center',
                            content=Row(
                              alignment='spaceBetween',
                              controls=[
                                Container(
                                  # width=200,   
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
                                    value='Заполнить карту КПЭ',
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
                            Row(
                              alignment='center',
                              # horizontal_alignment='center',
                              controls=[
                                Container(height=500), #space between buttons
                                
                                #buttons
                                ElevatedButton(
                                  # text='Заполнить карту КПЭ',
                                  color=primary_colors['WHITE'],
                                  bgcolor=primary_colors['GREEN'],
                                  width=400,
                                  height=200,
                                  content=Column(
                                    horizontal_alignment='center',
                                    alignment='center',
                                      controls=[
                                        Container(
                                          Text(
                                            value='Ввести карту КПЭ',
                                            size=16,
                                            color=primary_colors['WHITE'],
                                            text_align='center',
                                            weight='bold',
                                          )
                                        )
                                      ]
                                  ),
                                  on_click=lambda x: x == self.page.go('/scheduled')
                                ),
                                
                                ElevatedButton(
                                  # text='Заполнить карту КПЭ',
                                  color=primary_colors['WHITE'],
                                  bgcolor=primary_colors['GREEN'],
                                  width=400,
                                  height=200,
                                  content=Column(
                                    horizontal_alignment='center',
                                    alignment='center',
                                      controls=[
                                        Container(
                                          Text(
                                            value='Ввести изменение в карту КПЭ',
                                            size=16,
                                            color=primary_colors['WHITE'],
                                            text_align='center',
                                            weight='bold',
                                          )
                                        )
                                      ]
                                  ),
                                  on_click=lambda x: x == self.page.go('/edit_kpe')
                                ),
                                
                                # Container(height=0),
                                ElevatedButton(
                                  color=primary_colors['WHITE'],
                                  bgcolor=primary_colors['GREEN'],
                                  width=400,
                                  height=200,
                                  content=Column(
                                    horizontal_alignment='center',
                                    alignment='center',
                                      controls=[
                                        Container(
                                          Text(
                                            value='Ввести результат исполнения мероприятий КПЭ',
                                            size=16,
                                            color=primary_colors['WHITE'],
                                            text_align='center',
                                            weight='bold',
                                          )
                                        )
                                      ]
                                  ),
                                  on_click=lambda x: x == self.page.go('/actual')
                                ),
                              ]
                            )
                          ),
                          Container(
                            content=Row(
                              controls=[
                                Container(
                                  bgcolor=primary_colors['WHITE']
                                )
                              ]
                            )
                          )  
                      ],
                  )
                ),
            ]
        )