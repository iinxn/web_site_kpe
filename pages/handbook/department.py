from flet import *
from utils.consts import primary_colors 
from service.connection import *
from utils.components import *

class Department(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.components_manager = Components(page)
        self.page.theme_mode = ThemeMode.LIGHT
        self.alignment = alignment.center
        self.expand = True
        self.bgcolor = primary_colors['WHITE']
        
        self.selected_rows = set()

        # Creating the DataTable
        self.data_table = DataTable(
            columns=[
                DataColumn(Text("Код управления"), numeric=True),
                DataColumn(Text("Наименование")),
                DataColumn(Text("Редактирование")),
            ],
            rows=[],
            border=border.all(1, primary_colors['BLACK']),
            vertical_lines=border.BorderSide(1, primary_colors['BLACK']),
            horizontal_lines=border.BorderSide(1, primary_colors['BLACK']),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=colors.BLACK12,
            heading_row_height=100,
            width=1000
        )
        
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
        
        self.edit_name = Container(
            content=TextField(
                    hint_style=TextStyle(
                        size=12, color=primary_colors['MANATEE']
                    ),
                    label='Введите другое название',
                    cursor_color=primary_colors['MANATEE'],
                    text_style=TextStyle(
                        size=14,
                        color=primary_colors['GREEN'],
                    ),
                        ),
        )
        self.alter_dialog_add_new_specialists = AlertDialog(
            modal=True,
            title=Text("Изменить строку"),
            content=Column(
            height=250,
            controls=[
                self.edit_name
            ]
            ),
            actions=[
                TextButton("Изменить", on_click=self.edit_name_in_table),
                TextButton("Закрыть", on_click=self.close_edit_dialog),
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
                                                value='Добавить управление в справочник',
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
                                    spacing='40',
                                    alignment='center',
                                    controls=[
                                        self.textfield_box,
                                        ElevatedButton(
                                            color=primary_colors['WHITE'],
                                            bgcolor=primary_colors['GREEN'],
                                            width=180,
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
                                            on_click=self.insert_into_db,
                                        ),
                                        ElevatedButton(
                                            color=primary_colors['WHITE'],
                                            bgcolor=primary_colors['GREEN'],
                                            width=180,
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
                                            on_click=self.show_edit_dialog,
                                        ),
                                        ElevatedButton(
                                            color=primary_colors['WHITE'],
                                            bgcolor=primary_colors['GREEN'],
                                            width=180,
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
                                            on_click=self.delete_department,
                                        ),
                                    ]
                                )
                            ),
  # *2ND ROW (DATATABLE)
                            Container(
                                self.data_table
                            ),
                            Container(height=50),
                        ],
                    )
                ),
            ]
        )
        self.show_department()

    def show_department(self):
        self.data_table.rows.clear()
        cursor = connection.cursor()
        query_select = 'SELECT * FROM name_of_department ORDER BY department_id'
        cursor.execute(query_select)
        results=cursor.fetchall()
        for row in results:
            cells = [DataCell(Text(str(value))) for value in row]
            checkbox = Checkbox(value=False, on_change=lambda e, row=row: self.toggle_row_selection(e, row))
            cells.append(DataCell(checkbox))
            data_row = DataRow(cells=cells)
            self.data_table.rows.append(data_row)
        self.content.controls[1].content.controls[2] = self.data_table
        self.page.update()

    def insert_into_db(self, e):
        if self.textfield_box.content.value == "":
            self.components_manager.show_block_dialog("Заполните поле перед внесением", "Ошибка")
        else:
            try:
                cursor = connection.cursor()
                cursor.execute(f"SELECT max(department_id) FROM name_of_department;")
                max_id = cursor.fetchone()[0]
                query = "INSERT INTO TABLE name_of_department (department_id, name) VALUES ({}+1,'{}')".format(int(max_id), self.textfield_box.content.value)
                cursor.execute(query)
                print("Запись успешно добавлена в базу данных")
                self.show_department()
                self.textfield_box.content.value = ""
                self.page.update()
            except Exception as e:
                print(f"Ошибка при добавлении записи в базу данных: {str(e)}")

    def toggle_row_selection(self, e, row):
        if row not in self.selected_rows:
            self.selected_rows.add(row)
        else:
            self.selected_rows.remove(row)

    def show_edit_dialog(self, e):
        if not self.selected_rows:
            self.components_manager.show_block_dialog("Вы не выбрали строку в таблице", "Ошибка")
        else:
            selected_row = next(iter(self.selected_rows))
            selected_data = selected_row[1]
            self.edit_name.content.value = selected_data
            self.page.dialog = self.alter_dialog_add_new_specialists
            self.alter_dialog_add_new_specialists.open = True
            self.page.update()

    def edit_name_in_table(self, e):
        selected_row = next(iter(self.selected_rows))
        cursor = connection.cursor()
        query = "ALTER TABLE name_of_department UPDATE name = '{}' WHERE department_id = {}".format(self.edit_name.content.value, selected_row[0])
        cursor.execute(query)
        self.page.dialog = self.alter_dialog_add_new_specialists
        self.alter_dialog_add_new_specialists.open = False
        self.selected_rows.clear()
        self.data_table.rows.clear()
        self.page.update()
        self.show_department()

    def close_edit_dialog(self, e):
        self.page.dialog = self.alter_dialog_add_new_specialists
        self.alter_dialog_add_new_specialists.open = False
        self.page.update()

    def delete_department(self, e):
        if not self.selected_rows:
            self.components_manager.show_block_dialog("Вы не выбрали строку в таблице", "Ошибка")
        else:
            cursor = connection.cursor()
            for selected_row in self.selected_rows:
                query_delete_department = f"DELETE FROM name_of_department WHERE department_id = {selected_row[0]}"
                cursor.execute(query_delete_department)
                connection.commit()
                print(query_delete_department)
            self.show_department()
            self.selected_rows.clear()
            self.components_manager.show_block_dialog("Запись удалена", "Успешно")
            self.page.update()