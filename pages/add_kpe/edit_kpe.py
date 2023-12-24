import datetime
from flet import *
from service.connection import *
from utils.colors import *


class EditKPE(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.theme_mode = ThemeMode.LIGHT
        self.alignment = alignment.center
        self.expand = True
        self.bgcolor = tea_green

        self.selected_rows = set()
        self.sql_query = []
        self.data_table = DataTable(
            columns=[
                DataColumn(Text("п/п"), numeric=True),
                DataColumn(Text("Наименование показателя")),
                DataColumn(Text("Ед.изм.")),
                DataColumn(Text("""1
кв."""), numeric=True),
                DataColumn(Text("""2
кв."""), numeric=True),
                DataColumn(Text("""3
кв."""), numeric=True),
                DataColumn(Text("""4
кв."""), numeric=True),
                DataColumn(Text("год")),
                DataColumn(Text("""   Вес КПЭ 
1 кв."""), numeric=True),
                DataColumn(Text("""   Вес КПЭ 
2 кв."""), numeric=True),
                DataColumn(Text("""   Вес КПЭ 
3 кв."""), numeric=True),
                DataColumn(Text("""   Вес КПЭ 
4 кв."""), numeric=True),
                DataColumn(Text("Выбор")),
            ],
            rows=[],
            border=border.all(1, "black"),
            vertical_lines=border.BorderSide(1, "black"),
            horizontal_lines=border.BorderSide(1, "black"),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=colors.BLACK12,
            heading_row_height=100,
            width=2000
        )

        self.dropdown_options_indicators_truncated = []
        dropdown_options_specialists_1 = []
        dropdown_options_specialists_2 = []
        # * SPECIALIST ARRAY
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT full_name FROM specialists ORDER BY specialist_id')
            results = cursor.fetchall()

            for row in results:
                dropdown_options_specialists_1.append(dropdown.Option(row[0]))
                dropdown_options_specialists_2.append(dropdown.Option(row[0]))
        except Exception as e:
            print(f"Error fetching data from the database: {str(e)}")

        # * NAME OF INDICATORA ARRAY
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT name FROM name_of_indicators ORDER BY indicators_id')
            results = cursor.fetchall()
            max_length = 40
            for row in results:
                truncated_text = row[0] if len(row[0]) <= max_length else row[0][:max_length] + "..."
                self.dropdown_options_indicators_truncated.append(dropdown.Option(truncated_text))

            self.dropdown_options_indicators_truncated.append(dropdown.Option('Нет в списке'))
        except Exception as e:
            print(f"Error fetching data from the database: {str(e)}")

        # *DROPDOWNS
        self.report_spec = Container(
            content=Dropdown(
                hint_text='Выберите специалиста',
                color='black',
                options=dropdown_options_specialists_1
            )
        )
        self.specialist_menu_box = Container(
            content=Dropdown(
                hint_text='Выберите специалиста',
                color='black',
                options=dropdown_options_specialists_2
            )
        )
        self.first_qr_box = Container(
            content=TextField(
                hint_style=TextStyle(
                    size=12, color='#858796'
                ),
                label='1 квартал',
                cursor_color='#858796',
                text_style=TextStyle(
                    size=14,
                    color='#5B7553',
                ),
                width=100
            ),
        )
        self.second_qr_box = Container(
            content=TextField(
                hint_style=TextStyle(
                    size=12, color='#858796'
                ),
                label='2 квартал',
                cursor_color='#858796',
                text_style=TextStyle(
                    size=14,
                    color='#5B7553',
                ),
                width=100
            ),
        )
        self.third_qr_box = Container(
            content=TextField(
                hint_style=TextStyle(
                    size=12, color='#858796'
                ),
                label='3 квартал',
                cursor_color='#858796',
                text_style=TextStyle(
                    size=14,
                    color='#5B7553',
                ),
                width=100
            ),
        )
        self.fourtht_qr_box = Container(
            content=TextField(
                hint_style=TextStyle(
                    size=12, color='#858796'
                ),
                label='4 квартал',
                cursor_color='#858796',
                text_style=TextStyle(
                    size=14,
                    color='#5B7553',
                ),
                width=100
            ),
        )
        self.year_box = Container(
            content=TextField(
                hint_style=TextStyle(
                    size=12, color='#858796'
                ),
                label='Год',
                cursor_color='#858796',
                text_style=TextStyle(
                    size=14,
                    color='#5B7553',
                ),
                width=100
            ),
        )
        self.weight_first_qr_box = Container(
            content=TextField(
                hint_style=TextStyle(
                    size=12, color='#858796'
                ),
                label='Вес 1 кв.',
                cursor_color='#858796',
                text_style=TextStyle(
                    size=14,
                    color='#5B7553',
                ),
                width=100
            ),
        )
        self.weight_second_qr_box = Container(
            content=TextField(
                hint_style=TextStyle(
                    size=12, color='#858796'
                ),
                label='Вес 2 кв.',
                cursor_color='#858796',
                text_style=TextStyle(
                    size=14,
                    color='#5B7553',
                ),
                width=100
            ),
        )
        self.weight_third_qr_box = Container(
            content=TextField(
                hint_style=TextStyle(
                    size=12, color='#858796'
                ),
                label='Вес 3 кв.',
                cursor_color='#858796',
                text_style=TextStyle(
                    size=14,
                    color='#5B7553',
                ),
                width=100
            ),
        )
        self.weight_fourth_qr_box = Container(
            content=TextField(
                hint_style=TextStyle(
                    size=12, color='#858796'
                ),
                label='Вес 4 кв.',
                cursor_color='#858796',
                text_style=TextStyle(
                    size=14,
                    color='#5B7553',
                ),
                width=100
            ),
        )
        self.cb_menu_spec = Container(
            content=Dropdown(
                label='Выберите наименование показателя',
                color="black",
                width=350,
                options=self.dropdown_options_indicators_truncated,
                on_change=self.added_new_to_indicators
            ),
        )
        self.textfiled_input_new_indicator = Container(
            content=TextField(
                label="Введите наименование показателя",
                hint_style=TextStyle(
                    size=12, color='#858796'
                ),
                cursor_color='#858796',
                text_style=TextStyle(
                    size=14,
                    color='black',
                ),
                width=100
            ),
        )

        # *ALTERDIALOGS
        self.alter_dialog_block = AlertDialog(
            modal=True,
            actions=[TextButton("OK", on_click=self.close_dlg_block)],
            on_dismiss=lambda e: print("Modal dialog dismissed!")
        )
        self.alter_dialog_are_you_sure = AlertDialog(
            modal=True,
            title=Text("Подтверждение"),
            content=Text("Вы точно уверены?"),
            actions=[
                TextButton("Да", on_click=self.insert_all_data_from_array),
                TextButton("Нет", on_click=self.close_are_you_sure_dialoge)
            ]
        )
        self.alter_dialog_edit = AlertDialog(
            modal=True,
            title=Text(
                value="Изменить строку",
                size=16,
                color='#5B7553',
                text_align='center',
                weight='bold',
                width=60
            ),
            content=Column(
                height=300,
                width=800,
                controls=[
                    Container(
                        Row(
                            spacing='50',
                            alignment='center',
                            controls=[

                            ]
                        )
                    ),
                    Container(height=50),
                    # *2ND ROW
                    Container(
                        Row(
                            spacing='50',
                            alignment='center',
                            controls=[
                                Text(
                                    value='План',
                                    size=16,
                                    color='#5B7553',
                                    text_align='center',
                                    weight='bold',
                                    width=60
                                ),
                                # *Name of indicator
                                self.first_qr_box,
                                self.second_qr_box,
                                self.third_qr_box,
                                self.fourtht_qr_box,
                                self.year_box,
                            ]
                        )
                    ),
                    Container(height=50),
                    # *3RD ROW
                    Container(
                        Row(
                            spacing='50',
                            alignment='center',
                            controls=[
                                Text(
                                    value='Вес КПЭ',
                                    size=16,
                                    color='#5B7553',
                                    text_align='center',
                                    weight='bold',
                                ),
                                self.weight_first_qr_box,
                                self.weight_second_qr_box,
                                self.weight_third_qr_box,
                                self.weight_fourth_qr_box,
                            ]
                        )
                    ),
                ]
            ),

            actions=[
                TextButton("Изменить", on_click=self.edit_name_in_table),
                TextButton("Закрыть", on_click=self.close_edit_dialog),
            ],
            actions_alignment=MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        self.alter_dialog_add_new = AlertDialog(
            modal=True,
            title=Text(
                value="Добавить новую запись",
                size=16,
                text_align='center',
                weight='bold',
                width=60,
                color='#5B7553'
            ),
            content=Column(
                height=300,
                width=1000,
                controls=[
                    Container(
                        Row(
                            spacing='50',
                            alignment='center',
                            controls=[
                                self.cb_menu_spec,
                                # self.specialist_menu_box
                            ]
                        )
                    ),
                    Container(height=50),
                    # *2ND ROW
                    Container(
                        Row(
                            spacing='50',
                            alignment='center',
                            controls=[
                                Text(
                                    value='План',
                                    size=16,
                                    color='#5B7553',
                                    text_align='center',
                                    weight='bold',
                                    width=60
                                ),
                                # *Name of indicator
                                self.first_qr_box,
                                self.second_qr_box,
                                self.third_qr_box,
                                self.fourtht_qr_box,
                                self.year_box,
                            ]
                        )
                    ),

                    Container(height=50),
                    # *3RD ROW
                    Container(
                        Row(
                            spacing='50',
                            alignment='center',
                            controls=[
                                Text(
                                    value='Вес КПЭ',
                                    size=16,
                                    color='#5B7553',
                                    text_align='center',
                                    weight='bold',
                                ),
                                self.weight_first_qr_box,
                                self.weight_second_qr_box,
                                self.weight_third_qr_box,
                                self.weight_fourth_qr_box,
                            ]
                        )
                    ),
                ]
            ),
            actions=[
                TextButton("Добавить", on_click=self.add_new_specialist),
                TextButton("Закрыть", on_click=self.close_new_kpe_dialog),
            ],
            actions_alignment=MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        self.alter_dialog_no_in_list = AlertDialog(
            modal=True,
            title=Text("Добавление показателя в справочник"),
            content=self.textfiled_input_new_indicator,
            actions=[
                TextButton("Добавить", on_click=self.alter_dialoge_input_data),
                TextButton("Назад", on_click=self.close_dlg_new_indicator),
            ],
            actions_alignment=MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),

        )

        # *HEADER
        self.content = Column(
            spacing=0,
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
                                                            on_click=lambda x: x == self.page.go('/card')
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
                                                value='Ввести изменение в карту КПЭ',
                                                size=18,
                                                color='white',
                                                text_align='center',
                                            ),
                                        ),
                                        Container(
                                            width=300,
                                            content=Row(
                                                controls=[
                                                    Container(),

                                                ]
                                            )
                                        ),
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
                            Container(height=25),
                            Container(
                                content=Row(
                                    spacing='30',
                                    alignment='center',
                                    controls=[
                                        self.report_spec,
                                        Container(
                                            content=ElevatedButton(
                                                color=white,
                                                bgcolor='#5B7553',
                                                width=170,
                                                height=70,
                                                content=Column(
                                                    horizontal_alignment='center',
                                                    alignment='center',
                                                    controls=[
                                                        Container(
                                                            Text(
                                                                value='Сформировать',
                                                                size=16,
                                                                color=white,
                                                                text_align='center',
                                                                weight='bold',
                                                            )
                                                        )
                                                    ]
                                                ),
                                                on_click=self.show_kpe_table
                                            ),
                                        ),

                                        Container(width=300),
                                        Container(
                                            content=ElevatedButton(
                                                color=white,
                                                bgcolor='#5B7553',
                                                width=170,
                                                height=70,
                                                content=Column(
                                                    horizontal_alignment='center',
                                                    alignment='center',
                                                    controls=[
                                                        Container(
                                                            Text(
                                                                value='Редактировать',
                                                                size=16,
                                                                color=white,
                                                                text_align='center',
                                                                weight='bold',
                                                            )
                                                        )
                                                    ]
                                                ),
                                                on_click=lambda e: self.show_edit_dialog(),
                                            ),
                                        ),
                                        Container(
                                            content=ElevatedButton(
                                                color=white,
                                                bgcolor='#5B7553',
                                                width=170,
                                                height=70,
                                                content=Column(
                                                    horizontal_alignment='center',
                                                    alignment='center',
                                                    controls=[
                                                        Container(
                                                            Text(
                                                                value='Удалить',
                                                                size=16,
                                                                color=white,
                                                                text_align='center',
                                                                weight='bold',
                                                            )
                                                        )
                                                    ]
                                                ),
                                                on_click=self.delete_name_in_table,
                                            ),
                                        ),
                                        Container(
                                            content=ElevatedButton(
                                                color=white,
                                                bgcolor='#5B7553',
                                                width=170,
                                                height=70,
                                                content=Column(
                                                    horizontal_alignment='center',
                                                    alignment='center',
                                                    controls=[
                                                        Container(
                                                            Text(
                                                                value='Оставить без изменения',
                                                                size=16,
                                                                color=white,
                                                                text_align='center',
                                                                weight='bold',
                                                            )
                                                        )
                                                    ]
                                                ),
                                                on_click=self.stay_name_in_table,
                                            ),
                                        ),
                                        Container(
                                            content=ElevatedButton(
                                                color=white,
                                                bgcolor='#5B7553',
                                                width=170,
                                                height=70,
                                                content=Column(
                                                    horizontal_alignment='center',
                                                    alignment='center',
                                                    controls=[
                                                        Container(
                                                            Text(
                                                                value='Добавить',
                                                                size=16,
                                                                color=white,
                                                                text_align='center',
                                                                weight='bold',
                                                            )
                                                        )
                                                    ]
                                                ),
                                                on_click=self.show_add_dialog,
                                            ),
                                        ),
                                    ]
                                )
                            ),

                            # *2ND ROW (DATATABLE)
                            Container(
                                content=self.data_table,
                                alignment=alignment.center,
                                padding=padding.all(20),
                            ),
                            Container(height=50),
                            Container(
                                content=ElevatedButton(
                                    color=white,
                                    bgcolor='#5B7553',
                                    width=250,
                                    height=70,
                                    content=Column(
                                        horizontal_alignment='center',
                                        alignment='center',
                                        controls=[
                                            Container(
                                                Text(
                                                    value='Подтвердить изменения',
                                                    size=16,
                                                    color=white,
                                                    text_align='center',
                                                    weight='bold',
                                                )
                                            )
                                        ]
                                    ),
                                    on_click=self.open_are_you_sure_dialoge
                                ),
                            ),
                        ],
                    )
                ),
            ]
        )

    def show_block_dialog(self, content_text, title_text):
        self.page.dialog = self.alter_dialog_block
        self.alter_dialog_block.content = Text(f"{content_text}")
        self.alter_dialog_block.title = Text(f"{title_text}")
        self.alter_dialog_block.open = True
        self.page.update()

    def close_dlg_block(self, e):
        self.page.dialog = self.alter_dialog_block
        self.alter_dialog_block.open = False
        print("Вы закрыли модульное окно успеха")
        self.page.update()

    def show_kpe_table(self, e):
        global user_id
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT specialist_id FROM specialists WHERE full_name='{str(self.report_spec.content.value)}';")
        user_id = cursor.fetchone()[0]

        query_select = "SELECT MAX(number_of_version) FROM kpe_table WHERE kpe_user_id = '{}';".format(user_id)
        cursor.execute(query_select)
        latest_version = cursor.fetchone()[0]

        query_select = f"""
        SELECT
            ROW_NUMBER() OVER () AS "порядковый номер",
            ni.name AS indicator_name,
            um.type AS unit_of_measurement,
            kt.1st_quater_value,
            kt.2nd_quater_value,
            kt.3rd_quater_value,
            kt.4th_quater_value,
            kt.year,
            kt.KPE_weight_1,
            kt.KPE_weight_2,
            kt.KPE_weight_3,
            kt.KPE_weight_4
        FROM kpe_table AS kt
        JOIN name_of_indicators AS ni ON kt.kpe_indicators_id = ni.indicators_id
        JOIN units_of_measurement AS um ON kt.kpe_units_id = um.measurement_id
        WHERE kt.kpe_user_id = {user_id} AND kt.number_of_version = '{latest_version}' AND kt.status = 'Активно'
        ORDER BY kpe_id;
      """

        cursor.execute(query_select)
        results = cursor.fetchall()
        query_result = results
        data_rows = []

        for row in query_result:
            cells = [DataCell(Text(str(value))) for value in row]
            data_row = DataRow(cells=cells)

            checkbox = Checkbox(value=False, on_change=lambda e, row=row: self.toggle_row_selection(e, row))
            cells.append(DataCell(checkbox))
            data_rows.append(data_row)
        self.data_table.rows = data_rows
        self.page.update()

    def show_alter_dialog_add_new_specialists(self, e):
        self.page.dialog = self.alter_dialog_add_new_specialists
        self.page.dialog.open = True
        self.page.update()

    def close_dlg_add_new_specialists(self, e):
        self.page.dialog = self.alter_dialog_add_new_specialists
        self.page.dialog.open = False
        self.page.update()

    def toggle_row_selection(self, e, row):
        # Toggle the row's selection when the Checkbox value changes
        if row not in self.selected_rows:
            self.selected_rows.add(row)
            print("yes")
        else:
            self.selected_rows.remove(row)
            print("no")

    def show_edit_dialog(self):
        selected_row = next(iter(self.selected_rows))
        self.first_qr_box.content.value = selected_row[3]
        self.second_qr_box.content.value = selected_row[4]
        self.third_qr_box.content.value = selected_row[5]
        self.fourtht_qr_box.content.value = selected_row[6]
        self.year_box.content.value = selected_row[7]
        self.weight_first_qr_box.content.value = selected_row[8]
        self.weight_second_qr_box.content.value = selected_row[9]
        self.weight_third_qr_box.content.value = selected_row[10]
        self.weight_fourth_qr_box.content.value = selected_row[11]
        self.page.dialog = self.alter_dialog_edit
        self.alter_dialog_edit.open = True
        self.page.update()

    def edit_name_in_table(self, e):
        try:
            selected_row = next(iter(self.selected_rows))
            cursor = connection.cursor()

            sql_select = "SELECT kpe_id FROM kpe_table WHERE 1st_quater_value = {} AND 2nd_quater_value = {} AND 3rd_quater_value = {} AND 4th_quater_value = {} AND year = {} AND KPE_weight_1 = {} AND KPE_weight_2 = {} AND KPE_weight_3 = {} AND KPE_weight_4 = {};".format(
                selected_row[3], selected_row[4], selected_row[5], selected_row[6], selected_row[7], selected_row[8],
                selected_row[9], selected_row[10], selected_row[11])
            cursor.execute(sql_select)
            kpe_id = cursor.fetchone()[0]
            print(kpe_id)

            cursor.execute(f"SELECT number_of_version FROM kpe_table WHERE kpe_id = {kpe_id};")
            max_version = cursor.fetchone()[0]
            if max_version and len(max_version.split('-')) >= 3:
                current_version = int(max_version.split('-')[2])
            else:
                current_version = 0
            formatted_date = max_version.split('-')[1]
            number_of_verison_plus = f"{1}-{formatted_date}-{current_version + 1}"
            print(number_of_verison_plus)
            if self.first_qr_box.content.value != selected_row[3]:
                query_1st_qr = "ALTER TABLE kpe_table UPDATE 1st_quater_value = {} WHERE kpe_id = {};".format(self.first_qr_box.content.value, kpe_id)
                self.sql_query.append(query_1st_qr)
                self.page.dialog = self.alter_dialog_edit
                self.alter_dialog_edit.open = False

            if self.second_qr_box.content.value != selected_row[4]:
                query_2nd_qr = "ALTER TABLE kpe_table UPDATE 2nd_quater_value = {} WHERE kpe_id = {};".format(self.second_qr_box.content.value, kpe_id)
                self.sql_query.append(query_2nd_qr)
                self.page.dialog = self.alter_dialog_edit
                self.alter_dialog_edit.open = False

            if self.third_qr_box.content.value != selected_row[5]:
                query_3rd_qr = "ALTER TABLE kpe_table UPDATE 3rd_quater_value = {} WHERE kpe_id = {};".format(self.third_qr_box.content.value, kpe_id)
                self.sql_query.append(query_3rd_qr)
                self.page.dialog = self.alter_dialog_edit
                self.alter_dialog_edit.open = False

            if self.fourtht_qr_box.content.value != selected_row[6]:
                query_4th_qr = "ALTER TABLE kpe_table UPDATE 4th_quater_value = {} WHERE kpe_id = {};".format(self.fourtht_qr_box.content.value, kpe_id)
                self.sql_query.append(query_4th_qr)
                self.page.dialog = self.alter_dialog_edit
                self.alter_dialog_edit.open = False

            if self.year_box.content.value != selected_row[7]:
                query_year = "ALTER TABLE kpe_table UPDATE year = {} WHERE kpe_id = {};".format(self.year_box.content.value, kpe_id)
                self.sql_query.append(query_year)
                self.page.dialog = self.alter_dialog_edit
                self.alter_dialog_edit.open = False

            if self.weight_first_qr_box.content.value != selected_row[8]:
                query_weight_firts_qr = "ALTER TABLE kpe_table UPDATE KPE_weight_1 = {} WHERE kpe_id = {};".format(self.weight_first_qr_box.content.value, kpe_id)
                self.sql_query.append(query_weight_firts_qr)
                self.page.dialog = self.alter_dialog_edit
                self.alter_dialog_edit.open = False

            if self.weight_second_qr_box.content.value != selected_row[9]:
                query_weight_second_qr = "ALTER TABLE kpe_table UPDATE KPE_weight_2 = {} WHERE kpe_id = {};".format(self.weight_second_qr_box.content.value, kpe_id)
                self.sql_query.append(query_weight_second_qr)
                self.page.dialog = self.alter_dialog_edit
                self.alter_dialog_edit.open = False

            if self.weight_third_qr_box.content.value != selected_row[10]:
                query_weight_third_qr = "ALTER TABLE kpe_table UPDATE KPE_weight_3 = {} WHERE kpe_id = {};".format(self.weight_third_qr_box.content.value, kpe_id)
                self.sql_query.append(query_weight_third_qr)
                self.page.dialog = self.alter_dialog_edit
                self.alter_dialog_edit.open = False

            if self.weight_fourth_qr_box.content.value != selected_row[11]:
                query_weight_fourth_qr = "ALTER TABLE kpe_table UPDATE KPE_weight_4 = {} WHERE kpe_id = {};".format(self.weight_fourth_qr_box.content.value, kpe_id)
                self.sql_query.append(query_weight_fourth_qr)
                self.page.dialog = self.alter_dialog_edit
                self.alter_dialog_edit.open = False
            else:
                print("Поля никак не изменились")
            query_number_of_version = "ALTER TABLE kpe_table UPDATE number_of_version = '{}' WHERE kpe_id = {};".format(str(number_of_verison_plus), kpe_id)
            self.sql_query.append(query_number_of_version)
            self.first_qr_box.content.value = ""
            self.second_qr_box.content.value = ""
            self.third_qr_box.content.value = ""
            self.fourtht_qr_box.content.value = ""
            self.year_box.content.value = ""
            self.weight_first_qr_box.content.value = ""
            self.weight_second_qr_box.content.value = ""
            self.weight_third_qr_box.content.value = ""
            self.weight_fourth_qr_box.content.value = ""
            self.cb_menu_spec.content.value = ""
            self.show_block_dialog("Данные были успешно занесены в список изменений", "Успешно")
            self.page.update()
        except:
            self.show_block_dialog("При измение данных произошла ошибка", "Ошибка")

    def delete_name_in_table(self, e):
        cursor = connection.cursor()

        for selected_row in self.selected_rows:
            sql_select = "SELECT kpe_id FROM kpe_table WHERE 1st_quater_value = {} AND 2nd_quater_value = {} AND 3rd_quater_value = {} AND 4th_quater_value = {} AND year = {} AND KPE_weight_1 = {} AND KPE_weight_2 = {} AND KPE_weight_3 = {} AND KPE_weight_4 = {};".format(
                selected_row[3], selected_row[4], selected_row[5], selected_row[6], selected_row[7], selected_row[8],
                selected_row[9], selected_row[10], selected_row[11])
            cursor.execute(sql_select)
            kpe_id = cursor.fetchone()[0]
            print(kpe_id)
            query_status = "ALTER TABLE kpe_table UPDATE status = 'Неактивно' WHERE kpe_id = {};".format(kpe_id)
            self.sql_query.append(query_status)

        self.show_block_dialog("Запись была успешно занесены в список удаления", "Успешно")
        print(self.sql_query)
        self.page.update()

    def stay_name_in_table(self, e):
        cursor = connection.cursor()
        for selected_row in self.selected_rows:
            sql_select = "SELECT kpe_id FROM kpe_table WHERE 1st_quater_value = {} AND 2nd_quater_value = {} AND 3rd_quater_value = {} AND 4th_quater_value = {} AND year = {} AND KPE_weight_1 = {} AND KPE_weight_2 = {} AND KPE_weight_3 = {} AND KPE_weight_4 = {};".format(
                selected_row[3], selected_row[4], selected_row[5], selected_row[6], selected_row[7], selected_row[8],
                selected_row[9], selected_row[10], selected_row[11])
            cursor.execute(sql_select)
            kpe_id = cursor.fetchone()[0]

            date = datetime.datetime.now()

            cursor.execute(f"SELECT number_of_version FROM kpe_table WHERE kpe_id = {kpe_id};")
            max_version = cursor.fetchone()[0]
            if max_version and len(max_version.split('-')) >= 3:
                current_version = int(max_version.split('-')[2])
            else:
                current_version = 0

            formatted_date = max_version.split('-')[1]
            number_of_verison_plus = f"{1}-{formatted_date}-{current_version + 1}"
            print(number_of_verison_plus)

            print(kpe_id)
            query_number_of_version = "ALTER TABLE kpe_table UPDATE number_of_version = '{}' WHERE kpe_id = {};".format(str(number_of_verison_plus), kpe_id)
            self.sql_query.append(query_number_of_version)
        print(self.sql_query)
        self.show_block_dialog("Выбранные данные были успешно оставлены", "Успешно")
        self.page.update()

    def close_edit_dialog(self, e):
        self.page.dialog = self.alter_dialog_edit
        self.alter_dialog_edit.open = False
        self.page.update()

    def added_new_to_indicators(self, e):
        selected_item = self.cb_menu_spec.content.value
        print(f"Selected item: {selected_item}")
        if selected_item == "Нет в списке":
            self.page.dialog = self.alter_dialog_no_in_list
            print("Opening dialog...")
            self.alter_dialog_no_in_list.open = True
        self.page.update()

    def alter_dialoge_input_data(self, e):
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT max(indicators_id) FROM name_of_indicators;")
            max_id = cursor.fetchone()[0]
            query = "INSERT INTO TABLE name_of_indicators (indicators_id, name) VALUES ({},'{}');".format(
                int(max_id) + 1, self.textfiled_input_new_indicator.content.value)
            cursor.execute(query)
            print("Запись успешно добавлена в базу данных")
            self.page.dialog = self.alter_dialog
            self.alter_dialog.open = False
            self.page.update()
        except Exception as e:
            print(f"Ошибка при добавлении записи в базу данных: {str(e)}")

    def close_dlg_new_indicator(self, e):
        self.page.dialog = self.alter_dialog_no_in_list
        self.alter_dialog_no_in_list.open = False
        self.page.update()

    def show_add_dialog(self, e):
        self.page.dialog = self.alter_dialog_add_new
        self.alter_dialog_add_new.open = True
        self.page.update()

    def add_new_specialist(self, e):
        # *FOR USER DATA INFORMATION
        try:
            cursor = connection.cursor()
            cursor.execute(
                f"SELECT specialist_id FROM specialists WHERE full_name='{str(self.report_spec.content.value)}';")
            user_id = cursor.fetchone()[0]

            # *FOR AUTO ID INCRIPTION
            cursor = connection.cursor()
            cursor.execute(f"SELECT MAX(kpe_id) FROM kpe_table")
            max_kpe_id = cursor.fetchone()[0]
            # *FOR INDICATORS
            selected_indicator = self.cb_menu_spec.content.value
            cursor = connection.cursor()
            selected_indicator_without_dots = selected_indicator.replace(".", "")
            cursor.execute(
                f"SELECT indicators_id FROM name_of_indicators WHERE name LIKE '{selected_indicator_without_dots}%';")
            indicator_id = cursor.fetchone()[0]
            # *FRO PLAN_INDICATOR
            cursor = connection.cursor()
            cursor.execute(f"SELECT kpe_indicators_id FROM kpe_table;")
            kpe_indicator_id = cursor.fetchone()
            # *FOR UNITS
            # selected_unit = self.units_menu_box.content.value
            cursor = connection.cursor()
            # cursor.execute(f"SELECT measurement_id FROM name_of_indicators WHERE name LIKE '{selected_indicator}%'")
            cursor.execute(
                f"SELECT measurement_id FROM name_of_indicators WHERE name LIKE '{selected_indicator_without_dots}%';")
            units_id = cursor.fetchone()[0]

            # Определите максимальное значение номера версии для данного показателя
            # Determine the maximum version for the current indicator and user combination
            cursor.execute(f"SELECT MAX(number_of_version) FROM kpe_table WHERE kpe_user_id = {int(user_id)};")
            max_version = cursor.fetchone()[0]
            print(max_version)
            insert_query_to_kpe_table = """
          INSERT INTO kpe_table (
              kpe_id, 
              kpe_indicators_id, 
              kpe_user_id, 
              kpe_units_id, 
              1st_quater_value, 
              2nd_quater_value, 
              3rd_quater_value, 
              4th_quater_value, 
              year,
              status,
              KPE_weight_1, 
              KPE_weight_2, 
              KPE_weight_3, 
              KPE_weight_4, 
              number_of_version
              )
          VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, '{}', {}, {}, {}, {}, '{}');
          """.format(
                int(max_kpe_id + 1),
                int(indicator_id),
                int(user_id),
                int(units_id),
                int(self.first_qr_box.content.value),
                int(self.second_qr_box.content.value),
                int(self.third_qr_box.content.value),
                int(self.fourtht_qr_box.content.value),
                int(self.year_box.content.value),
                str("Активно"),
                int(self.weight_first_qr_box.content.value),
                int(self.weight_second_qr_box.content.value),
                int(self.weight_third_qr_box.content.value),
                int(self.weight_fourth_qr_box.content.value),
                str(max_version)
            )
            cursor.execute(insert_query_to_kpe_table)
            print("Success")
            self.first_qr_box.content.value = ""
            self.second_qr_box.content.value = ""
            self.third_qr_box.content.value = ""
            self.fourtht_qr_box.content.value = ""
            self.year_box.content.value = ""
            self.weight_first_qr_box.content.value = ""
            self.weight_second_qr_box.content.value = ""
            self.weight_third_qr_box.content.value = ""
            self.weight_fourth_qr_box.content.value = ""
            self.cb_menu_spec.content.value = ""
            self.page.dialog = self.alter_dialog_add_new
            self.alter_dialog_add_new.open = False

            cursor = connection.cursor()
            cursor.execute(
                f"SELECT specialist_id FROM specialists WHERE full_name='{str(self.report_spec.content.value)}';")
            user_id = cursor.fetchone()[0]

            query_select = "SELECT MAX(number_of_version) FROM kpe_table WHERE kpe_user_id = '{}'".format(user_id)
            cursor.execute(query_select)
            latest_version = cursor.fetchone()[0]

            query_select = f"""
                      SELECT
                          ROW_NUMBER() OVER () AS "порядковый номер",
                          ni.name AS indicator_name,
                          um.type AS unit_of_measurement,
                          kt.1st_quater_value,
                          kt.2nd_quater_value,
                          kt.3rd_quater_value,
                          kt.4th_quater_value,
                          kt.year,
                          kt.KPE_weight_1,
                          kt.KPE_weight_2,
                          kt.KPE_weight_3,
                          kt.KPE_weight_4
                      FROM kpe_table AS kt
                      JOIN name_of_indicators AS ni ON kt.kpe_indicators_id = ni.indicators_id
                      JOIN units_of_measurement AS um ON kt.kpe_units_id = um.measurement_id
                      WHERE kt.kpe_user_id = {user_id} AND kt.number_of_version = '{latest_version}' AND kt.status = 'Активно';
                    """

            cursor.execute(query_select)
            results = cursor.fetchall()
            query_result = results
            data_rows = []

            for row in query_result:
                cells = [DataCell(Text(str(value))) for value in row]
                data_row = DataRow(cells=cells)

                # Create a Checkbox for the third column
                checkbox_1 = Checkbox(value=False, on_change=lambda e, row=row: self.toggle_row_selection(e, row))
                cells.append(DataCell(checkbox_1))

                data_rows.append(data_row)

            # After you fetch new data from the database and create data_rows, update the DataTable like this:
            self.data_table.rows = data_rows
            self.page.update()
        except:
            self.show_block_dialog("При внесение новой записи произошла ошибка", "Ошибка")

    def close_new_kpe_dialog(self, e):
        self.page.dialog = self.alter_dialog_add_new
        self.alter_dialog_add_new.open = False
        self.page.update()

    def open_are_you_sure_dialoge(self,e):
        self.page.dialog = self.alter_dialog_are_you_sure
        self.alter_dialog_are_you_sure.open = True
        self.page.update()


    def close_are_you_sure_dialoge(self,e):
        self.page.dialog = self.alter_dialog_are_you_sure
        self.alter_dialog_are_you_sure.open = False
        self.page.update()


    def insert_all_data_from_array(self, e):
        try:
            cursor = connection.cursor()
            for queryes in self.sql_query:
                cursor.execute(queryes)
            self.sql_query.clear()
            print(self.sql_query)
            cursor.execute(
                f"SELECT specialist_id FROM specialists WHERE full_name='{str(self.report_spec.content.value)}';")
            user_id = cursor.fetchone()[0]

            query_select = "SELECT MAX(number_of_version) FROM kpe_table WHERE kpe_user_id = '{}'".format(user_id)
            cursor.execute(query_select)
            latest_version = cursor.fetchone()[0]

            query_select = f"""
                              SELECT
                                  ROW_NUMBER() OVER () AS "порядковый номер",
                                  ni.name AS indicator_name,
                                  um.type AS unit_of_measurement,
                                  kt.1st_quater_value,
                                  kt.2nd_quater_value,
                                  kt.3rd_quater_value,
                                  kt.4th_quater_value,
                                  kt.year,
                                  kt.KPE_weight_1,
                                  kt.KPE_weight_2,
                                  kt.KPE_weight_3,
                                  kt.KPE_weight_4
                              FROM kpe_table AS kt
                              JOIN name_of_indicators AS ni ON kt.kpe_indicators_id = ni.indicators_id
                              JOIN units_of_measurement AS um ON kt.kpe_units_id = um.measurement_id
                              WHERE kt.kpe_user_id = {user_id} AND kt.number_of_version = '{latest_version}' AND kt.status = 'Активно'
                              ORDER BY kpe_id;
                            """

            cursor.execute(query_select)
            results = cursor.fetchall()
            query_result = results
            data_rows = []

            for row in query_result:
                cells = [DataCell(Text(str(value))) for value in row]
                data_row = DataRow(cells=cells)

                # Create a Checkbox for the third column
                checkbox_1 = Checkbox(value=False, on_change=lambda e, row=row: self.toggle_row_selection(e, row))
                cells.append(DataCell(checkbox_1))

                data_rows.append(data_row)

            # After you fetch new data from the database and create data_rows, update the DataTable like this:
            self.data_table.rows = data_rows
            self.page.dialog = self.alter_dialog_are_you_sure
            self.alter_dialog_are_you_sure.open = False
            self.page.update()
            self.selected_rows.clear()
        except:
            self.show_block_dialog("При подтверждение изменённой вами информации произошла ошибка", "Ошибка")