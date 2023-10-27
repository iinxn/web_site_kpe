from flet import *
from utils.colors import * 
from service.connection import *

class ScheduledView(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.theme_mode = ThemeMode.LIGHT
        self.alignment = alignment.center
        self.expand = True
        self.bgcolor = tea_green
#*BOX FOR TEXTFIELD
        self.textfield_box = Container(
          content=TextField(
                    hint_style=TextStyle(
                        size=12, color='#858796'
                    ),
                    label='Поле ввода',
                    cursor_color='#858796',
                    text_style=TextStyle(
                        size=14,
                        color='#5B7553',
                    ),
                        ),
        )

# *HEADER
        self.content = Column(
            spacing=0,
            scroll=True,
            controls=[
                Container(
                    width=8000,
                    padding=40,
                    bgcolor='#5B7553',
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
                                                  bgcolor='white',
                                                  width=70,
                                                  height=70,
                                                  border_radius=50,
                                                  content=IconButton(
                                                      icons.ARROW_BACK_OUTLINED,
                                                      icon_color='#5B7553',
                                                      icon_size=30,
                                                      on_click=lambda x: x == self.page.go('/handbook')
                                                  )
                                              ),
                                              Container(
                                                  bgcolor='white',
                                                  width=70,
                                                  height=70,
                                                  border_radius=50,
                                                  content=IconButton(
                                                      icons.HOME,
                                                      icon_color='#5B7553',
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
                                                color='white',
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
                    bgcolor='white',
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
                                            color=white,
                                            bgcolor='#5B7553',
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
                                                        #     color=white,
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
                                        DataColumn(Text("ФИО специалиста")),
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
                                        DataColumn(Text("Номер версии"), numeric=True),
                                    ],
                                    rows=[],  # Leave this empty for now
                                    border=border.all(1, "black"),
                                    vertical_lines=border.BorderSide(1, "black"),
                                    horizontal_lines=border.BorderSide(1, "black"),
                                    sort_column_index=0,
                                    sort_ascending=True,
                                    heading_row_color=colors.BLACK12,
                                    heading_row_height=100,
                                    # width=1000
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
                  pv.plan_user_id,
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
                  pv.number_of_version
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

