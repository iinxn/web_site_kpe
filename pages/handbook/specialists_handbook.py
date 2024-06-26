from flet import *
from utils.consts import primary_colors
from utils.components import *
from service.connection import *

class SpecialistsHandbook(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.theme_mode = ThemeMode.LIGHT
        self.alignment = alignment.center
        self.components_manager = Components(page)
        self.expand = True
        self.bgcolor = primary_colors['WHITE']
        
        self.selected_rows = set()

        # Creating the DataTable
        self.data_table = DataTable(
            columns=[
                DataColumn(Text("Код специалиста"), numeric=True),
                DataColumn(Text("Наименование управления"), numeric=True),
                DataColumn(Text("ФИО")),
                DataColumn(Text("Должность")),
                DataColumn(Text("Статус")),
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
        self.specialist_new_position = Container(
          content=TextField(
                  label="Введите должность специалиста",
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
#*DROPDOWNS
        self.cb_menu_department = Container(
            content=Dropdown(
                hint_text='Выберите управление',
                color=primary_colors['BLACK'],
                width=400,
                options=dropdown_options_department,
            ),
        )
        self.cb_menu_status = Container(
          content=Dropdown(
                hint_text='Выберите статус',
                color=primary_colors['BLACK'],
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
                                                value='Добавить специалиста в справочник',
                                                size=18,
                                                color=primary_colors['WHITE'],
                                                text_align='center',
                                            ),
                                        ),
                                        Container(
                                          content=Row(
                                            controls=[
                                              ElevatedButton(
                                                color=primary_colors['WHITE'],
                                                bgcolor=primary_colors['WHITE'],
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
                                                          color=primary_colors['GREEN'],
                                                          text_align='center',
                                                          weight='bold',
                                                        )
                                                      )
                                                    ]
                                                ),
                                                on_click=self.show_alter_dialog
                                              ),  
                                              ElevatedButton(
                                                color=primary_colors['WHITE'],
                                                bgcolor=primary_colors['WHITE'],
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
                                                          color=primary_colors['GREEN'],
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
                                                bgcolor=primary_colors['WHITE'],
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
                                                          color=primary_colors['GREEN'],
                                                          text_align='center',
                                                          weight='bold',
                                                        )
                                                      )
                                                    ]
                                                ),
                                                on_click=self.delete_specialists,
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
                    bgcolor=primary_colors['WHITE'],
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
        self.show_specialists()

    def show_specialists(self):
      self.data_table.rows.clear()
      cursor = connection.cursor()
      query_select = '''
      SELECT
        sc.specialist_id,
        nd.name,
        sc.full_name,
        sc.position,
        sc.status
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
        checkbox = Checkbox(value=False, on_change=lambda e, row=row: self.toggle_row_selection(e, row))
        cells.append(DataCell(checkbox))
        data_rows.append(data_row)
      self.data_table.rows = data_rows

    def add_new_specialist(self, e):
      cursor = connection.cursor()
      if (self.specialist_new_full_name == "" or
        self.specialist_new_position == "" or
        self.cb_menu_department.content.value == "" or
        self.cb_menu_status == ""):
        self.components_manager.show_block_dialog("Вы не заполнили поля", "Ошибка")
      else:
        try:
          cursor = connection.cursor()
          sql_select = "SELECT department_id FROM name_of_department WHERE name = '{}'".format(self.cb_menu_department.content.value)
          cursor.execute(sql_select)
          department_id = cursor.fetchone()[0]
          cursor.execute(f"SELECT max(specialist_id) FROM specialists;")
          max_id = cursor.fetchone()[0]
          query = "INSERT INTO TABLE specialists (specialist_id, specialist_department_id, full_name, position, status) VALUES ({}+1,{},'{}','{}','{}');".format(
            int(max_id),
            int(department_id),
            self.specialist_new_full_name.content.value,
            self.specialist_new_position.content.value,
            self.cb_menu_status.content.value,
            )
          cursor.execute(query)
          print("Запись успешно добавлена в базу данных")
          self.alter_dialog_add_new_specialists.open = False
          self.show_specialists()
          self.page.update()
          
        except Exception as e:
          print(f"Ошибка при добавлении записи в базу данных: {str(e)}")
          self.components_manager.show_block_dialog("Заполните все поля!", "Ошибка")
        self.page.update()
        self.clear_enters()

    def show_alter_dialog(self, e):
      self.page.dialog = self.alter_dialog_add_new_specialists
      self.page.dialog.open = True
      self.page.update()

    def close_dlg(self, e):
      self.page.dialog = self.alter_dialog_add_new_specialists
      self.page.dialog.open = False
      self.page.update()      

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
        self.cb_menu_department.content.value = selected_row[1]
        self.specialist_new_full_name.content.value = selected_row[2]
        self.specialist_new_position.content.value = selected_row[3]
        self.cb_menu_status.content.value = selected_row[4]
        self.page.dialog = self.alter_dialog_edit
        self.alter_dialog_edit.open = True
        self.page.update()

    def edit_name_in_table(self, e):
      selected_row = next(iter(self.selected_rows))
      cursor = connection.cursor()
      sql_select = "SELECT department_id FROM name_of_department WHERE name = '{}'".format(self.cb_menu_department.content.value)
      cursor.execute(sql_select)
      department_id = cursor.fetchone()[0]
      if self.cb_menu_department.content.value != selected_row[1]:
        query_department = "ALTER TABLE specialists UPDATE specialist_department_id = {} WHERE specialist_id = {}".format(department_id, selected_row[0])
        cursor.execute(query_department)
        self.selected_rows.clear()
      if self.specialist_new_full_name.content.value != selected_row[2]:
        query_full_name = "ALTER TABLE specialists UPDATE full_name = '{}' WHERE specialist_id = {}".format(self.specialist_new_full_name.content.value, selected_row[0])
        cursor.execute(query_full_name)
        self.selected_rows.clear()
      if self.specialist_new_position.content.value != selected_row[3]:
        query_position = "ALTER TABLE specialists UPDATE position = '{}' WHERE specialist_id = {}".format(self.specialist_new_position.content.value, selected_row[0])
        cursor.execute(query_position)
        self.selected_rows.clear()
      if self.cb_menu_status.content.value != selected_row[4]:
        query_status = "ALTER TABLE specialists UPDATE status = '{}' WHERE specialist_id = {}".format(self.cb_menu_status.content.value, selected_row[0])
        cursor.execute(query_status)
        self.selected_rows.clear()
      self.page.dialog = self.alter_dialog_edit
      self.alter_dialog_edit.open = False
      self.components_manager.show_block_dialog("Запись была отредактирована успешно", "Успешно")
      self.show_specialists()
      self.page.update()
      self.clear_enters()

    def close_edit_dialog(self, e):
      self.clear_enters()
      self.page.dialog = self.alter_dialog_edit
      self.alter_dialog_edit.open = False
      self.page.update()

    def clear_enters(self):
      self.specialist_new_full_name.content.value = ""
      self.specialist_new_position.content.value = ""
      self.cb_menu_department.content.value = ""
      self.cb_menu_status.content.value = ""

    def delete_specialists(self, e):
      if not self.selected_rows:
            self.components_manager.show_block_dialog("Вы не выбрали строку в таблице", "Ошибка")
      else:
        cursor = connection.cursor()
        for selected_row in self.selected_rows:
            query_delete_department = f"DELETE FROM specialists WHERE specialist_id = {selected_row[0]}"
            cursor.execute(query_delete_department)
            connection.commit()
            print(query_delete_department)
        self.components_manager.show_block_dialog("Запись удалена", "Успешно")
        self.page.update()
        self.selected_rows.clear()
        self.show_specialists()