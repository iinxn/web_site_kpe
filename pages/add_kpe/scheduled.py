import datetime
from flet import *
from service.connection import *
from utils.consts import primary_colors


class Scheduled(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.theme_mode = ThemeMode.LIGHT
        self.alignment = alignment.center
        self.expand = True
        self.bgcolor = primary_colors['WHITE']
        self.end_edit = False
        self.user_id = self.page.session.get("user_id")
        print(self.user_id)

        self.dropdown_options_indicators = []
        self.dropdown_options_specialists = []
        dropdown_options_units = []
        dropdown_options_departments = []
        self.selected_rows = set()
        
        # * TABLE FOR PREVIEW THE DATA
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
            data_row_max_height=80,
            width=2000
        )
        # *SELECT QUERY TO DISPLAY UNITS FROM DB
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT type FROM units_of_measurement ORDER BY measurement_id')
            results = cursor.fetchall()

            for row in results:
                dropdown_options_units.append(dropdown.Option(row[0]))
        except Exception as e:
            print(f"Error fetching data from the database: {str(e)}")

        # * SELECT QUERY TO DISPLAY NAME IN NAME OF DEPARTMENT TABLE FROM DB
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT name FROM name_of_department ORDER BY department_id')
            results = cursor.fetchall()

            for row in results:
                dropdown_options_departments.append(dropdown.Option(row[0]))

        except Exception as e:
            print(f"Error fetching data from the database: {str(e)}")

        # *THERE ARE MY BOXES FOR 2ND ROW
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
                width=100,
                on_change=self.validate
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
                width=100,
                on_change=self.validate
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
                width=100,
                on_change=self.validate
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
                width=100,
                on_change=self.validate
            ),
        )
        self.year_box = Container(
            content=TextField(
                hint_style=TextStyle(
                    size=12, color=primary_colors['MANATEE']
                ),
                label='год',
                cursor_color=primary_colors['MANATEE'],
                text_style=TextStyle(
                    size=14,
                    color=primary_colors['GREEN'],
                ),
                width=100,
                on_change=self.validate
            ),
        )
        # * THERE ARE MY NEXT BOXES FOR MY 3RD ROW
        self.weight_first_qr_box = Container(
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
                width=100,
                on_change=self.validate
            ),
        )
        self.weight_second_qr_box = Container(
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
                width=100,
                on_change=self.validate
            ),
        )
        self.weight_third_qr_box = Container(
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
                width=100,
                on_change=self.validate
            ),
        )
        self.weight_fourth_qr_box = Container(
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
                width=100,
                on_change=self.validate
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
        # *DROPDOWN MENU
        # Create the Dropdown container
        self.cb_menu_spec = Container(
            content=Dropdown(
                label='Выберите наименование показателя',
                color=primary_colors['BLACK'],
                width=600,
                # filled=True,
                options=self.dropdown_options_indicators,
                on_change=self.added_new_to_indicators,
            ),
        )
        self.units_menu_box = Container(
            content=Dropdown(
                hint_text='ед. изм.',
                color=primary_colors['BLACK'],
                width=300,
                options=dropdown_options_units,
            ),
        )
        self.specialist_menu_box = Container(
            content=Dropdown(
                hint_text='Выберите специалиста',
                color=primary_colors['BLACK'],
                width=330,
                options=self.dropdown_options_specialists,
                on_change=self.show_indicators
            )
        )
        self.name_of_department_menu_box = Container(
            content=Dropdown(
                hint_text='Выберите управление',
                color=primary_colors['BLACK'],
                width=600,
                options=dropdown_options_departments,
                on_change=self.show_specialists
            ),
        )
        # *MODULE FORM
        self.alter_dialog = AlertDialog(
            modal=True,
            title=Text("Добавление показателя в справочник"),
            content=Container(
                width=800,
                height=100,
                content = Container(
                    content=Column(
                        controls=[
                            Container(
                                Text(
                                    value='Перед добавлением показателей, необходимо заполнить справочник единицы измерения!!!',
                                    size=18,
                                    text_align='center'
                                ),
                            ),
                            Container(
                                Row(
                                    spacing='30',
                                    alignment='center',
                                    controls=[
                                        self.textfiled_input_new_indicator,
                                        self.units_menu_box
                                    ]
                                ),
                            )
                        ]
                    )
                    
                )
            ),
            actions=[
                TextButton("Добавить", on_click=self.alter_dialoge_input_data),
                TextButton("Назад", on_click=self.close_dlg),
            ],
            actions_alignment=MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),

        )
        self.alter_dialog_block = AlertDialog(
            modal=True,
            title=Text("Default Title"),
            content=Text("Default Content"),
            actions=[TextButton("OK", on_click=self.close_dlg_block)],
            on_dismiss=lambda e: print("Modal dialog dismissed!")
        )
#!
        self.alter_dialog_preview = AlertDialog(
            modal=True,
            title=Text(
                value="Предпросмотр",
                size=16,
                color=primary_colors['GREEN'],
                text_align='center',
                weight='bold',
                width=60,
            ),
            content=ListView(
                height=500,
                width=2000,
                controls=[
                    # *3RD ROW
                    Container(
                        content=self.data_table,
                        alignment=alignment.center,
                        padding=padding.all(20),
                    )
                ]
            ),

            actions=[
                TextButton("Редактировать", on_click=self.show_edit_preview_dialog),
                TextButton("Удалить", on_click=self.delete_preview_data),
                TextButton("Закрыть", on_click=self.close_preview_dialog),
            ],
            actions_alignment=MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
#!
        self.first_qr_box_2 = Container(
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
                width=100,
                on_change=self.validate
            ),
        )
        self.second_qr_box_2 = Container(
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
                width=100,
                on_change=self.validate
            ),
        )
        self.third_qr_box_2 = Container(
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
                width=100,
                on_change=self.validate
            ),
        )
        self.fourtht_qr_box_2 = Container(
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
                width=100,
                on_change=self.validate
            ),
        )
        self.year_box_2 = Container(
            content=TextField(
                hint_style=TextStyle(
                    size=12, color=primary_colors['MANATEE']
                ),
                label='год',
                cursor_color=primary_colors['MANATEE'],
                text_style=TextStyle(
                    size=14,
                    color=primary_colors['GREEN'],
                ),
                width=100,
                on_change=self.validate
            ),
        )


        self.weight_first_qr_box_2 = Container(
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
                width=100,
                on_change=self.validate
            ),
        )
        self.weight_second_qr_box_2 = Container(
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
                width=100,
                on_change=self.validate
            ),
        )
        self.weight_third_qr_box_2 = Container(
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
                width=100,
                on_change=self.validate
            ),
        )
        self.weight_fourth_qr_box_2 = Container(
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
                width=100,
                on_change=self.validate
            ),
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
                                self.first_qr_box_2,
                                self.second_qr_box_2,
                                self.third_qr_box_2,
                                self.fourtht_qr_box_2,
                                self.year_box_2,
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
                                # * THERE ARE MY NEXT BOXES FOR MY 3RD ROW
                                self.weight_first_qr_box_2,
                                self.weight_second_qr_box_2,
                                self.weight_third_qr_box_2,
                                self.weight_fourth_qr_box_2,
                            ]
                        )
                    ),
                ]
            ),
            actions=[
                TextButton("Изменить", on_click=self.edit_preview_data),
                TextButton("Закрыть", on_click=self.close_edit_dialog),
            ],
            actions_alignment=MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )




        # *ELEVATED BUTTNON
        self.elevated_button_end = Container(
            content=ElevatedButton(
                color=primary_colors['WHITE'],
                bgcolor=primary_colors['WHITE'],
                width=250,
                height=70,
                content=Column(
                    horizontal_alignment='center',
                    alignment='center',
                    controls=[
                        Container(
                            Text(
                                value='Закончить формирование КПЭ',
                                size=16,
                                color=primary_colors['GREEN'],
                                text_align='center',
                                weight='bold',
                            )
                        )
                    ]
                ),
                on_click=self.show_blocked
            )
        )
        # *THIS IS A HEADER
        self.content = Column(
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
                                                value='Ввести карту КПЭ',
                                                size=18,
                                                color=primary_colors['WHITE'],
                                                text_align='center',
                                            ),
                                        ),
                                        Container(
                                            # width=200,
                                            content=Row(
                                                spacing=10,
                                                controls=[
                                                    Container(
                                                        content=ElevatedButton(
                                                            bgcolor=primary_colors['WHITE'],
                                                            width=170,
                                                            height=70,
                                                            content=Column(
                                                                horizontal_alignment='center',
                                                                alignment='center',
                                                                controls=[
                                                                    Container(
                                                                        Text(
                                                                            value='Предпросмотр КПЭ',
                                                                            size=16,
                                                                            color=primary_colors['GREEN'],
                                                                            text_align='center',
                                                                            weight='bold',
                                                                        )
                                                                    )
                                                                ]
                                                            ),
                                                            on_click=self.preview,
                                                        ),
                                                    ),
                                                    self.elevated_button_end,
                                                ]
                                            )
                                        ),
                                    ]
                                )
                            )
                        ],
                    )
                ),

                # *THERE ARE MANUAL BUTTONS FOR THIS FORM
                Container(
                    expand=True,
                    bgcolor=primary_colors['WHITE'],
                    content=Column(
                        expand=True,
                        # alignment='center',
                        horizontal_alignment='center',
                        controls=[
                            # *1ST ROW
                            Container(height=50),
                            Container(
                                Row(
                                    spacing='50',
                                    alignment='center',
                                    # horizontal_alignment='center',
                                    controls=[
                                        # Container(width=90)
                                        self.name_of_department_menu_box,
                                        self.specialist_menu_box,
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
                            Container(height=50),
                            # *4TH ROW
                            Container(
                                Row(
                                    alignment='center',
                                    # horizontal_alignment='center',
                                    controls=[
                                        ElevatedButton(
                                            color=primary_colors['WHITE'],
                                            bgcolor=primary_colors['GREEN'],
                                            width=400,
                                            height=100,
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
                                            # on_click=lambda x: x == self.page.go('/home')
                                            on_click=self.insert_into_db
                                        ),
                                    ]
                                )
                            ),
                        ],
                    )
                ),
            ]
        )
    def validate(self, e):
        txt_field = e.control
        current_text = txt_field.value
        if not current_text.replace('.', '', 1).isdigit():
            txt_field.value = ''.join(filter(lambda x: x.isdigit() or x == '.', current_text[:-1]))
        txt_field.update() 

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
            sql_select_specialist_id = f"SELECT specialist_id FROM specialists WHERE full_name = '{self.specialist_menu_box.content.value}'"
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

    def added_new_to_indicators(self, e):
        selected_item = self.cb_menu_spec.content.value 
        print(f"Selected item: {selected_item}")
        if selected_item == "Нет в списке":
            self.page.dialog = self.alter_dialog
            print("Opening dialog...")
            self.alter_dialog.open = True
        self.page.update()

    def alter_dialoge_input_data(self, e):
        try:
            cursor = connection.cursor()
            sql_select_specialist_id = "SELECT specialist_id FROM specialists WHERE full_name = '{}'".format(self.specialist_menu_box.content.value)
            cursor.execute(sql_select_specialist_id)
            specialist_id = cursor.fetchone()[0]
            cursor.execute(f"SELECT measurement_id FROM units_of_measurement WHERE type = '{self.units_menu_box.content.value}'")
            units_id = cursor.fetchone()[0]
            cursor.execute(f"SELECT max(indicators_id) FROM name_of_indicators;")
            max_id = cursor.fetchone()[0]
            new_indicator_name = self.textfiled_input_new_indicator.content.value
            new_indicator_id = max_id + 1
            query = "INSERT INTO TABLE name_of_indicators (indicators_id, measurement_id, name, specialist_id) VALUES ({},{},'{}',{})".format(
                new_indicator_id, units_id, new_indicator_name, specialist_id)
            cursor.execute(query)
            connection.commit()
            print("Запись успешно добавлена в базу данных")
            self.dropdown_options_indicators.clear()
            self.show_indicators("")
            self.cb_menu_spec.content.value = str(new_indicator_id)
            self.textfiled_input_new_indicator.content.value = ''
            self.units_menu_box.content.value = ''
            self.alter_dialog.open = False
            self.page.update()
        except Exception as e:
            print(f"Ошибка при добавлении записи в базу данных: {str(e)}")

    def close_dlg(self, e):
        self.page.dialog = self.alter_dialog
        self.alter_dialog.open = False
        self.page.update()

    def show_block_dialog(self, content_text, title_text):
        self.page.dialog = self.alter_dialog_block
        self.alter_dialog_block.content = Text(f"{content_text}")
        self.alter_dialog_block.title = Text(f"{title_text}")
        self.alter_dialog_block.open = True
        self.page.update()

    def close_dlg_block(self, e):
        self.page.dialog = self.alter_dialog_block
        self.alter_dialog_block.open = False
        print("Вы закрыли модульное окно блокировки")
        self.page.update()

    def show_blocked(self, e):
        try:
            date = datetime.datetime.now()
            formatted_date = date.strftime("%Y%m%d")
            # *FOR AUTO ID INCRIPTION
            cursor = connection.cursor()
            cursor.execute(f"SELECT max(plan_id) FROM planned_value;")
            max_plan_id = cursor.fetchone()[0]
            query_select = 'SELECT plan_indicators_id FROM planned_value'
            cursor.execute(query_select)

            query_select = f"""
            SELECT
                plan_specialist_id,
                plan_indicators_id,
                MAX(date) AS latest_date,
                MAX(number) AS latest_number
            FROM planned_value
            WHERE plan_specialist_id = (SELECT specialist_id FROM specialists WHERE full_name = '{self.specialist_menu_box.content.value}')
            GROUP BY
                plan_specialist_id,
                plan_indicators_id
            ORDER BY plan_indicators_id
            """
            cursor.execute(query_select)
            latest_data = cursor.fetchall()
            if not latest_data:
                self.show_block_dialog('Карта КПЭ выбранного специалиста пуста', 'Ошибка')
            else:
                for specialist_id, indicator_id, latest_date, latest_number in latest_data:
                    query_max_number = f"""
                    SELECT MAX(number)
                    FROM planned_value
                    WHERE plan_specialist_id = {int(specialist_id)} 
                    AND plan_indicators_id = {int(indicator_id)} 
                    AND date = '{latest_date}'
                    """
                    cursor.execute(query_max_number)
                    current_version = cursor.fetchone()[0] or 0

                    max_plan_id += 1
                    query_exists = """
                        SELECT 1
                        FROM kpe_table
                        WHERE kpe_specialist_id = {}
                        AND kpe_indicators_id = {}
                        AND date = '{}'
                        AND number = {}
                    """.format(specialist_id, indicator_id, latest_date, latest_number)
                    cursor.execute(query_exists)
                    data_exists = cursor.fetchone()
                    if not data_exists:
                        query_select = """
                        SELECT plan_indicators_id, plan_specialist_id, plan_units_id, 1st_quater_value, 2nd_quater_value, 3rd_quater_value, 4th_quater_value, year, status,
                            KPE_weight_1, KPE_weight_2, KPE_weight_3, KPE_weight_4
                        FROM planned_value
                        WHERE
                        date = '{}'
                        AND number = {}
                        AND plan_indicators_id = {}
                        AND plan_specialist_id = {}
                        AND status = 'Активно'
                        """.format(latest_date, latest_number, indicator_id, specialist_id)
                        cursor.execute(query_select)
                        data = cursor.fetchone()
                        if data:
                            plan_indicators_id, specialist_id, units_id, first_qr_value, second_qr_value, third_qr_value, fourth_qr_value, year, status, weight_1, weight_2, weight_3, weight_4 = data
                            weight_query = f"""
                            SELECT
                                SUM(KPE_weight_1) AS total_weight_1,
                                SUM(KPE_weight_2) AS total_weight_2,
                                SUM(KPE_weight_3) AS total_weight_3,
                                SUM(KPE_weight_4) AS total_weight_4
                            FROM planned_value
                            WHERE plan_specialist_id = {specialist_id} 
                            AND status = 'Активно'
                            AND date = '{latest_date}'
                            AND number = {latest_number}
                            """
                            cursor.execute(weight_query)
                            sum_weight_1, sum_weight_2, sum_weight_3, sum_weight_4 = cursor.fetchone()
                            print(sum_weight_1)
                            print(sum_weight_2)
                            print(sum_weight_3)
                            print(sum_weight_4)
                            if sum_weight_1 < 100 or sum_weight_2 < 100 or sum_weight_3 < 100 or sum_weight_4 < 100:
                                self.show_block_dialog(
                                    f"Сумма Веса КПЭ\n1 квартала = {sum_weight_1}%\n2 квартала = {sum_weight_2}%\n3 квартала = {sum_weight_3}%\n4 квартала = {sum_weight_4}%\nСумма каждого квартала должна равняться 100%", 
                                    "Предупреждение"
                                )
                            else:
                                insert_query_to_kpe_table = """
                                INSERT INTO
                                    kpe_table (
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
                                VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, '{}', {}, {}, {}, {}, {}, '{}', {});
                                """.format(
                                        int(max_plan_id),
                                        int(plan_indicators_id),
                                        int(specialist_id),
                                        int(units_id),
                                        float(first_qr_value),
                                        float(second_qr_value),
                                        float(third_qr_value),
                                        float(fourth_qr_value),
                                        float(year),
                                        str(status),
                                        float(weight_1),
                                        float(weight_2),
                                        float(weight_3),
                                        float(weight_4),
                                        int(self.user_id),
                                        str(formatted_date),
                                        int(current_version)
                                    )
                                cursor.execute(insert_query_to_kpe_table)
                                print("Success")
                                self.specialist_menu_box.content.value = ""
                                self.show_block_dialog("Вы завершили формирование карты КПЭ","Карта КПЭ сформирована")
                    else:
                        self.show_block_dialog("Данные уже есть в карте КПЭ","Информация")
        except Exception as ex:
            print(ex)
            self.show_block_dialog("Произошла ошибка","Ошибка")


    def insert_into_db(self, e):
        if self.end_edit == False:
            try:
                field_names_mapping = {
                'first_qr_box': '1 квартал',
                'second_qr_box': '2 квартал',
                'third_qr_box': '3 квартал',
                'fourtht_qr_box': '4 квартал',
                'year_box': 'год',
                'weight_first_qr_box': 'Вес 1 квартал',
                'weight_second_qr_box': 'Вес 2 квартал',
                'weight_third_qr_box': 'Вес 3 квартал',
                'weight_fourth_qr_box': 'Вес 4 квартал',
                'cb_menu_spec': 'Наименование показателя',
                'specialist_menu_box': 'Специалиста'
                }
                required_fields = [
                    self.first_qr_box.content.value,
                    self.second_qr_box.content.value,
                    self.third_qr_box.content.value,
                    self.fourtht_qr_box.content.value,
                    self.year_box.content.value,
                    self.weight_first_qr_box.content.value,
                    self.weight_second_qr_box.content.value,
                    self.weight_third_qr_box.content.value,
                    self.weight_fourth_qr_box.content.value,
                    self.cb_menu_spec.content.value,
                    self.specialist_menu_box.content.value
                ]
                empty_fields = [field_names_mapping[field_name] for field_name, field_value in zip(
                    ['first_qr_box', 'second_qr_box', 'third_qr_box', 'fourtht_qr_box', 'year_box',
                    'weight_first_qr_box', 'weight_second_qr_box', 'weight_third_qr_box',
                    'weight_fourth_qr_box', 'cb_menu_spec', 'specialist_menu_box'], required_fields)
                    if not field_value]
                if empty_fields:
                    error_message = f"Вы не заполнили следующие поля:\n{', '.join(empty_fields)}"
                    print(f"Error: {error_message}")
                    self.show_block_dialog(error_message, "Ошибка")
                    return
                date = datetime.datetime.now()
                formatted_date = date.strftime("%Y%m%d")
                cursor = connection.cursor()
                cursor.execute(
                    f"SELECT specialist_id FROM specialists WHERE full_name='{str(self.specialist_menu_box.content.value)}';")
                specialist_id = cursor.fetchone()[0]
                cursor.execute(f"SELECT max(plan_id) FROM planned_value;")
                max_id = cursor.fetchone()[0]
                cursor.execute(
                    f"SELECT measurement_id FROM name_of_indicators WHERE indicators_id = '{int(self.cb_menu_spec.content.value)}'")
                units_id = cursor.fetchone()[0]
                cursor.execute(
                    f"""
                    SELECT 
                        concat(
                            toString(plan_specialist_id), '-',
                            substring(replace(toString(date), '-', ''), 7, 2),
                            substring(replace(toString(date), '-', ''), 5, 2),
                            substring(replace(toString(date), '-', ''), 1, 4),
                            '-', toString(number)
                        ) AS number_of_version
                    FROM planned_value
                    WHERE 
                        plan_specialist_id = {int(specialist_id)} AND 
                        plan_indicators_id = {int(self.cb_menu_spec.content.value)} AND
                        date = (
                            SELECT MAX(date)
                            FROM planned_value
                            WHERE plan_specialist_id = {int(specialist_id)} AND plan_indicators_id = {int(self.cb_menu_spec.content.value)}
                        ) AND 
                        number = (
                            SELECT MAX(number)
                            FROM planned_value
                            WHERE 
                                plan_specialist_id = {int(specialist_id)} AND 
                                plan_indicators_id = {int(self.cb_menu_spec.content.value)} AND
                                date = (
                                    SELECT MAX(date)
                                    FROM planned_value
                                    WHERE plan_specialist_id = {int(specialist_id)} AND plan_indicators_id = {int(self.cb_menu_spec.content.value)}
                                )
                        );
                    """
                    )
                max_version = cursor.fetchone()
                if max_version is None:
                    current_version = 1
                else:
                    current_version = int(max_version[0].split('-')[2]) + 1
                query = """
                    INSERT INTO planned_value (
                        plan_id, 
                        plan_indicators_id, 
                        plan_specialist_id, 
                        plan_units_id, 
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
                        plan_user_id,
                        date, 
                        number
                    )
                    VALUES ({}+1, {}, {}, {}, {}, {}, {}, {}, {},'{}', {}, {}, {}, {},{},'{}', {});
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
                        str(formatted_date),
                        int(current_version)
                    )
                cursor.execute(query)
                connection.commit()
                self.show_block_dialog("Запись успешно добавлена в базу данных","Успешно")
                self.first_qr_box.content.value = ''
                self.second_qr_box.content.value = ''
                self.third_qr_box.content.value = ''
                self.fourtht_qr_box.content.value = ''
                self.year_box.content.value = ''
                self.weight_first_qr_box.content.value = ''
                self.weight_second_qr_box.content.value = ''
                self.weight_third_qr_box.content.value = ''
                self.weight_fourth_qr_box.content.value = ''
                self.cb_menu_spec.content.value = ''
                self.units_menu_box.content.value = ""
                print("Запись успешно добавлена в базу данных")
            except Exception as e:
                self.show_block_dialog("Ошибка при добавлении записи в базу данных","Ошибка")
                print(f"Ошибка при добавлении записи в базу данных: {str(e)}")
        else:
            print("Blocked")

    def preview(self, e):
        try:
            self.selected_rows.clear()
            cursor = connection.cursor()
            cursor.execute(
                f"SELECT specialist_id FROM specialists WHERE full_name='{str(self.specialist_menu_box.content.value)}';")
            specialist_id = cursor.fetchone()[0]
            query_select = f"""
            SELECT
                ROW_NUMBER() OVER (ORDER BY plan_id) AS "порядковый номер",
                ni.name AS indicator_name,
                um.type AS unit_of_measurement,
                pn.1st_quater_value,
                pn.2nd_quater_value,
                pn.3rd_quater_value,
                pn.4th_quater_value,
                pn.year,
                pn.KPE_weight_1,
                pn.KPE_weight_2,
                pn.KPE_weight_3,
                pn.KPE_weight_4
            FROM planned_value AS pn
            JOIN name_of_indicators AS ni ON pn.plan_indicators_id = ni.indicators_id
            JOIN units_of_measurement AS um ON pn.plan_units_id = um.measurement_id
            WHERE
                pn.plan_specialist_id = {int(specialist_id)} AND
                pn.status = 'Активно' AND
                pn.date = (
                    SELECT MAX(date)
                    FROM planned_value
                    WHERE plan_specialist_id = {int(specialist_id)} AND status = 'Активно'
                ) AND
                pn.number = (
                    SELECT MAX(number)
                    FROM planned_value
                    WHERE
                        plan_specialist_id = {int(specialist_id)} AND
                        status = 'Активно' AND
                        date = (
                            SELECT MAX(date)
                            FROM planned_value
                            WHERE plan_specialist_id = {int(specialist_id)} AND status = 'Активно'
                        )
                )
            ORDER BY plan_id;
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
            self.page.dialog = self.alter_dialog_preview
            self.alter_dialog_preview.open = True
            self.page.update()
        except:
            self.show_block_dialog("Вы не выбрали специалиста","Ошибка")

    def close_preview_dialog(self, e):
        self.page.dialog = self.alter_dialog_preview
        self.alter_dialog_preview.open = False
        print("Вы закрыли модульное окно блокировки")
        self.page.update()

    def toggle_row_selection(self, e, row):
        # Toggle the row's selection when the Checkbox value changes
        if row not in self.selected_rows:
            self.selected_rows.add(row)
            print("yes")
        else:
            self.selected_rows.remove(row)
            print("no")

    def show_edit_preview_dialog(self, e):
        selected_row = next(iter(self.selected_rows))
        self.first_qr_box_2.content.value = selected_row[3]
        self.second_qr_box_2.content.value = selected_row[4]
        self.third_qr_box_2.content.value = selected_row[5]
        self.fourtht_qr_box_2.content.value = selected_row[6]
        self.year_box_2.content.value = selected_row[7]
        self.weight_first_qr_box_2.content.value = selected_row[8]
        self.weight_second_qr_box_2.content.value = selected_row[9]
        self.weight_third_qr_box_2.content.value = selected_row[10]
        self.weight_fourth_qr_box_2.content.value = selected_row[11]
        self.page.dialog = self.alter_dialog_edit
        self.alter_dialog_edit.open = True
        self.page.update()

    def edit_preview_data(self, e):
        # try:
            selected_row = next(iter(self.selected_rows))
            
            cursor = connection.cursor()
            sql_select = "SELECT plan_id FROM planned_value WHERE 1st_quater_value = {} AND 2nd_quater_value = {} AND 3rd_quater_value = {} AND 4th_quater_value = {} AND year = {} AND KPE_weight_1 = {} AND KPE_weight_2 = {} AND KPE_weight_3 = {} AND KPE_weight_4 = {};".format(
                selected_row[3], selected_row[4], selected_row[5], selected_row[6], selected_row[7], selected_row[8],
                selected_row[9], selected_row[10], selected_row[11])
            cursor.execute(sql_select)
            plan_id = cursor.fetchone()[0]
            if self.first_qr_box.content.value != selected_row[3]:
                query_1st_qr = "ALTER TABLE planned_value UPDATE 1st_quater_value = {} WHERE plan_id = {};".format(self.first_qr_box_2.content.value, plan_id)
                cursor.execute(query_1st_qr)
                self.page.dialog = self.alter_dialog_edit
                self.alter_dialog_edit.open = False
            if self.second_qr_box.content.value != selected_row[4]:
                query_2nd_qr = "ALTER TABLE planned_value UPDATE 2nd_quater_value = {} WHERE plan_id = {};".format(self.second_qr_box_2.content.value, plan_id)
                cursor.execute(query_2nd_qr)
                self.page.dialog = self.alter_dialog_edit
                self.alter_dialog_edit.open = False
            if self.third_qr_box.content.value != selected_row[5]:
                query_3rd_qr = "ALTER TABLE planned_value UPDATE 3rd_quater_value = {} WHERE plan_id = {};".format(self.third_qr_box_2.content.value, plan_id)
                cursor.execute(query_3rd_qr)
                self.page.dialog = self.alter_dialog_edit
                self.alter_dialog_edit.open = False
            if self.fourtht_qr_box.content.value != selected_row[6]:
                query_4th_qr = "ALTER TABLE planned_value UPDATE 4th_quater_value = {} WHERE plan_id = {};".format(self.fourtht_qr_box_2.content.value, plan_id)
                cursor.execute(query_4th_qr)
                self.page.dialog = self.alter_dialog_edit
                self.alter_dialog_edit.open = False
            if self.year_box.content.value != selected_row[7]:
                query_year = "ALTER TABLE planned_value UPDATE year = {} WHERE plan_id = {};".format(self.year_box_2.content.value, plan_id)
                cursor.execute(query_year)
                self.page.dialog = self.alter_dialog_edit
                self.alter_dialog_edit.open = False
            if self.weight_first_qr_box.content.value != selected_row[8]:
                query_weight_firts_qr = "ALTER TABLE planned_value UPDATE KPE_weight_1 = {} WHERE plan_id = {};".format(self.weight_first_qr_box_2.content.value, plan_id)
                cursor.execute(query_weight_firts_qr)
                self.page.dialog = self.alter_dialog_edit
                self.alter_dialog_edit.open = False
            if self.weight_second_qr_box.content.value != selected_row[9]:
                query_weight_second_qr = "ALTER TABLE planned_value UPDATE KPE_weight_2 = {} WHERE plan_id = {};".format(self.weight_second_qr_box_2.content.value, plan_id)
                cursor.execute(query_weight_second_qr)
                self.page.dialog = self.alter_dialog_edit
                self.alter_dialog_edit.open = False
            if self.weight_third_qr_box.content.value != selected_row[10]:
                query_weight_third_qr = "ALTER TABLE planned_value UPDATE KPE_weight_3 = {} WHERE plan_id = {};".format(self.weight_third_qr_box_2.content.value, plan_id)
                cursor.execute(query_weight_third_qr)
                self.page.dialog = self.alter_dialog_edit
                self.alter_dialog_edit.open = False
            if self.weight_fourth_qr_box.content.value != selected_row[11]:
                query_weight_fourth_qr = "ALTER TABLE planned_value UPDATE KPE_weight_4 = {} WHERE plan_id = {};".format(self.weight_fourth_qr_box_2.content.value, plan_id)
                cursor.execute(query_weight_fourth_qr)
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
            self.show_block_dialog("Данные были успешно занесены в список изменений", "Успешно")
            self.page.update()
        # except:
        #     self.show_block_dialog("При изменении данных произошла ошибка", "Ошибка")

    def close_edit_dialog(self, e):
        self.page.dialog = self.alter_dialog_edit
        self.alter_dialog_edit.open = False
        self.preview(e)
        self.page.update()

    def delete_preview_data(self, e):
        cursor = connection.cursor()
        for selected_row in self.selected_rows:
            cursor.execute(f"SELECT specialist_id FROM specialists WHERE full_name='{str(self.specialist_menu_box.content.value)}';")
            specialist_id = cursor.fetchone()[0]
            indicator = f"SELECT indicators_id FROM name_of_indicators WHERE name = '{selected_row[1]}' AND specialist_id = '{specialist_id}'"
            # print(indicator)
            cursor.execute(indicator)
            indicator_id = cursor.fetchone()[0]
            # print(indicator_id)
            sql_select = "SELECT plan_id FROM planned_value WHERE plan_specialist_id = {} AND plan_indicators_id = {} AND 1st_quater_value = {} AND 2nd_quater_value = {} AND 3rd_quater_value = {} AND 4th_quater_value = {} AND year = {} AND KPE_weight_1 = {} AND KPE_weight_2 = {} AND KPE_weight_3 = {} AND KPE_weight_4 = {};".format(
                specialist_id, indicator_id, selected_row[3], selected_row[4], selected_row[5], selected_row[6], selected_row[7], selected_row[8], selected_row[9], selected_row[10], selected_row[11])
            cursor.execute(sql_select)
            print(sql_select)
            plan_id = cursor.fetchone()[0]
            print(plan_id)
            query_delete = "DELETE FROM planned_value WHERE plan_id = {};".format(plan_id)
            cursor.execute(query_delete)
        self.page.dialog = self.alter_dialog_preview
        self.alter_dialog_preview.open = False
        self.show_block_dialog("Запись была успешно удалена", "Успешно")
        self.page.update()