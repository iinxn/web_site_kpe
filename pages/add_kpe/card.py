from flet import *
from utils.colors import * 

class Card(Container):
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
                                  # width=200,   
                                  bgcolor='white',
                                  width=70,
                                  height=70,
                                  border_radius=50,
                                  content=IconButton(
                                      icons.ARROW_BACK_OUTLINED,
                                      icon_color='#5B7553',
                                      icon_size=30,
                                      on_click=lambda x: x == self.page.go('/home')
                                  )
                                ),
                                Container(
                                    content=Text(
                                    value='Заполнить карту КПЭ',
                                    size=18,
                                    color='white',
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
                    bgcolor='white',
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
                                  color=white,
                                  bgcolor='#5B7553',
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
                                            color=white,
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
                                  color=white,
                                  bgcolor='#5B7553',
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
                                            color=white,
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
                                  color=white,
                                  bgcolor='#5B7553',
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
                                            color=white,
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