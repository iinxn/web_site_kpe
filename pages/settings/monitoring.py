from flet import *
from utils.consts import primary_colors

class Monitoring(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page  # Initialize the self.page object
        self.page.theme_mode = ThemeMode.LIGHT  # Set the theme mode
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
                                Container(),
                                Container(
                                    content=Text(
                                    value='Мониторинг',
                                    size=18,
                                    color=primary_colors['WHITE'],
                                    text_align='center',
                                  ),
                                ),
                                Container(),
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
                        #1st row
                          Container(height=50),
                          Container(
                            Row(
                              spacing='50',
                              alignment='center',
                              # horizontal_alignment='center',
                              controls=[
                                Dropdown(
                                    # label='Специалист',
                                    hint_text='Выберите пользователя',
                                    # hint_style=TextStyle(
                                    #   size=14, color='#858796'
                                    # ),
                                    # color=primary_colors['GREEN'],
                                    # content_padding=30,
                                    options=[
                                      dropdown.Option('Пользователь 1'),
                                      dropdown.Option('Пользователь 2'),
                                      dropdown.Option('Пользователь 3'),
                                    ]
                                  ),
                                  Container(width=90),
                                #dropdown 1st row
                                  #specialist
                                  # TextField(
                                  #     hint_style=TextStyle(
                                  #       size=12, color='#858796'
                                  #     ),
                                  #     label='',
                                  #     cursor_color='#858796',
                                  #     text_style=TextStyle(
                                  #       size=14,
                                  #       color=primary_colors['GREEN'],
                                  #     ),
                                  #     # width=400,
                                  # ),
                                  ElevatedButton(
                                    color=primary_colors['WHITE'],
                                    bgcolor=primary_colors['GREEN'],
                                    width=400,
                                    height=70,
                                    content=Column(
                                      horizontal_alignment='center',
                                      alignment='center',
                                        controls=[
                                          Container(
                                            Text(
                                              value='Посмотреть',
                                              size=16,
                                              color=primary_colors['WHITE'],
                                              text_align='center',
                                              weight='bold',
                                            )
                                          )
                                        ]
                                    ),
                                    on_click=lambda x: x == self.page.go('/home') 
                                  )
                              ]
                            )
                          ), 
                          
                          # Container(height=50),
                          #2nd row
                          Container(
                            content=DataTable(
                                columns=[
                                    DataColumn(Text("Номер"), numeric=True),
                                    DataColumn(Text("История")),
                                ],
                                rows=[
                                    DataRow(
                                        cells=[
                                            DataCell(Text("1")),
                                            DataCell(Text("Пользователь создал новые объект в спавочнике")),
                                        ],
                                        on_select_changed=lambda e: print("На запись можноназать")
                                    )
                                ],
                                border=border.all(1, primary_colors['BLACK']),
                                vertical_lines=border.BorderSide(1, primary_colors['BLACK']),
                                horizontal_lines=border.BorderSide(1, primary_colors['BLACK']),
                                sort_column_index=0,
                                sort_ascending=True,
                                heading_row_color=colors.BLACK12,
                                heading_row_height=100,
                                width=1000
                            ),
                            alignment=alignment.center,
                            # horizontal_alignment='center',
                            padding=padding.all(20),
                          ),
                          Container(height=50),
                          #4th row
                          
                      ],
                  )
                ),
            ]
        )