from flet import *
from utils.colors import * 
from service.connection import *

class SpecialistsHandbook(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.theme_mode = ThemeMode.LIGHT
        self.alignment = alignment.center
        self.expand = True
        self.bgcolor = tea_green
        
        self.selected_rows = set()

        # Creating the DataTable
        self.data_table = DataTable(
            columns=[
                DataColumn(Text("Код специалиста"), numeric=True),
                DataColumn(Text("Код управления"), numeric=True),
                DataColumn(Text("ФИО")),
                DataColumn(Text("Должность")),
                DataColumn(Text("Статус")),
                DataColumn(Text("Пользователь")),
                DataColumn(Text("Редактировать")),
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

        dropdown_options_department = []

        try:
            cursor = connection.cursor()
            cursor.execute('SELECT name FROM name_of_department')
            results = cursor.fetchall()

            for row in results:
                dropdown_options_department.append(dropdown.Option(row[0]))
        except Exception as e:
            print(f"Error fetching data from the database: {str(e)}")

#*BOX FOR TEXTFIELD
        self.specialist_new_full_name = Container(
          content=TextField(
                  label="Введите ФИО специалиста",
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
        self.specialist_new_position = Container(
          content=TextField(
                  label="Введите должность специалиста",
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
#*DROPDOWNS
        self.cb_menu_department = Container(
            content=Dropdown(
                hint_text='Выберите управление',
                color="black",
                width=400,
                options=dropdown_options_department,
            ),
        )
        self.cb_menu_status = Container(
          content=Dropdown(
                hint_text='Выберите статус',
                color="black",
                width=400,
                options=[
                  dropdown.Option("Активный"),
                  dropdown.Option("Неактивный")
                ],
            ),
        )

#*ALTERDIALOGS
        self.alter_dialog_add_new_specialists = AlertDialog(
            modal=True,
            title=Text("Добавление специалиста в справочник"),
            content=Column(
              height=250,
              controls=[
                self.cb_menu_department,
                self.specialist_new_full_name,
                self.specialist_new_position,
                self.cb_menu_status,
              ]
            ),
            actions=[
                TextButton("Добавить", on_click=self.add_new_specialist),
                TextButton("Закрыть", on_click=self.close_dlg),
            ],
            actions_alignment=MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.edit_name = Container(
          content=Dropdown(
                hint_text='Изменить состояние',
                color="black",
                width=400,
                options=[
                  dropdown.Option("Является"),
                  dropdown.Option("Не является")
                ],
            ),
        )
        self.alter_dialog_edit = AlertDialog(
            modal=True,
            title=Text("Изменить строку"),  
            content=Column(
              height=300,
              width=500,
              controls=[
                self.cb_menu_department,
                self.specialist_new_full_name,
                self.specialist_new_position,
                self.cb_menu_status,
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
                                                value='Добавить специалиста в справочник',
                                                size=18,
                                                color='white',
                                                text_align='center',
                                            ),
                                        ),
                                        Container(
                                          width=300,
                                          content=Row(
                                            controls=[
                                              Container(
                                                content=ElevatedButton(
                                                  color=white,
                                                  bgcolor='white',
                                                  width=150,
                                                  height=70,
                                                  content=Column(
                                                    horizontal_alignment='center',
                                                    alignment='center',
                                                      controls=[
                                                        Container(
                                                          
                                                          Text(
                                                            value='Добавить специалиста',
                                                            size=16,
                                                            color='#5B7553',
                                                            text_align='center',
                                                            weight='bold',
                                                          )
                                                        )
                                                      ]
                                                  ),
                                                  on_click=self.show_alter_dialog
                                                ),  
                                              ),
                                              Container(
                                                content=ElevatedButton(
                                                  color=white,
                                                  bgcolor='white',
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
                                                            color='#5B7553',
                                                            text_align='center',
                                                            weight='bold',
                                                          )
                                                        )
                                                      ]
                                                  ),
                                                  on_click=lambda e: self.show_edit_dialog(),
                                                ),  
                                              ),
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
                            Container(),
                            Container(),

  # *2ND ROW (DATATABLE)
                            Container(
                                content=self.data_table,
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
        query_select = '''
        SELECT
            sc.specialist_id,
            nd.name,
            sc.full_name,
            sc.position,
            sc.status,
            sc.is_user
        FROM specialists AS sc
        JOIN name_of_department AS nd ON sc.specialist_department_id = nd.department_id
        ORDER BY sc.specialist_id;
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

    def show_alter_dialog(self, e):
      self.page.dialog = self.alter_dialog_add_new_specialists
      self.page.dialog.open = True
      self.page.update()
    def close_dlg(self, e):
        self.page.dialog = self.alter_dialog_add_new_specialists
        self.page.dialog.open = False
        self.page.update()      

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
            self.cb_menu_department.content.value = selected_row[1]
            self.specialist_new_full_name.content.value = selected_row[2]
            self.specialist_new_position.content.value = selected_row[3]
            self.cb_menu_status.content.value = selected_row[4]
            self.edit_name.content.value = selected_row[5]
            # self.dp_units.content.value = selected_row[1]
            self.page.dialog = self.alter_dialog_edit
            self.alter_dialog_edit.open = True
            self.page.update()


    def edit_name_in_table(self, e):
        selected_row = next(iter(self.selected_rows))

        cursor = connection.cursor()
        sql_select = "SELECT department_id FROM name_of_department WHERE name = '{}'".format(self.cb_menu_department.content.value)
        cursor.execute(sql_select)
        department_id = cursor.fetchone()[0]
        # Use the UPDATE statement to modify the record
        query_department = "ALTER TABLE specialists UPDATE specialist_department_id = {} WHERE specialist_id = {}".format(department_id, selected_row[0])
        query_full_name = "ALTER TABLE specialists UPDATE full_name = '{}' WHERE specialist_id = {}".format(self.specialist_new_full_name.content.value, selected_row[0])
        query_position = "ALTER TABLE specialists UPDATE position = '{}' WHERE specialist_id = {}".format(self.specialist_new_position.content.value, selected_row[0])
        query_status = "ALTER TABLE specialists UPDATE status = '{}' WHERE specialist_id = {}".format(self.cb_menu_status.content.value, selected_row[0])
        query_is_user = "ALTER TABLE specialists UPDATE is_user = '{}' WHERE specialist_id = {}".format(self.edit_name.content.value, selected_row[0])
        cursor.execute(query_department)
        cursor.execute(query_full_name)
        cursor.execute(query_position)
        cursor.execute(query_status)
        cursor.execute(query_is_user)

        # Fetch the updated data from the database
        query_select = '''
        SELECT
            sc.specialist_id,
            nd.name,
            sc.full_name,
            sc.position,
            sc.status,
            sc.is_user
        FROM specialists AS sc
        JOIN name_of_department AS nd ON sc.specialist_department_id = nd.department_id
        ORDER BY sc.specialist_id;
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
        self.page.dialog = self.alter_dialog_edit
        self.alter_dialog_edit.open = False
        self.page.update()

    
    def close_edit_dialog(self, e):
        self.page.dialog = self.alter_dialog_edit
        self.alter_dialog_edit.open = False
        self.page.update()

    def add_new_specialist(self, e):
      cursor = connection.cursor()
      
      quary_select_from_users = "SELECT full_name FROM users ORDER BY user_id"
      cursor.execute(quary_select_from_users)
      results_from_users = cursor.fetchall()
      full_names_from_users = [result[0] for result in results_from_users]
      typed_full_name = self.specialist_new_full_name.content.value
      if typed_full_name in full_names_from_users:
          print(f"{typed_full_name} является пользователем")
          is_user = "Является"
      else:
          print(f"{typed_full_name} не является пользователем")
          is_user = "Не является"

      
      if (self.specialist_new_full_name == "" or
          self.specialist_new_position == "" or
          self.cb_menu_department.content.value == "" or
          self.cb_menu_status == ""):
        print("Please")
      else:
        try:
          cursor = connection.cursor()
          
          sql_select = "SELECT department_id FROM name_of_department WHERE name = '{}'".format(self.cb_menu_department.content.value)
          cursor.execute(sql_select)
          department_id = cursor.fetchone()[0]
          
          cursor.execute(f"SELECT max(specialist_id) FROM specialists;")
          max_id = cursor.fetchone()[0]
          query = "INSERT INTO TABLE specialists (specialist_id, specialist_department_id, full_name, position, status, is_user) VALUES ({}+1,{},'{}','{}','{}','{}');".format(
            int(max_id),
            int(department_id),
            self.specialist_new_full_name.content.value,
            self.specialist_new_position.content.value,
            self.cb_menu_status.content.value,
            is_user
            )
          cursor.execute(query)
          print("Запись успешно добавлена в базу данных")
          self.alter_dialog_add_new_specialists.open = False
          self.page.update()
          
          query_select = '''
          SELECT
              sc.specialist_id,
              nd.name,
              sc.full_name,
              sc.position,
              sc.status,
              sc.is_user
          FROM specialists AS sc
          JOIN name_of_department AS nd ON sc.specialist_department_id = nd.department_id
          ORDER BY sc.specialist_id;
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
          self.page.update()
          self.specialist_new_full_name.content.value = ""
          self.specialist_new_position.content.value = ""
          self.cb_menu_department.content.value = ""
          self.cb_menu_status.content.value = ""

      
        except Exception as e:
          print(f"Ошибка при добавлении записи в базу данных: {str(e)}")
        self.page.update()

