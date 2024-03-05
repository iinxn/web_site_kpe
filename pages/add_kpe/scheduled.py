import datetime
from flet import *
from service.connection import *
from utils.colors import *


class Scheduled(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        # page.theme = theme.Theme(color_scheme_seed="green")
        self.page.theme_mode = ThemeMode.LIGHT
        self.alignment = alignment.center
        self.expand = True
        self.bgcolor = '#FFFFFF'
        self.end_edit = False

        self.use_truncated_options = True
        self.dropdown_options_indicators = []
        self.dropdown_options_indicators_truncated = []
        dropdown_options_specialists = []
        dropdown_options_units = []
        self.kpe_weight_1 = []
        self.kpe_weight_2 = []
        self.kpe_weight_3 = []
        self.kpe_weight_4 = []
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
            border=border.all(1, "black"),
            vertical_lines=border.BorderSide(1, "black"),
            horizontal_lines=border.BorderSide(1, "black"),
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

        # *SELECT QUERY TO DISPLAY SPECIALISTS FROM DB
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT full_name FROM specialists ORDER BY specialist_id')
            results = cursor.fetchall()

            for row in results:
                dropdown_options_specialists.append(dropdown.Option(row[0]))
        except Exception as e:
            print(f"Error fetching data from the database: {str(e)}")

        # *THERE ARE MY BOXES FOR 2ND ROW
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
                label='год',
                cursor_color='#858796',
                text_style=TextStyle(
                    size=14,
                    color='#5B7553',
                ),
                width=100
            ),
        )
        # * THERE ARE MY NEXT BOXES FOR MY 3RD ROW
        self.weight_first_qr_box = Container(
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
        self.weight_second_qr_box = Container(
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
        self.weight_third_qr_box = Container(
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
        self.weight_fourth_qr_box = Container(
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
                width=400
            ),
        )
        # *DROPDOWN MENU
        # Create the Dropdown container
        self.cb_menu_spec = Container(
            content=Dropdown(
                label='Выберите наименование показателя',
                color="black",
                width=360,
                # filled=True,
                options=self.dropdown_options_indicators_truncated,
                on_change=self.added_new_to_indicators,
            ),
        )
        self.units_menu_box = Container(
            content=Dropdown(
                hint_text='ед. изм.',
                color="black",
                width=300,
                options=dropdown_options_units,  # Set the options from the fetched data
            ),
        )
        self.specialist_menu_box = Container(
            content=Dropdown(
                hint_text='Выберите специалиста',
                color="black",
                width=330,
                options=dropdown_options_specialists,
                on_change=self.show_indicators
            )
        )
        # *MODULE FORM
        self.alter_dialog = AlertDialog(
            modal=True,
            title=Text("Добавление показателя в справочник"),
            content=Container(
                width=800,
                content = Row(
                    spacing='30',
                    alignment='center',
                    controls=[
                        self.textfiled_input_new_indicator,
                        self.units_menu_box
                    ]
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
                color='#5B7553',
                text_align='center',
                weight='bold',
                width=60,
            ),
            content=Column(
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
        self.second_qr_box_2 = Container(
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
        self.third_qr_box_2 = Container(
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
        self.fourtht_qr_box_2 = Container(
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
        self.year_box_2 = Container(
            content=TextField(
                hint_style=TextStyle(
                    size=12, color='#858796'
                ),
                label='год',
                cursor_color='#858796',
                text_style=TextStyle(
                    size=14,
                    color='#5B7553',
                ),
                width=100
            ),
        )


        self.weight_first_qr_box_2 = Container(
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
        self.weight_second_qr_box_2 = Container(
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
        self.weight_third_qr_box_2 = Container(
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
        self.weight_fourth_qr_box_2 = Container(
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
                                    color='#5B7553',
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
                color=white,
                bgcolor='white',
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
                                color='#5B7553',
                                text_align='center',
                                weight='bold',
                            )
                        )
                    ]
                ),
                on_click=self.end_input_data
            )
        )
        # *THIS IS A HEADER
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
                                                value='Ввести карту КПЭ',
                                                size=18,
                                                color='white',
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
                                                            bgcolor=white,
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
                                                                            color='#5B7553',
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
                    bgcolor='white',
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
                            Container(height=50),
                            # *4TH ROW
                            Container(
                                Row(
                                    alignment='center',
                                    # horizontal_alignment='center',
                                    controls=[
                                        ElevatedButton(
                                            color=white,
                                            bgcolor='#5B7553',
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
                                                            color=white,
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

    def show_indicators(self, e):
      # *SELECT QUERY TO DIPLAY NAMES OF INDICATORS FROM DB
        try:
            self.dropdown_options_indicators.clear()
            self.dropdown_options_indicators_truncated.clear()
            cursor = connection.cursor()
            sql_select_specialist_id = "SELECT specialist_id FROM specialists WHERE full_name = '{}'".format(self.specialist_menu_box.content.value)
            cursor.execute(sql_select_specialist_id)
            specialist_id = cursor.fetchone()[0]
            
            cursor.execute('SELECT name FROM name_of_indicators WHERE specialist_id = {} ORDER BY indicators_id'.format(specialist_id))
            results = cursor.fetchall()
            max_length = 40
            for row in results:
                truncated_text = row[0] if len(row[0]) <= max_length else row[0][:max_length] + "..."
                self.dropdown_options_indicators.append(dropdown.Option(row[0]))
                self.z.append(dropdown.Option(truncated_text))

            # Add "Нет в списке" option at the end
            self.dropdown_options_indicators.append(dropdown.Option('Нет в списке'))
            self.dropdown_options_indicators_truncated.append(dropdown.Option('Нет в списке'))
            self.page.update()
        except Exception as e:
            print(f"Error fetching data from the database: {str(e)}")
    
    
    def end_input_data(self, e):
        self.show_blocked()

    def added_new_to_indicators(self, e):
        selected_item = self.cb_menu_spec.content.value  # Получите выбранную опцию
        print(f"Selected item: {selected_item}")  # Отладочный вывод: Выведите выбранную опцию
        if selected_item == "Нет в списке":
            self.page.dialog = self.alter_dialog
            print("Opening dialog...")  # Отладочный вывод: Откройте диалоговое окно
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
            query = "INSERT INTO TABLE name_of_indicators (indicators_id, measurement_id, name, specialist_id) VALUES ({}+1,{},'{}',{})".format(
                int(max_id), units_id, self.textfiled_input_new_indicator.content.value, specialist_id)
            cursor.execute(query)
            print("Запись успешно добавлена в базу данных")
            self.cb_menu_spec.content.value = self.textfiled_input_new_indicator.content.value
            self.textfiled_input_new_indicator.content.value = ''
            self.units_menu_box.content.value = ''
            #clear indicators cb and add new data
            self.dropdown_options_indicators_truncated.clear()
            self.show_indicators("")
            self.page.dialog = self.alter_dialog
            self.alter_dialog.open = False
            self.page.update()
        except Exception as e:
            print(f"Ошибка при добавлении записи в базу данных: {str(e)}")

    def close_dlg(self, e):
        self.page.dialog = self.alter_dialog
        self.alter_dialog.open = False
        self.page.update()

    # TODO: These two functions for succes message

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
    
    # TODO: These two functions for blocked message
    def show_blocked(self):
        # try:

        date = datetime.datetime.now()
        formatted_date = date.strftime("%d%m%Y")

        # *FOR AUTO ID INCRIPTION
        cursor = connection.cursor()
        cursor.execute(f"SELECT max(kpe_id) FROM kpe_table;")
        max_kpe_id = cursor.fetchone()[0]

        query_select = 'SELECT plan_indicators_id FROM planned_value'
        cursor.execute(query_select)
        indicator_original_list = cursor.fetchall()
        indicators = [item[0] for item in indicator_original_list]

        query_select = """
        SELECT
            plan_user_id,
            plan_indicators_id,
            MAX(number_of_version) AS latest_version
        FROM planned_value
        GROUP BY
            plan_user_id,
            plan_indicators_id
        ORDER BY plan_indicators_id
        """
        cursor.execute(query_select)
        latest_number_of_version_with_user_indicator_ids = cursor.fetchall()
        # Loop through the results of the first query

        for specialist_id, indicator_id, latest_version in latest_number_of_version_with_user_indicator_ids:
            cursor.execute(
                f"SELECT MAX(number_of_version) FROM kpe_table WHERE kpe_indicators_id = {int(indicator_id)} AND kpe_user_id = {int(specialist_id)}")
            max_version = cursor.fetchone()[0]
            # Check if max_version has the expected format (3 hyphen-separated parts)
            if max_version and len(max_version.split('-')) >= 3:
                current_version = int(max_version.split('-')[2])
            else:
                current_version = 0  # Start with version 1 if the format is unexpected or max_version is None

            number_of_verison_plus = f"{1}-{formatted_date}-{current_version + 1}"

            max_kpe_id += 1
            query_exists = """
                SELECT 1
                FROM kpe_table
                WHERE kpe_user_id = {}
                AND kpe_indicators_id = {}
                AND number_of_version = '{}'
            """.format(specialist_id, indicator_id, latest_version)
            cursor.execute(query_exists)
            data_exists = cursor.fetchone()
            if not data_exists:
                # Получение данных из planned_value
                query_select = """
                SELECT plan_indicators_id, plan_user_id, plan_units_id, 1st_quater_value, 2nd_quater_value, 3rd_quater_value, 4th_quater_value, year, status,
                    KPE_weight_1, KPE_weight_2, KPE_weight_3, KPE_weight_4
                FROM planned_value
                WHERE
                number_of_version = '{}'
                AND plan_indicators_id = {}
                AND plan_user_id = {}
                AND status = 'Активно'
            """.format(latest_version, indicator_id, specialist_id)
                cursor.execute(query_select)
                data = cursor.fetchone()

                if data:
                    plan_indicators_id, user_id, units_id, first_qr_value, second_qr_value, third_qr_value, fourth_qr_value, year, status, weight_1, weight_2, weight_3, weight_4 = data
                    print(sum(self.kpe_weight_1))
                    print(sum(self.kpe_weight_2))
                    print(sum(self.kpe_weight_3))
                    print(sum(self.kpe_weight_4))
                    weight_1_below_100 = sum(self.kpe_weight_1) != 100
                    weight_2_below_100 = sum(self.kpe_weight_2) != 100
                    weight_3_below_100 = sum(self.kpe_weight_3) != 100
                    weight_4_below_100 = sum(self.kpe_weight_4) != 100

                    if weight_1_below_100 or weight_2_below_100 or weight_3_below_100 or weight_4_below_100:
                        messages = []
                        if weight_1_below_100:
                            messages.append("1 квартала")
                        if weight_2_below_100:
                            messages.append("2 квартала")
                        if weight_3_below_100:
                            messages.append("3 квартала")
                        if weight_4_below_100:
                            messages.append("4 квартала")
                        # self.show_block_dialog(f"Сумма Веса КПЭ {', '.join(messages)} меньше 100%","Предупреждение")
                        self.show_block_dialog(f"Сумма Веса КПЭ\n1 квартала = {sum(self.kpe_weight_1)}%\n2 квартала = {sum(self.kpe_weight_2)}%\n3 квартала = {sum(self.kpe_weight_3)}%\n4 квартала = {sum(self.kpe_weight_4)}%\nСумма каждого квартала должна равняться 100%","Предупреждение")
                    else:
                        # Вставка данных в kpe_table
                        insert_query_to_kpe_table = """
                        INSERT INTO
                            kpe_table (
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
                            number_of_version, 
                            plan_number_of_version
                            )
                        VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, '{}', {}, {}, {}, {}, '{}','{}');
                        """.format(
                                int(max_kpe_id),
                                int(plan_indicators_id),
                                int(user_id),
                                int(units_id),
                                int(first_qr_value),
                                int(second_qr_value),
                                int(third_qr_value),
                                int(fourth_qr_value),
                                int(year),
                                str(status),
                                int(weight_1),
                                int(weight_2),
                                int(weight_3),
                                int(weight_4),
                                str(number_of_verison_plus),
                                str(latest_version)
                            )
                        # print("SQL Query:", insert_query_to_kpe_table)

                        cursor.execute(insert_query_to_kpe_table)
                        print("Success")
                        self.specialist_menu_box.content.value = ""
                        self.show_block_dialog("Вы завершили формирование карты КПЭ","Карта КПЭ сформирована")
                else:
                    self.show_block_dialog("Данные уже есть в карте КПЭ","Информация")
                    print("All data is in kpe_table")
        if sum(self.kpe_weight_1) != 100 or sum(self.kpe_weight_2) != 100 or sum(self.kpe_weight_3) != 100 or sum(self.kpe_weight_4) != 100:
            print("Sum of kpe_weight arrays is not equal to 100")
        else:
            # Clear the arrays if all records are successfully inserted
            self.kpe_weight_1.clear()
            self.kpe_weight_2.clear()
            self.kpe_weight_3.clear()
            self.kpe_weight_4.clear()

    # TODO: This is a insert function for add new data to planned table
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
                formatted_date = date.strftime("%d%m%Y")
                # print(formatted_date)
                # *FOR USER DATA INFORMATION
                cursor = connection.cursor()
                cursor.execute(
                    f"SELECT specialist_id FROM specialists WHERE full_name='{str(self.specialist_menu_box.content.value)}';")
                user_id = cursor.fetchone()[0]

                # *FOR AUTO ID INCRIPTION
                cursor = connection.cursor()
                cursor.execute(f"SELECT max(plan_id) FROM planned_value;")
                max_id = cursor.fetchone()[0]
                # print(f"{user_id}-{formatted_date}-{max_id}")
                # *FOR INDICATORS
                selected_indicator = self.cb_menu_spec.content.value
                cursor = connection.cursor()
                selected_indicator_without_dots = selected_indicator.replace(".", "")
                cursor.execute(
                    f"SELECT indicators_id FROM name_of_indicators WHERE name LIKE '{selected_indicator_without_dots}%'")
                indicator_id = cursor.fetchone()[0]
                # *FRO PLAN_INDICATOR
                cursor = connection.cursor()
                cursor.execute(f"SELECT plan_indicators_id FROM planned_value")
                plan_indicator_id = cursor.fetchone()
                # *FOR UNITS
                # selected_unit = self.units_menu_box.content.value
                cursor = connection.cursor()
                # cursor.execute(f"SELECT measurement_id FROM name_of_indicators WHERE name LIKE '{selected_indicator}%'")
                cursor.execute(
                    f"SELECT measurement_id FROM name_of_indicators WHERE name LIKE '{selected_indicator_without_dots}%'")
                units_id = cursor.fetchone()[0]

                # Определите максимальное значение номера версии для данного показателя
                # Determine the maximum version for the current indicator and user combination
                cursor.execute(
                    f"SELECT MAX(number_of_version) FROM planned_value WHERE plan_indicators_id = {int(indicator_id)} AND plan_user_id = {int(user_id)}")
                max_version = cursor.fetchone()[0]

                # Check if max_version has the expected format (3 hyphen-separated parts)
                if max_version and len(max_version.split('-')) >= 3:
                    current_version = int(max_version.split('-')[2])
                else:
                    current_version = 0  # Start with version 1 if the format is unexpected or max_version is None

                number_of_verison_plus = f"{1}-{formatted_date}-{current_version + 1}"
                
                self.kpe_weight_1.append(int(self.weight_first_qr_box.content.value))
                self.kpe_weight_2.append(int(self.weight_second_qr_box.content.value))
                self.kpe_weight_3.append(int(self.weight_third_qr_box.content.value))
                self.kpe_weight_4.append(int(self.weight_fourth_qr_box.content.value))

                query = """
                    INSERT INTO planned_value (plan_id, plan_indicators_id, plan_user_id, plan_units_id, 1st_quater_value, 2nd_quater_value, 3rd_quater_value, 4th_quater_value, year, status, KPE_weight_1, KPE_weight_2, KPE_weight_3, KPE_weight_4, number_of_version)
                    VALUES ({}+1, {}, {}, {}, {}, {}, {}, {}, {},'{}', {}, {}, {}, {},'{}');
                """.format(
                        int(max_id),
                        int(indicator_id),
                        int(user_id),
                        int(units_id),
                        int(self.first_qr_box.content.value),
                        int(self.second_qr_box.content.value),
                        int(self.third_qr_box.content.value),
                        int(self.fourtht_qr_box.content.value),
                        int(self.year_box.content.value),
                        "Активно",
                        int(self.weight_first_qr_box.content.value),
                        int(self.weight_second_qr_box.content.value),
                        int(self.weight_third_qr_box.content.value),
                        int(self.weight_fourth_qr_box.content.value),
                        str(number_of_verison_plus),
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
                # self.cb_menu_spec.content.option = self.dropdown_options_indicators
                self.units_menu_box.content.value = ""
                # self.specialist_menu_box.content.value = ""
                print("Запись успешно добавлена в базу данных")
                print(self.kpe_weight_1)
                print(self.kpe_weight_2)
                print(self.kpe_weight_3)
                print(self.kpe_weight_4)
                

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
            user_id = cursor.fetchone()[0]

            query_select = "SELECT MAX(number_of_version) FROM planned_value WHERE plan_user_id = '{}';".format(user_id)
            cursor.execute(query_select)
            latest_version = cursor.fetchone()[0]

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
            WHERE pn.plan_user_id = {user_id} AND pn.number_of_version = '{latest_version}' AND pn.status = 'Активно'
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
                self.kpe_weight_1[int(plan_id)-1] = int(self.first_qr_box_2.content.value)
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
                self.kpe_weight_1[int(selected_row[0])-1] = int(self.weight_first_qr_box_2.content.value)
                self.page.dialog = self.alter_dialog_edit
                self.alter_dialog_edit.open = False

            if self.weight_second_qr_box.content.value != selected_row[9]:
                query_weight_second_qr = "ALTER TABLE planned_value UPDATE KPE_weight_2 = {} WHERE plan_id = {};".format(self.weight_second_qr_box_2.content.value, plan_id)
                cursor.execute(query_weight_second_qr)
                self.kpe_weight_2[int(selected_row[0])-1] = int(self.weight_second_qr_box_2.content.value)
                self.page.dialog = self.alter_dialog_edit
                self.alter_dialog_edit.open = False

            if self.weight_third_qr_box.content.value != selected_row[10]:
                query_weight_third_qr = "ALTER TABLE planned_value UPDATE KPE_weight_3 = {} WHERE plan_id = {};".format(self.weight_third_qr_box_2.content.value, plan_id)
                cursor.execute(query_weight_third_qr)
                self.kpe_weight_3[int(selected_row[0])-1] = int(self.weight_third_qr_box_2.content.value)
                self.page.dialog = self.alter_dialog_edit
                self.alter_dialog_edit.open = False

            if self.weight_fourth_qr_box.content.value != selected_row[11]:
                query_weight_fourth_qr = "ALTER TABLE planned_value UPDATE KPE_weight_4 = {} WHERE plan_id = {};".format(self.weight_fourth_qr_box_2.content.value, plan_id)
                cursor.execute(query_weight_fourth_qr)
                self.kpe_weight_4[int(selected_row[0])-1] = int(self.weight_fourth_qr_box_2.content.value)
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
        #     self.show_block_dialog("При измение данных произошла ошибка", "Ошибка")

    def close_edit_dialog(self, e):
        self.page.dialog = self.alter_dialog_edit
        self.alter_dialog_edit.open = False
        self.page.update()

    def delete_preview_data(self, e):
        cursor = connection.cursor()
        for selected_row in self.selected_rows:
            cursor.execute(f"SELECT specialist_id FROM specialists WHERE full_name='{str(self.specialist_menu_box.content.value)}';")
            user_id = cursor.fetchone()[0]
            indicator = f"SELECT indicators_id FROM name_of_indicators WHERE name LIKE '{selected_row[1]}'"
            # print(indicator)
            cursor.execute(indicator)
            indicator_id = cursor.fetchone()[0]
            # print(indicator_id)
            sql_select = "SELECT plan_id FROM planned_value WHERE plan_user_id = {} AND plan_indicators_id = {} AND 1st_quater_value = {} AND 2nd_quater_value = {} AND 3rd_quater_value = {} AND 4th_quater_value = {} AND year = {} AND KPE_weight_1 = {} AND KPE_weight_2 = {} AND KPE_weight_3 = {} AND KPE_weight_4 = {};".format(
                user_id, indicator_id, selected_row[3], selected_row[4], selected_row[5], selected_row[6], selected_row[7], selected_row[8], selected_row[9], selected_row[10], selected_row[11])
            cursor.execute(sql_select)
            kpe_id = cursor.fetchone()[0]
            print(kpe_id)
            query_status = "ALTER TABLE planned_value UPDATE status = 'Неактивно' WHERE plan_id = {};".format(kpe_id)
            cursor.execute(query_status)
        self.page.dialog = self.alter_dialog_preview
        self.alter_dialog_preview.open = False
        self.show_block_dialog("Запись была успешно удалена", "Успешно")
        self.page.update()