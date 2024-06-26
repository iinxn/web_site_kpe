import datetime
from flet import *
from service.connection import *
from utils.consts import primary_colors


class EditKPE(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.theme_mode = ThemeMode.LIGHT
        self.alignment = alignment.center
        self.expand = True
        self.bgcolor = primary_colors['WHITE']
        self.user_id = self.page.session.get('user_id')
        self.selected_rows = set()
        self.sql_query = []
        self.dropdown_options_indicators = []
        self.dropdown_options_specialists = []
        dropdown_options_units = []
        dropdown_options_departments = []
        
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
            border=border.all(1, primary_colors['BLACK']),
            vertical_lines=border.BorderSide(1, primary_colors['BLACK']),
            horizontal_lines=border.BorderSide(1, primary_colors['BLACK']),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=colors.BLACK12,
            heading_row_height=100,
            data_row_max_height=100,
            width=2000
        )

        # * SELECT UNITS NAME FROM MEASUREMNT TABLE
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT type FROM units_of_measurement ORDER BY measurement_id')
            results = cursor.fetchall()

            for row in results:
                dropdown_options_units.append(dropdown.Option(row[0]))
        except Exception as e:
            print(f"Error fetching data from the database: {str(e)}")

        try:
            cursor = connection.cursor()
            cursor.execute('SELECT name FROM name_of_department ORDER BY department_id')
            results = cursor.fetchall()

            for row in results:
                dropdown_options_departments.append(dropdown.Option(row[0]))

        except Exception as e:
            print(f"Error fetching data from the database: {str(e)}")
        # *DROPDOWNS
        self.report_spec = Container(
            content=Dropdown(
                hint_text='Выберите специалиста',
                color=primary_colors['BLACK'],
                options=self.dropdown_options_specialists,
                on_change=self.show_indicators
            )
        )
        self.units_menu_box = Container(
            content=Dropdown(
                hint_text='ед. изм.',
                color=primary_colors['BLACK'],
                width=300,
                options=dropdown_options_units,  # Set the options from the fetched data
            ),
        )
        self.name_of_department_menu_box = Container(
            content=Dropdown(
                hint_text='Выберите управление',
                color=primary_colors['BLACK'],
                width=500,
                options=dropdown_options_departments,
                on_change=self.show_specialists
            ),
        )
        self.first_qr_box = Container(
            content=TextField(
                hint_style=TextStyle(
                    size=12, color=primary_colors['MANATEE']
                ),
                label='1 квартал',
                cursor_color=primary_colors['MANATEE'],
                text_style=TextStyle(
                    size=14,
                    color=primary_colors['GREEN'],
                ),
                width=100
            ),
        )
        self.second_qr_box = Container(
            content=TextField(
                hint_style=TextStyle(
                    size=12, color=primary_colors['MANATEE']
                ),
                label='2 квартал',
                cursor_color=primary_colors['MANATEE'],
                text_style=TextStyle(
                    size=14,
                    color=primary_colors['GREEN'],
                ),
                width=100
            ),
        )
        self.third_qr_box = Container(
            content=TextField(
                hint_style=TextStyle(
                    size=12, color=primary_colors['MANATEE']
                ),
                label='3 квартал',
                cursor_color=primary_colors['MANATEE'],
                text_style=TextStyle(
                    size=14,
                    color=primary_colors['GREEN'],
                ),
                width=100
            ),
        )
        self.fourtht_qr_box = Container(
            content=TextField(
                hint_style=TextStyle(
                    size=12, color=primary_colors['MANATEE']
                ),
                label='4 квартал',
                cursor_color=primary_colors['MANATEE'],
                text_style=TextStyle(
                    size=14,
                    color=primary_colors['GREEN'],
                ),
                width=100
            ),
        )
        self.year_box = Container(
            content=TextField(
                hint_style=TextStyle(
                    size=12, color=primary_colors['MANATEE']
                ),
                label='Год',
                cursor_color=primary_colors['MANATEE'],
                text_style=TextStyle(
                    size=14,
                    color=primary_colors['GREEN'],
                ),
                width=100
            ),
        )
        self.weight_first_qr_box = Container(
            content=TextField(
                hint_style=TextStyle(
                    size=12, color=primary_colors['MANATEE']
                ),
                label='Вес 1 кв.',
                cursor_color=primary_colors['MANATEE'],
                text_style=TextStyle(
                    size=14,
                    color=primary_colors['GREEN'],
                ),
                width=100
            ),
        )
        self.weight_second_qr_box = Container(
            content=TextField(
                hint_style=TextStyle(
                    size=12, color=primary_colors['MANATEE']
                ),
                label='Вес 2 кв.',
                cursor_color=primary_colors['MANATEE'],
                text_style=TextStyle(
                    size=14,
                    color=primary_colors['GREEN'],
                ),
                width=100
            ),
        )
        self.weight_third_qr_box = Container(
            content=TextField(
                hint_style=TextStyle(
                    size=12, color=primary_colors['MANATEE']
                ),
                label='Вес 3 кв.',
                cursor_color=primary_colors['MANATEE'],
                text_style=TextStyle(
                    size=14,
                    color=primary_colors['GREEN'],
                ),
                width=100
            ),
        )
        self.weight_fourth_qr_box = Container(
            content=TextField(
                hint_style=TextStyle(
                    size=12, color=primary_colors['MANATEE']
                ),
                label='Вес 4 кв.',
                cursor_color=primary_colors['MANATEE'],
                text_style=TextStyle(
                    size=14,
                    color=primary_colors['GREEN'],
                ),
                width=100
            ),
        )
        self.cb_menu_spec = Container(
            content=Dropdown(
                label='Выберите наименование показателя',
                color=primary_colors['BLACK'],
                width=850,
                options=self.dropdown_options_indicators,
                on_change=self.added_new_to_indicators
            ),
        )
        self.textfiled_input_new_indicator = Container(
            content=TextField(
                label="Введите наименование показателя",
                hint_style=TextStyle(
                    size=12, color=primary_colors['MANATEE']
                ),
                cursor_color=primary_colors['MANATEE'],
                text_style=TextStyle(
                    size=14,
                    color=primary_colors['BLACK'],
                ),
                width=400
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
                color=primary_colors['GREEN'],
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
                                self.units_menu_box,
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
                                    color=primary_colors['GREEN'],
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
                                    color=primary_colors['GREEN'],
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
                color=primary_colors['GREEN']
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
                                    color=primary_colors['GREEN'],
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
                                    color=primary_colors['GREEN'],
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
                TextButton("Добавить", on_click=self.add_new_row_to_kpe_table),
                TextButton("Закрыть", on_click=self.close_new_kpe_dialog),
            ],
            actions_alignment=MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        self.alter_dialog_no_in_list = AlertDialog(
            modal=True,
            title=Text("Добавление показателя в справочник"),
            content=Container(
                width=800,
                height=100,
                content=Column(
                    controls=[
                        Container(
                            Text(
                                value='Перед добавлением показателей, необходимо заполнить справочник единицы измерения!!!',
                                text_align='center',
                                size=18
                            )
                        ),
                        Container(
                            Row(
                                spacing='30',
                                alignment='center',
                                controls=[
                                    self.textfiled_input_new_indicator,
                                    self.units_menu_box
                                ]
                            )
                        )
                    ]
                )
            ),
            actions=[
                TextButton("Добавить", on_click=self.alter_dialoge_input_new_indicator),
                TextButton("Назад", on_click=self.close_dlg_new_indicator),
            ],
            actions_alignment=MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
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
                                                            on_click=lambda x: x == self.page.go('/card')
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
                                                value='Ввести изменение в карту КПЭ',
                                                size=18,
                                                color=primary_colors['WHITE'],
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
                    bgcolor=primary_colors['WHITE'],
                    content=Column(
                        expand=True,
                        horizontal_alignment='center',
                        controls=[
                            # *1ST ROW (TEXTFILED AND BUTTON)
                            Container(height=25),
                            Container(
                                content=Row(
                                    controls=[
                                        Container(width=29),
                                        self.name_of_department_menu_box,
                                    ]
                                )
                            ),
                            Container(
                                content=Row(
                                    spacing='30',
                                    alignment='center',
                                    controls=[
                                        self.report_spec,
                                        Container(
                                            content=ElevatedButton(
                                                color=primary_colors['WHITE'],
                                                bgcolor=primary_colors['GREEN'],
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
                                                                color=primary_colors['WHITE'],
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
                                                color=primary_colors['WHITE'],
                                                bgcolor=primary_colors['GREEN'],
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
                                                                color=primary_colors['WHITE'],
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
                                                color=primary_colors['WHITE'],
                                                bgcolor=primary_colors['GREEN'],
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
                                                                color=primary_colors['WHITE'],
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
                                                color=primary_colors['WHITE'],
                                                bgcolor=primary_colors['GREEN'],
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
                                                                color=primary_colors['WHITE'],
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
                                                color=primary_colors['WHITE'],
                                                bgcolor=primary_colors['GREEN'],
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
                                                                color=primary_colors['WHITE'],
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
                                    color=primary_colors['WHITE'],
                                    bgcolor=primary_colors['GREEN'],
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
                                                    color=primary_colors['WHITE'],
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
    def show_specialists(self, e):
        self.dropdown_options_specialists.clear()
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT department_id FROM name_of_department WHERE name = '{self.name_of_department_menu_box.content.value}'")
            specialist_department_id = cursor.fetchone()[0]
            
            cursor.execute(f"SELECT full_name FROM specialists WHERE specialist_department_id = {specialist_department_id}")
            specialists_full_name = cursor.fetchall()

            for row in specialists_full_name:
                self.dropdown_options_specialists.append(dropdown.Option(row[0]))
                
            self.page.update()
        except Exception as e:
            print(f"Error fetching data from the database: {str(e)}")

    def show_indicators(self, e):
        try:
            self.dropdown_options_indicators.clear()

            cursor = connection.cursor()
            sql_select_specialist_id = f"SELECT specialist_id FROM specialists WHERE full_name = '{self.report_spec.content.value}'"
            cursor.execute(sql_select_specialist_id)
            specialist_id = cursor.fetchone()[0]

            cursor.execute(f'SELECT indicators_id, name FROM name_of_indicators WHERE specialist_id = {specialist_id} ORDER BY indicators_id')
            results = cursor.fetchall()

            for indicator_id, name in results:
                self.dropdown_options_indicators.append(dropdown.Option(indicator_id, name))

            no_list_option = dropdown.Option('Нет в списке')
            self.dropdown_options_indicators.append(no_list_option)

            self.page.update()
        except Exception as e:
            print(f"Error fetching data from the database: {str(e)}")

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
        try:
            global specialist_id
            cursor = connection.cursor()
            cursor.execute(
                f"SELECT specialist_id FROM specialists WHERE full_name='{str(self.report_spec.content.value)}';")
            specialist_id = cursor.fetchone()[0]

            query_select = f"""
                SELECT
                    ROW_NUMBER() OVER (ORDER BY kpe_id) AS "порядковый номер",
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
                WHERE
                    kt.kpe_specialist_id = {int(specialist_id)} AND
                    kt.status = 'Активно' AND
                    kt.date = (
                        SELECT MAX(date)
                        FROM kpe_table
                        WHERE kpe_specialist_id = {int(specialist_id)} AND status = 'Активно'
                    ) AND
                    kt.number = (
                        SELECT MAX(number)
                        FROM kpe_table
                        WHERE
                            kpe_specialist_id = {int(specialist_id)} AND
                            status = 'Активно' AND
                            date = (
                                SELECT MAX(date)
                                FROM kpe_table
                                WHERE kpe_specialist_id = {int(specialist_id)} AND status = 'Активно'
                            )
                    )
                ORDER BY kpe_id;
            """
            cursor.execute(query_select)
            results = cursor.fetchall()
            query_result = results
            if not query_result:
                self.show_block_dialog('Карта КПЭ этого специалиста не сформирована', 'Ошибка')
            else:
                data_rows = []

                for row in query_result:
                    cells = [DataCell(Text(str(value))) for value in row]
                    data_row = DataRow(cells=cells)

                    checkbox = Checkbox(value=False, on_change=lambda e, row=row: self.toggle_row_selection(e, row))
                    cells.append(DataCell(checkbox))
                    data_rows.append(data_row)
                self.data_table.rows = data_rows
                self.page.update()
        except:
            self.show_block_dialog("Вы не выбрали специалиста", "Ошибка")

    def show_alter_dialog_add_new_row_to_kpe_tables(self, e):
        self.page.dialog = self.alter_dialog_add_new_row_to_kpe_tables
        self.page.dialog.open = True
        self.page.update()

    def close_dlg_add_new_row_to_kpe_tables(self, e):
        self.page.dialog = self.alter_dialog_add_new_row_to_kpe_tables
        self.page.dialog.open = False
        self.page.update()

    def toggle_row_selection(self, e, row):
        if row not in self.selected_rows:
            self.selected_rows.add(row)
            print("yes")
        else:
            self.selected_rows.remove(row)
            print("no")

    def show_edit_dialog(self):
        selected_row = next(iter(self.selected_rows))
        self.units_menu_box.content.value = selected_row[2]
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
            
            changes_made = False
            # Fetch measurement_id based on type name
            cursor.execute(f"SELECT measurement_id FROM units_of_measurement WHERE type = '{self.units_menu_box.content.value}'")
            measurement_id = cursor.fetchone()[0]

            # Iterate over fields to check
            fields_to_check = [
                (self.units_menu_box.content.value, selected_row[2], 'kpe_units_id'),
                (self.first_qr_box.content.value, selected_row[3], '1st_quater_value'),
                (self.second_qr_box.content.value, selected_row[4], '2nd_quater_value'),
                (self.third_qr_box.content.value, selected_row[5], '3rd_quater_value'),
                (self.fourtht_qr_box.content.value, selected_row[6], '4th_quater_value'),
                (self.year_box.content.value, selected_row[7], 'year'),
                (self.weight_first_qr_box.content.value, selected_row[8], 'KPE_weight_1'),
                (self.weight_second_qr_box.content.value, selected_row[9], 'KPE_weight_2'),
                (self.weight_third_qr_box.content.value, selected_row[10], 'KPE_weight_3'),
                (self.weight_fourth_qr_box.content.value, selected_row[11], 'KPE_weight_4'),
            ]
            for new_value, old_value, column_name in fields_to_check:
                if new_value != old_value:
                    cursor.execute(f"SELECT MAX(number) FROM kpe_table WHERE kpe_id = {kpe_id};")
                    max_number = cursor.fetchone()[0]
                    number_plus = max_number+1
                    print(number_plus)
                    if column_name == 'kpe_units_id':
                        cursor.execute(f"SELECT measurement_id FROM units_of_measurement WHERE type = '{new_value}'")
                        measurement_id = cursor.fetchone()[0]
                    query = f"ALTER TABLE kpe_table UPDATE {column_name} = {measurement_id if column_name == 'kpe_units_id' else new_value} WHERE kpe_id = {kpe_id};"
                    query_number_of_version = "ALTER TABLE kpe_table UPDATE number = {} WHERE kpe_id = {};".format(str(number_plus), kpe_id)
                    self.sql_query.append(query_number_of_version)
                    self.sql_query.append(query)
                    for queryes in self.sql_query:
                        print(queryes)
                    changes_made = True
            if changes_made:
                self.page.dialog = self.alter_dialog_edit
                self.alter_dialog_edit.open = False
            else:
                print("Поля никак не изменились")
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
            self.units_menu_box.content.value = ""
            self.show_block_dialog("Данные были успешно занесены в список изменений", "Успешно")
            self.page.update()
        except:
            self.show_block_dialog("При измение данных произошла ошибка", "Ошибка")

    def delete_name_in_table(self, e):
        cursor = connection.cursor()
        for selected_row in self.selected_rows:
            cursor.execute(f"SELECT specialist_id FROM specialists WHERE full_name='{str(self.report_spec.content.value)}';")
            specialist_id = cursor.fetchone()[0]
            indicator = f"SELECT indicators_id FROM name_of_indicators WHERE name = '{selected_row[1]}' AND specialist_id = '{specialist_id}'"
            # print(indicator)
            cursor.execute(indicator)
            indicator_id = cursor.fetchone()[0]
            # print(indicator_id)
            sql_select = "SELECT kpe_id FROM kpe_table WHERE kpe_specialist_id = {} AND kpe_indicators_id = {} AND 1st_quater_value = {} AND 2nd_quater_value = {} AND 3rd_quater_value = {} AND 4th_quater_value = {} AND year = {} AND KPE_weight_1 = {} AND KPE_weight_2 = {} AND KPE_weight_3 = {} AND KPE_weight_4 = {};".format(
                specialist_id, indicator_id, selected_row[3], selected_row[4], selected_row[5], selected_row[6], selected_row[7], selected_row[8], selected_row[9], selected_row[10], selected_row[11])
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
            cursor.execute(f"SELECT specialist_id FROM specialists WHERE full_name='{str(self.report_spec.content.value)}';")
            specialist_id = cursor.fetchone()[0]
            indicator = f"SELECT indicators_id FROM name_of_indicators WHERE name = '{selected_row[1]}' AND specialist_id = '{specialist_id}'"
            # print(indicator)
            cursor.execute(indicator)
            indicator_id = cursor.fetchone()[0]
            # print(indicator_id)
            sql_select = "SELECT kpe_id FROM kpe_table WHERE kpe_specialist_id = {} AND kpe_indicators_id = {} AND 1st_quater_value = {} AND 2nd_quater_value = {} AND 3rd_quater_value = {} AND 4th_quater_value = {} AND year = {} AND KPE_weight_1 = {} AND KPE_weight_2 = {} AND KPE_weight_3 = {} AND KPE_weight_4 = {};".format(
                specialist_id, indicator_id, selected_row[3], selected_row[4], selected_row[5], selected_row[6], selected_row[7], selected_row[8], selected_row[9], selected_row[10], selected_row[11])
            cursor.execute(sql_select)
            kpe_id = cursor.fetchone()[0]

            cursor.execute(f"SELECT MAX(number) FROM kpe_table WHERE kpe_id = {kpe_id};")
            max_number = cursor.fetchone()[0]
            number_plus = max_number+1

            print(kpe_id)
            query_number_of_version = "ALTER TABLE kpe_table UPDATE number = '{}' WHERE kpe_id = {};".format(str(number_plus), kpe_id)
            self.sql_query.append(query_number_of_version)
        print(self.sql_query)
        for queryes in self.sql_query:
            print(queryes)
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

    def alter_dialoge_input_new_indicator(self, e):
        try:
            cursor = connection.cursor()
            sql_select_specialist_id = "SELECT specialist_id FROM specialists WHERE full_name = '{}'".format(self.report_spec.content.value)
            cursor.execute(sql_select_specialist_id)
            specialist_id = cursor.fetchone()[0]
            cursor.execute(f"SELECT measurement_id FROM units_of_measurement WHERE type = '{self.units_menu_box.content.value}'")
            units_id = cursor.fetchone()[0]
            cursor.execute(f"SELECT max(indicators_id) FROM name_of_indicators;")
            max_id = cursor.fetchone()[0]
            query = "INSERT INTO TABLE name_of_indicators (indicators_id, measurement_id, name, specialist_id) VALUES ({}+1,{},'{}',{})".format(
                int(max_id), units_id, self.textfiled_input_new_indicator.content.value, specialist_id)
            cursor.execute(query)
            print("Запись успешно добавлена в базу данных")
            self.cb_menu_spec.content.value = self.textfiled_input_new_indicator.content.value
            self.textfiled_input_new_indicator.content.value = ''
            self.units_menu_box.content.value = ''
            #clear indicators cb and add new data
            self.dropdown_options_indicators.clear()
            self.show_indicators("")

            self.page.dialog = self.alter_dialog_no_in_list
            self.alter_dialog_no_in_list.open = False
            self.page.dialog = self.alter_dialog_add_new
            self.alter_dialog_add_new.open = True
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

    def add_new_row_to_kpe_table(self, e):
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT specialist_id FROM specialists WHERE full_name='{str(self.report_spec.content.value)}';")
            specialist_id = cursor.fetchone()[0]
            cursor.execute(f"SELECT max(kpe_id) FROM kpe_table;")
            max_id = cursor.fetchone()[0]
            cursor.execute(f"SELECT measurement_id FROM name_of_indicators WHERE indicators_id = '{int(self.cb_menu_spec.content.value)}'")
            units_id = cursor.fetchone()[0]
            query_select = f'SELECT MAX(date), MAX(number) FROM kpe_table WHERE kpe_specialist_id = {int(specialist_id)};'
            cursor.execute(query_select)
            latest_date, latest_number = cursor.fetchone()
            print(latest_date, latest_number)
            query = """
                INSERT INTO kpe_table (
                    kpe_id, 
                    kpe_indicators_id, 
                    kpe_specialist_id, 
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
                    kpe_user_id,
                    date, 
                    number
                    )
                VALUES ({}+1, {}, {}, {}, {}, {}, {}, {}, {},'{}', {}, {}, {}, {}, {}, '{}', {});
            """.format(
                    int(max_id),
                    int(self.cb_menu_spec.content.value),
                    int(specialist_id),
                    int(units_id),
                    float(self.first_qr_box.content.value),
                    float(self.second_qr_box.content.value),
                    float(self.third_qr_box.content.value),
                    float(self.fourtht_qr_box.content.value),
                    float(self.year_box.content.value),
                    "Активно",
                    float(self.weight_first_qr_box.content.value),
                    float(self.weight_second_qr_box.content.value),
                    float(self.weight_third_qr_box.content.value),
                    float(self.weight_fourth_qr_box.content.value),
                    int(self.user_id),
                    str(latest_date),
                    int(latest_number)
                )
            cursor.execute(query)
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
            self.show_kpe_table(e)
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
            self.show_kpe_table(e)
            self.page.dialog = self.alter_dialog_are_you_sure
            self.alter_dialog_are_you_sure.open = False
            self.page.update()
            self.selected_rows.clear()
        except:
            self.show_block_dialog("При подтверждение изменённой вами информации произошла ошибка", "Ошибка")