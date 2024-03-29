from flet import *
from utils.consts import primary_colors
from service.connection import *

class MeasurementHandbook(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.theme_mode = ThemeMode.LIGHT
        self.alignment = alignment.center
        self.expand = True
        self.bgcolor = primary_colors['WHITE']
        self.selected_rows = set()

        # Creating the DataTable
        self.data_table = DataTable(
            columns=[
                DataColumn(Text("Код единицы измерения"), numeric=True),
                DataColumn(Text("Наименование")),
                DataColumn(Text("Редактировать")),
            ],
            rows=[],
            border=border.all(1, primary_colors['BLACK']),
            vertical_lines=border.BorderSide(1, primary_colors['BLACK']),
            horizontal_lines=border.BorderSide(1, primary_colors['BLACK']),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=colors.BLACK12,
            heading_row_height=100,
            width=1000,
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
        self.alter_dialog_error = AlertDialog(
            modal=True,
            title=Text("Default Title"),
            content=Text("Default Content"),
            actions=[TextButton("OK", on_click=self.close_dlg_error)],
            on_dismiss=lambda e: print("Modal dialog dismissed!")
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
                                                value='Добавить единицы измерения в справочник',
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
                                    spacing='50',
                                    alignment='center',
                                    controls=[
                                        Container(width=90),
                                        self.textfield_box,
                                        ElevatedButton(
                                            color=primary_colors['WHITE'],
                                            bgcolor=primary_colors['GREEN'],
                                            width=200,
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
                                            width=200,
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
                                            # on_click=lambda e: self.output_selected_rows(),
                                            on_click=lambda e: self.show_edit_dialog(),
                                        )
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
        cursor = connection.cursor()
        query_select = 'SELECT * FROM units_of_measurement ORDER BY measurement_id'
        cursor.execute(query_select)
        results = cursor.fetchall()

        for row in results:
            # Create cells for the row
            cells = [DataCell(Text(str(value))) for value in row]

            # Create a Checkbox for row selection
            checkbox = Checkbox(value=False, on_change=lambda e, row=row: self.toggle_row_selection(e, row))
            cells.append(DataCell(checkbox))

            # Create the DataRow with cells
            data_row = DataRow(cells=cells)

            # Add the row to the DataTable
            self.data_table.rows.append(data_row)

        # Add the DataTable to the content
        self.content.controls[1].content.controls[2] = self.data_table
        
    def toggle_row_selection(self, e, row):
        # Toggle the row's selection when the Checkbox value changes
        if row not in self.selected_rows:
            self.selected_rows.add(row)
        else:
            self.selected_rows.remove(row)
    
    
    def show_edit_dialog(self):
        if not self.selected_rows:
            # If no rows are selected, show an error dialog
            self.show_error_dialog("Вы не выбрали строку в таблице")
        else:
            # Get the first selected row (you can adjust this logic if you want to handle multiple selected rows)
            selected_row = next(iter(self.selected_rows))
            # Assuming the selected data is in the second column of the DataTable, index 1
            selected_data = selected_row[1]

            # Set the value of the edit_name TextField
            self.edit_name.content.value = selected_data

            
            # Show the edit dialog
            self.page.dialog = self.alter_dialog_add_new_specialists
            self.alter_dialog_add_new_specialists.open = True
            self.page.update()


    def edit_name_in_table(self, e):
        selected_row = next(iter(self.selected_rows))

        cursor = connection.cursor()

        # Use the UPDATE statement to modify the record
        query = "ALTER TABLE units_of_measurement UPDATE type = '{}' WHERE measurement_id = {}".format(self.edit_name.content.value, selected_row[0])
        cursor.execute(query)

        # Fetch the updated data from the database

        query_select = 'SELECT * FROM units_of_measurement ORDER BY measurement_id'

        cursor.execute(query_select)
        results = cursor.fetchall()
        query_result = results
        data_rows = []

        for row in query_result:
            cells = [DataCell(Text(str(value))) for value in row]
            data_row = DataRow(cells=cells)
            checkbox_1 = Checkbox(value=False, on_change=lambda e, row=row: self.toggle_row_selection(e, row))
            cells.append(DataCell(checkbox_1))

            data_rows.append(data_row)

        # After you fetch new data from the database and create data_rows, update the DataTable like this:
        self.data_table.rows = data_rows
        self.selected_rows.clear()
        self.page.dialog = self.alter_dialog_add_new_specialists
        self.alter_dialog_add_new_specialists.open = False
        self.page.update()

    
    def close_edit_dialog(self, e):
        self.page.dialog = self.alter_dialog_add_new_specialists
        self.alter_dialog_add_new_specialists.open = False
        self.page.update()
    
    def show_error_dialog(self, text):
        self.page.dialog = self.alter_dialog_error
        self.alter_dialog_error.title = Text(value="Ошибка", color=primary_colors['BLACK'])
        self.alter_dialog_error.content = Text(value=text, color=primary_colors['BLACK'])
        self.alter_dialog_error.open = True
        self.page.update() 
    
    def close_dlg_error(self, e):
        self.page.dialog = self.alter_dialog_error
        self.alter_dialog_error.open = False
        print("It's closed successfully")
        self.page.update()
    
    def insert_into_db(self, e):
      if self.textfield_box.content.value == "":
        self.show_error_dialog("Заполните поле")
      else:
        try:
          cursor = connection.cursor()
          cursor.execute(f"SELECT max(measurement_id) FROM units_of_measurement;")
          max_id = cursor.fetchone()[0]
          query = "INSERT INTO TABLE units_of_measurement (measurement_id, type) VALUES ({}+1,'{}')".format(int(max_id), self.textfield_box.content.value)
          cursor.execute(query)
          print("Запись успешно добавлена в базу данных")

          cursor.execute('SELECT * FROM units_of_measurement ORDER BY measurement_id')
          results = cursor.fetchall()
          query_result = results
          data_rows = []

          for row in query_result:
            cells = [DataCell(Text(str(value))) for value in row]
            data_row = DataRow(cells=cells)

            # Create a Checkbox for the third column
            checkbox = Checkbox(value=False, on_change=lambda e, row=row: self.toggle_row_selection(e, row))
            cells.append(DataCell(checkbox))

            data_rows.append(data_row)
          # After you fetch new data from the database and create data_rows, update the DataTable like this:
          self.data_table.rows = data_rows
          self.textfield_box.content.value = ""
          self.page.update()

        except Exception as e:
            print(f"Ошибка при добавлении записи в базу данных: {str(e)}")
