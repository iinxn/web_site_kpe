import datetime
import re
from flet import *
from service.connection import *
from utils.consts import primary_colors


class Actual(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.theme_mode = ThemeMode.LIGHT
        self.alignment = alignment.center
        self.expand = True
        self.bgcolor = primary_colors['GREEN']
        self.user_id = self.page.session.get('user_id')

        self.use_truncated_options = True
        self.dropdown_options_indicators = []
        self.dropdown_options_specialists = []
        dropdown_options_departments = []
        
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT name FROM name_of_department ORDER BY department_id')
            results = cursor.fetchall()

            for row in results:
                dropdown_options_departments.append(dropdown.Option(row[0]))

        except Exception as e:
            print(f"Error fetching data from the database: {str(e)}")
        # *BOX FOR DROPDOWN MENU
        self.cb_menu_spec = Container(
            content=Dropdown(
                label='Выберите наименование показателя',
                # max_width=200,
                width=400,
                color=primary_colors['BLACK'],
                options=self.dropdown_options_indicators,
                on_change=self.update_plan_values,
            ),
        )
        self.cb_quter_menu = Container(
            content=Dropdown(
                label='Выберите номер квартала',
                color=primary_colors['BLACK'],
                options=[
                    dropdown.Option('1-й квартал'),
                    dropdown.Option('2-й квартал'),
                    dropdown.Option('3-й квартал'),
                    dropdown.Option('4-й квартал')
                ],
            ),
        )
        self.cb_specialist_menu = Container(
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
                width=500,
                options=dropdown_options_departments,
                on_change=self.show_specialists
            ),
        )
        # *TEXTFIELD AREA
        self.plan_value_box = Container(
            content=TextField(
                hint_style=TextStyle(
                    size=12, color=primary_colors['MANATEE']
                ),
                label='Значение показателя',
                cursor_color=primary_colors['MANATEE'],
                text_style=TextStyle(
                    size=14,
                    color=primary_colors['GREEN'],
                ),
                # content_padding=30,
            ),
        )
        self.plan_weight_value_box = Container(
            content=TextField(
                hint_style=TextStyle(
                    size=12, color=primary_colors['MANATEE']
                ),
                label='Вес КПЭ',
                cursor_color=primary_colors['MANATEE'],
                text_style=TextStyle(
                    size=14,
                    color=primary_colors['GREEN'],
                ),
                # content_padding=30,
            ),
        )
        self.textfiled_input_actual_value = Container(
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
                # content_padding=30,
            ),
        )
        self.search_input = Container(
            content=TextField(
                label='Поиск показателя по наименованию',
                hint_style=TextStyle(size=12, color=primary_colors['MANATEE']),
                cursor_color=primary_colors['MANATEE'],
                text_style=TextStyle(size=14, color=primary_colors['GREEN']),
                on_change=self.filter_dropdown_options,
                width=400,
            ),
        )

        self.alter_dialog_block = AlertDialog(
            modal=True,
            title=Text("Default Title"),
            content=Text("Default Content"),
            actions=[TextButton("OK", on_click=self.close_dlg_block)],
            on_dismiss=lambda e: print("Modal dialog dismissed!")
        )

        # *header
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
                                                value='Ввести результат исполнения мероприятий КПЭ',
                                                size=18,
                                                color='white',
                                                text_align='center',
                                            ),
                                        ),
                                        Container(
                                            width=200,
                                            height=70,
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
                        # alignment='center',
                        # horizontal_alignment='center',
                        controls=[
                            # *1ST ROW
                            Container(height=30),
                            Container(
                                Row(
                                    spacing='50',
                                    alignment='center',
                                    # horizontal_alignment='center',
                                    controls=[
                                        Container(width=340),
                                        self.search_input,
                                        Container(width=200)
                                    ]
                                )
                            ),
                            Container(height=30),
                            Container(
                                Row(
                                    alignment='center',
                                    spacing='40',
                                    controls=[
                                        self.name_of_department_menu_box,
                                        self.cb_specialist_menu,
                                        self.cb_quter_menu,
                                        self.cb_menu_spec,
                                    ]
                                )
                            ),
                            Container(height=30),
                            # *2ND ROW
                            Container(
                                Row(
                                    spacing='50',
                                    alignment='center',
                                    controls=[
                                        Text(
                                            value='Плановые значения',
                                            size=16,
                                            color=primary_colors['GREEN'],
                                            text_align='center',
                                            weight='bold',
                                            width=120
                                        ),

                                        # dropdown 1st row
                                        # *VALUE OF INDICATORS
                                        self.plan_value_box,
                                        # *KPE WEIGHT
                                        self.plan_weight_value_box,
                                    ]
                                )
                            ),

                            Container(height=30),
                            # *3RD ROW
                            Container(
                                Row(
                                    spacing='50',
                                    alignment='center',
                                    controls=[
                                        Text(
                                            value='Введите факт',
                                            size=16,
                                            color=primary_colors['GREEN'],
                                            text_align='center',
                                            weight='bold',
                                        ),
                                        # *INPUT TEXTFIELD
                                        self.textfiled_input_actual_value,
                                    ]
                                )
                            ),
                            Container(height=30),
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
                                            on_click=self.insert_data_to_actual_table
                                        ),
                                    ]
                                )
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
            sql_select_specialist_id = f"SELECT specialist_id FROM specialists WHERE full_name = '{self.cb_specialist_menu.content.value}'"
            cursor.execute(sql_select_specialist_id)
            specialist_id = cursor.fetchone()[0]

            cursor.execute(f'SELECT indicators_id, name FROM name_of_indicators WHERE specialist_id = {specialist_id} ORDER BY indicators_id')
            results = cursor.fetchall()

            for indicator_id, name in results:
                self.dropdown_options_indicators.append(dropdown.Option(indicator_id, name))

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
        print("It's closed successfully")
        self.page.update()

    def insert_data_to_actual_table(self, e):
        try:
            cursor = connection.cursor()
            date = datetime.datetime.now()
            formatted_date = date.strftime("%Y%m%d")

            cursor.execute(
                f"SELECT specialist_id FROM specialists WHERE full_name='{str(self.cb_specialist_menu.content.value)}';")
            specialist_id = cursor.fetchone()[0]
            # *FOR AUTO ID INCRIPTION
            cursor.execute(f"SELECT max(actual_id) FROM actual_value;")
            max_id = cursor.fetchone()[0]
            indicator_id = self.cb_menu_spec.content.value
            cursor.execute(
                    f"""
                    SELECT 
                        concat(
                            toString(actual_specialist_id), '-',
                            substring(replace(toString(date), '-', ''), 7, 2),
                            substring(replace(toString(date), '-', ''), 5, 2),
                            substring(replace(toString(date), '-', ''), 1, 4),
                            '-', toString(number)
                        ) AS number_of_version
                    FROM actual_value
                    WHERE 
                        actual_specialist_id = {int(specialist_id)} AND 
                        actual_indicators_id = {int(self.cb_menu_spec.content.value)} AND
                        date = (
                            SELECT MAX(date)
                            FROM actual_value
                            WHERE actual_specialist_id = {int(specialist_id)} AND actual_indicators_id = {int(self.cb_menu_spec.content.value)}
                        ) AND 
                        number = (
                            SELECT MAX(number)
                            FROM actual_value
                            WHERE 
                                actual_specialist_id = {int(specialist_id)} AND 
                                actual_indicators_id = {int(self.cb_menu_spec.content.value)} AND
                                date = (
                                    SELECT MAX(date)
                                    FROM actual_value
                                    WHERE actual_specialist_id = {int(specialist_id)} AND actual_indicators_id = {int(self.cb_menu_spec.content.value)}
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
            INSERT INTO actual_value (
                actual_id,
                actual_indicators_id,
                actual_specialist_id,
                quarter_number,
                value,
                actual_user_id,
                date,
                number
            )
            VALUES ({}, {}, {}, '{}', {}, {}, '{}', {});
        """.format(
                int(max_id) + 1,
                int(indicator_id),
                int(specialist_id),
                str(self.cb_quter_menu.content.value),
                float(self.textfiled_input_actual_value.content.value),
                int(self.user_id),
                str(formatted_date),
                int(current_version)
            )
            cursor.execute(query)
            connection.commit()
            self.show_block_dialog("Запись успешно добавлена в базу данных", "Успешно")
            print("Запись успешно добавлена в базу данных")
            self.cb_menu_spec.content.value = ''
            # self.cb_quter_menu.content.value = ''
            self.plan_value_box.content.value = ''
            self.plan_weight_value_box.content.value = ''
            self.textfiled_input_actual_value.content.value = ''
            self.page.update()

        except Exception as e:
            self.show_block_dialog("Ошибка при добавлении записи в базу данных","Ошибка")
            print(f"Ошибка при добавлении записи в базу данных: {str(e)}")

    def update_plan_values(self, e):
        try:
            cursor = connection.cursor()
            # Получение specialist_id на основе выбранного специалиста
            cursor.execute(
                f"SELECT specialist_id FROM specialists WHERE full_name='{self.cb_specialist_menu.content.value}';")
            specialist_id = cursor.fetchone()[0]

            indicator_id = int(self.cb_menu_spec.content.value)

            # Получение максимальных date и number
            cursor.execute(
                f"""
                SELECT MAX(date), MAX(number)
                FROM kpe_table
                WHERE kpe_indicators_id = {indicator_id} AND kpe_specialist_id = {specialist_id}
                """
            )
            max_date, max_number = cursor.fetchone()

            quarter_mapping = {
                "1-й квартал": ("1st_quater_value", "KPE_weight_1"),
                "2-й квартал": ("2nd_quater_value", "KPE_weight_2"),
                "3-й квартал": ("3rd_quater_value", "KPE_weight_3"),
                "4-й квартал": ("4th_quater_value", "KPE_weight_4")
            }
            quarter_column, weight_column = quarter_mapping[self.cb_quter_menu.content.value]

            cursor.execute(
                f"""
                SELECT {quarter_column}, {weight_column}
                FROM kpe_table
                WHERE kpe_indicators_id = {indicator_id}
                AND kpe_specialist_id = {specialist_id}
                AND date = '{max_date}'
                AND number = {max_number}
                """
            )

            result = cursor.fetchone()

            if result:
                self.plan_value_box.content.value = str(result[0])
                self.plan_weight_value_box.content.value = str(result[1])
                self.page.update()
            else:
                self.show_block_dialog("Запись не найдена в базе данных", "Не найдено")
                print("Запись не найдена в базе данных")
                self.page.update()

        except Exception as e:
            self.show_block_dialog("Ошибка при добавлении записи в базу данных", "Ошибка")
            print(f"Ошибка при добавлении записи в базу данных: {str(e)}")


    def filter_dropdown_options(self, e):
        search_text = self.search_input.content.value.lower()
        filtered_options = []

        if self.dropdown_options_indicators is not None:
            for option in self.dropdown_options_indicators:
                # Проверка, что опция не None и что у опции есть текст
                if option is not None and getattr(option, 'text', None) is not None:
                    # Применяем фильтрацию к текстовому свойству опции
                    if search_text in option.text.lower():
                        filtered_options.append(option)
        else:
            print("Dropdown options are None")

        # Если строка поиска пуста, возвращаем все опции
        if not search_text:
            filtered_options = self.dropdown_options_indicators

        print("Search Text:", search_text)  # Отладочное сообщение
        print("Filtered options:", [option.text for option in filtered_options])  # Отладочное сообщение

        # Обновляем опции в выпадающем списке
        self.cb_menu_spec.content.options = filtered_options
        self.page.update()