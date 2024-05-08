from flet import *
from utils.consts import primary_colors
from service.connection import *

class ScheduledView(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.theme_mode = ThemeMode.LIGHT
        self.alignment = alignment.center
        self.expand = True
        self.bgcolor = primary_colors['WHITE']
#*BOX FOR TEXTFIELD
        self.textfield_box = Container(
          content=TextField(
                    hint_style=TextStyle(
                        size=12, color=primary_colors['MANATEE']
                    ),
                    label='Поле ввода',
                    cursor_color=primary_colors['MANATEE'],
                    text_style=TextStyle(
                        size=14,
                        color=primary_colors['GREEN'],
                    ),
                        ),
        )

# *HEADER
        self.content = ListView(
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
                                                      on_click=lambda x: x == self.page.go('/handbook')
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
                                                value='Просмотр плановый показателей',
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

# *MANUAL BUTTONS
                Container(
                    expand=True,
                    bgcolor=primary_colors['WHITE'],
                    content=Column(
                        expand=True,
                        horizontal_alignment='center',
                        controls=[
  # *1ST ROW (TEXTFILED AND BUTTON)
                            Container(height=50),
                            Container(
                                Row(
                                    spacing='50',
                                    alignment='center',
                                    controls=[
                                        Container(width=90),
                                        self.textfield_box,
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
                                                        # Text(
                                                        #     value='Добавить',
                                                        #     size=16,
                                                        #     color=primary_colors['WHITE'],
                                                        #     text_align='center',
                                                        #     weight='bold',
                                                        # )
                                                    )
                                                ]
                                            ),
                                            # on_click=lambda x: x == self.page.go('/home')
                                            # on_click=self.insert_into_db,
                                        )
                                    ]
                                )
                            ),

  # *2ND ROW (DATATABLE)
                            Container(
                                content=DataTable(
                                    columns=[
                                        DataColumn(Text("п/п"), numeric=True),
                                        DataColumn(Text("Наименование показателя")),
                                        DataColumn(Text("Код специалиста")),
                                        DataColumn(Text("Ед.изм.")),
                                        DataColumn(Text("1 кв."), numeric=True),
                                        DataColumn(Text("2 кв."), numeric=True),
                                        DataColumn(Text("3 кв."), numeric=True),
                                        DataColumn(Text("4 кв."), numeric=True),
                                        DataColumn(Text("год")),
                                        DataColumn(Text("Вес КПЭ 1 кв."), numeric=True),
                                        DataColumn(Text("Вес КПЭ 2 кв."), numeric=True),
                                        DataColumn(Text("Вес КПЭ 3 кв."), numeric=True),
                                        DataColumn(Text("Вес КПЭ 4 кв."), numeric=True),
                                        DataColumn(Text("Код пользователя"), numeric=True),
                                        DataColumn(Text("Дата"), numeric=True),
                                        DataColumn(Text("Номер"), numeric=True),
                                    ],
                                    rows=[],  # Leave this empty for now
                                    border=border.all(1, primary_colors['BLACK']),
                                    vertical_lines=border.BorderSide(1, primary_colors['BLACK']),
                                    horizontal_lines=border.BorderSide(1, primary_colors['BLACK']),
                                    sort_column_index=0,
                                    sort_ascending=True,
                                    heading_row_color=colors.BLACK12,
                                    heading_row_height=100,
                                    data_row_max_height=100,
                                    width=2000
                                ),
                                alignment=alignment.center,
                                padding=padding.all(20),
                            ),
                            Container(height=50),
                        ],
                    )
                ),
            ]
        )
        cursor = connection.cursor()
        query_select = """
            SELECT
                pv.plan_id,
                ni.name AS indicator_name,
                pv.plan_specialist_id,
                um.type AS unit_of_measurement,
                pv.1st_quater_value,
                pv.2nd_quater_value,
                pv.3rd_quater_value,
                pv.4th_quater_value,
                pv.year,
                pv.KPE_weight_1,
                pv.KPE_weight_2,
                pv.KPE_weight_3,
                pv.KPE_weight_4,
                pv.plan_user_id,
                pv.date,
                pv.number
            FROM planned_value AS pv
            JOIN name_of_indicators AS ni ON pv.plan_indicators_id = ni.indicators_id
            JOIN units_of_measurement AS um ON pv.plan_units_id = um.measurement_id
            ORDER BY pv.plan_id;
        """
        
        cursor.execute(query_select)
        results = cursor.fetchall()

        query_result = results

        data_rows = []

        for row in query_result:
            cells = [DataCell(Text(str(value))) for value in row]
            data_row = DataRow(cells=cells)
            data_rows.append(data_row)

        self.content.controls[1].content.controls[2].content.rows = data_rows
        page.update()

