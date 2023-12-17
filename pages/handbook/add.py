from flet import *
from utils.colors import * 
from service.connection import *

class Add(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page  # Initialize the self.page object
        self.page.theme_mode = ThemeMode.LIGHT  # Set the theme mode
        self.alignment = alignment.center
        self.expand = True
        self.bgcolor = tea_green
        
        self.selected_rows = set()

        # Creating the DataTable
        self.data_table = DataTable(
            columns=[
                DataColumn(Text("""
                                Код
                                показателя"""), numeric=True),
                DataColumn(Text("""
                                Код
                                ед. из."""), numeric=True),
                DataColumn(Text("Наименование")),
                DataColumn(Text("Редактирование")),
            ],
            rows=[],  # Leave this empty for now
            border=border.all(1, "black"),
            vertical_lines=border.BorderSide(1, "black"),
            horizontal_lines=border.BorderSide(1, "black"),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=colors.BLACK12,
            heading_row_height=100,
            width=2000
        )
        
        dropdown_options_units_1 = []
        dropdown_options_units_2 = []
        
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT type FROM units_of_measurement ORDER BY measurement_id')
            results = cursor.fetchall()

            for row in results:
                dropdown_options_units_1.append(dropdown.Option(row[0]))
                dropdown_options_units_2.append(dropdown.Option(row[0]))
        except Exception as e:
            print(f"Error fetching data from the database: {str(e)}")
#*TEXTFIELD
        self.add_textfield_box = Container(
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
          )
        )
        self.alter_dialog_error = AlertDialog(
            modal=True,
            title=Text("Default Title"),
            content=Text("Default Content"),
            actions=[TextButton("OK", on_click=self.close_dlg_error)],
            on_dismiss=lambda e: print("Modal dialog dismissed!")
        )
        self.cb_units = Container(
          content=Dropdown(
                hint_text='Выберите измерения',
                color="black",
                width=300,
                options=dropdown_options_units_1,  # Set the options from the fetched data
            ),
        )
        self.dp_units = Container(
          content=Dropdown(
                hint_text='Выберите измерения',
                color="black",
                width=300,
                options=dropdown_options_units_2,  # Set the options from the fetched data
            ),
        )
        
        self.edit_name = Container(
          content=TextField(
                    hint_style=TextStyle(
                        size=12, color='#858796'
                    ),
                    label='Введите другое название',
                    cursor_color='#858796',
                    text_style=TextStyle(
                        size=14,
                        color='#5B7553',
                    ),
                        ),
        )
        self.alter_dialog_add_new_specialists = AlertDialog(
            modal=True,
            title=Text("Изменить строку"),
            content=Column(
              height=250,
              width=500,
              controls=[
                self.dp_units,
                self.edit_name,
              ]
            ),
            actions=[
                TextButton("Изменить", on_click=self.edit_name_in_table),
                TextButton("Закрыть", on_click=self.close_edit_dialog),
            ],
            actions_alignment=MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

#*HEADER
        self.content = Column(
            spacing=0,
            controls=[
                Container(
                    width=8000,
                    padding=40,
                    bgcolor='#5B7553',
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
                                    value='Добавление показателя в справочник',
                                    size=18,
                                    color='white',
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
                
#*MANUAL BUTTONS
                Container(
                    expand=True,
                    bgcolor='white',
                    content=Column(
                      expand=True,
                      # alignment='center',
                      horizontal_alignment='center',
                      controls=[
#*1ST ROW
                          Container(height=50),
                          Container(
                            Row(
                              spacing='50',
                              alignment='center',
                              controls=[
                                  Container(width=90),
                                  self.add_textfield_box,
                                  self.cb_units,
                                  ElevatedButton(
                                            color=white,
                                            bgcolor='#5B7553',
                                            width=300,
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
                                            on_click=self.insert_into_db,
                                        ),
                                        ElevatedButton(
                                            color=white,
                                            bgcolor='#5B7553',
                                            width=300,
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
                                            # on_click=lambda e: self.output_selected_rows(),
                                            on_click=lambda e: self.show_edit_dialog(),
                                        )
                              ]
                            )
                          ), 
                          
                          # Container(height=50),
#*2ND ROW (DATATABLE)
                          Container(
                            content=self.data_table,
                            alignment=alignment.center,
                            padding=padding.all(20),
                          ),
                          Container(height=50),
                          #4th row
                          
                      ],
                  )
                ),
            ]
        )
#*DB CONNECTIONS WITH SELECT QUERY
        cursor = connection.cursor()
        query_select = '''
        SELECT
            ni.indicators_id,
            um.type,
            ni.name,
        FROM name_of_indicators AS ni
        JOIN units_of_measurement AS um ON ni.measurement_id = um.measurement_id
        ORDER BY ni.indicators_id;
        '''

        cursor.execute(query_select)
        results = cursor.fetchall()

        for row in results:
            cells = [DataCell(Text(str(value))) for value in row]
            checkbox = Checkbox(value=False, on_change=lambda e, row=row: self.toggle_row_selection(e, row))
            cells.append(DataCell(checkbox))
            data_row = DataRow(cells=cells)
            self.data_table.rows.append(data_row)
        self.content.controls[1].content.controls[2] = self.data_table

    def toggle_row_selection(self, e, row):
        # Toggle the row's selection when the Checkbox value changes
        if row not in self.selected_rows:
            self.selected_rows.add(row)
        else:
            self.selected_rows.remove(row)
    
    
    def show_edit_dialog(self):
        if not self.selected_rows:
            self.show_error_dialog("Вы не выбрали строку в таблице")
        else:
            selected_row = next(iter(self.selected_rows))
            selected_data = selected_row[2]
            self.edit_name.content.value = selected_data
            self.dp_units.content.value = selected_row[1]
            self.page.dialog = self.alter_dialog_add_new_specialists
            self.alter_dialog_add_new_specialists.open = True
            self.page.update()


    def edit_name_in_table(self, e):
        selected_row = next(iter(self.selected_rows))

        cursor = connection.cursor()
        self.dp_units.content.value
        cursor.execute(f"SELECT measurement_id FROM units_of_measurement WHERE type = '{self.dp_units.content.value}'")
        units_id = cursor.fetchone()[0]
        print(units_id)
        # Use the UPDATE statement to modify the record
        query_name = "ALTER TABLE name_of_indicators UPDATE name = '{}' WHERE indicators_id = {}".format(self.edit_name.content.value, selected_row[0])
        query_units = "ALTER TABLE name_of_indicators UPDATE measurement_id = {} WHERE indicators_id = {}".format(int(units_id), selected_row[0])
        print(query_name)
        print(query_units)
        print(selected_row[0])
        cursor.execute(query_name)
        cursor.execute(query_units)

        # Fetch the updated data from the database
        query_select = '''
        SELECT
            ni.indicators_id,
            um.type,
            ni.name,
        FROM name_of_indicators AS ni
        JOIN units_of_measurement AS um ON ni.measurement_id = um.measurement_id
        ORDER BY ni.indicators_id;
        '''
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

    def show_error_dialog(self,text):
        self.page.dialog = self.alter_dialog_error
        self.alter_dialog_error.title = Text(value="Ошибка", color="black")
        self.alter_dialog_error.content = Text(value=text, color="black")
        self.alter_dialog_error.open = True
        self.page.update() 
    def close_dlg_error(self, e):
        self.page.dialog = self.alter_dialog_error
        self.alter_dialog_error.open = False
        print("It's closed successfully")
        self.page.update()
    
    def insert_into_db(self, e):
      selected_unit = self.cb_units.content.value
      
      if self.add_textfield_box.content.value == "" or selected_unit == "":
        self.show_error_dialog("Вы не заполнили все поля")
      else:
        try:
          cursor = connection.cursor()
          cursor.execute(f"SELECT measurement_id FROM units_of_measurement WHERE type = '{selected_unit}'")
          units_id = cursor.fetchone()[0]
          
          cursor.execute(f"SELECT max(indicators_id) FROM name_of_indicators;")
          max_id = cursor.fetchone()[0]
          query = "INSERT INTO TABLE name_of_indicators (indicators_id, measurement_id, name) VALUES ({}+1,{},'{}')".format(int(max_id), units_id, self.add_textfield_box.content.value)
          cursor.execute(query)
          print("Запись успешно добавлена в базу данных")
          query_select = '''
          SELECT
              ni.indicators_id,
              um.type,
              ni.name,
          FROM name_of_indicators AS ni
          JOIN units_of_measurement AS um ON ni.measurement_id = um.measurement_id
          ORDER BY ni.indicators_id;
          '''
          cursor.execute(query_select)
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
          self.add_textfield_box.content.value = ""
          self.page.update()

        except Exception as e:
            print(f"Ошибка при добавлении записи в базу данных: {str(e)}")
