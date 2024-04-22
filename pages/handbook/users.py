from flet import *
from utils.consts import primary_colors 
from service.connection import *
from utils.components import *

class Users(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.theme_mode = ThemeMode.LIGHT
        self.alignment = alignment.center
        self.expand = True
        self.bgcolor = primary_colors['WHITE']
        self.components_manager = Components(page)
        self.selected_rows = set()
        
        self.data_table = DataTable(
            columns=[
                DataColumn(Text("Код пользователя"), numeric=True),
                DataColumn(Text("Логин")),
                DataColumn(Text("Пароль")),
                DataColumn(Text("ФИО")),
                DataColumn(Text("Статус")),
                DataColumn(Text("Выбор")),
            ],
            rows=[],  # Leave this empty for now
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
        self.user_login = Container(
          content=TextField(
                  label="Введите логин пользователя",
                  hint_style=TextStyle(
                      size=12, color=primary_colors['MANATEE']
                  ),
                  cursor_color=primary_colors['MANATEE'],
                  text_style=TextStyle(
                    size=14,
                    color=primary_colors['BLACK'],
                  ),
                  width=330
              ),
        )
        self.user_password = Container(
          content=TextField(
                  label="Введите пароль пользователя",
                  hint_style=TextStyle(
                      size=12, color=primary_colors['MANATEE']
                  ),
                  cursor_color=primary_colors['MANATEE'],
                  text_style=TextStyle(
                    size=14,
                    color=primary_colors['BLACK'],
                  ),
                  width=330
              ),
        )
        self.user_full_name = Container(
          content=TextField(
                  label="Введите ФИО пользователя",
                  hint_style=TextStyle(
                      size=12, color=primary_colors['MANATEE']
                  ),
                  cursor_color=primary_colors['MANATEE'],
                  text_style=TextStyle(
                    size=14,
                    color=primary_colors['BLACK'],
                  ),
                  width=330
              ),
        )
#*DROPDOWNS
        self.cb_menu_status = Container(
          content=Dropdown(
                hint_text='Выберите статус',
                color=primary_colors['BLACK'],
                width=330,
                options=[
                  dropdown.Option("Активный"),
                  dropdown.Option("Неактивный")
                ],
            ),
        )

#*ALTERDIALOGS
        self.alter_dialog_add_new_users = AlertDialog(
            modal=True,
            title=Text("Добавление пользователя в справочник"),
            content=Column(
              height=250,
              controls=[
                self.user_login,
                self.user_password,
                self.user_full_name,
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
                                                value='Добавить пользователя в справочник',
                                                size=18,
                                                color=primary_colors['WHITE'],
                                                text_align='center',
                                            ),
                                        ),
                                        Container(
                                          width=400,
                                          content=Row(
                                            spacing=10,
                                            controls= [
                                              Container(
                                                ElevatedButton(
                                                  color=primary_colors['WHITE'],
                                                  bgcolor=primary_colors['WHITE'],
                                                  width=200,
                                                  height=70,
                                                  content=Column(
                                                    horizontal_alignment='center',
                                                    alignment='center',
                                                      controls=[
                                                        Container(
                                                          
                                                          Text(
                                                            value='Добавить нового пользователя',
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
                                              ),
                                              Container(
                                                ElevatedButton(
                                                  color=primary_colors['WHITE'],
                                                  bgcolor=primary_colors['WHITE'],
                                                  width=200,
                                                  height=70,
                                                  content=Column(
                                                    horizontal_alignment='center',
                                                    alignment='center',
                                                      controls=[
                                                        Container(
                                                          
                                                          Text(
                                                            value='Удалить пользователя',
                                                            size=16,
                                                            color=primary_colors['GREEN'],
                                                            text_align='center',
                                                            weight='bold',
                                                          )
                                                        )
                                                      ]
                                                  ),
                                                  on_click=self.delete_users_from_table
                                                ),  
                                              ),
                                            ],
                                          )
                                        )
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
                                content = self.data_table,
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
        query_select = "SELECT * FROM users ORDER BY user_id;" 
        cursor.execute(query_select)
        results = cursor.fetchall()
        query_result = results
        for row in query_result:
            cells = [DataCell(Text(str(value))) for value in row]
            checkbox = Checkbox(value=False, on_change=lambda e, row=row: self.toggle_row_selection(e, row))
            cells.append(DataCell(checkbox))
            data_row = DataRow(cells=cells)
            self.data_table.rows.append(data_row)
        self.content.controls[1].content.controls[2] = self.data_table
        self.page.update()
        
    def show_table(self):
      cursor = connection.cursor()
      query_select = "SELECT * FROM users ORDER BY user_id;" 
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
    

    def show_alter_dialog(self, e):
      self.page.dialog = self.alter_dialog_add_new_users
      self.page.dialog.open = True
      self.page.update()
    
    
    def close_dlg(self, e):
      self.page.dialog = self.alter_dialog_add_new_users
      self.page.dialog.open = False
      self.page.update()
      
    def add_new_specialist(self, e):
      if (self.user_password.content.value == "" or 
          self.user_full_name.content.value == "" or
          self.user_login.content.value == "" or
          self.cb_menu_status.content.value == ""):
        print("Please")
      else:
        try:
          cursor = connection.cursor()
          
          cursor.execute(f"SELECT max(user_id) FROM users;")
          max_id = cursor.fetchone()[0]
          print(max_id)
          query = "INSERT INTO TABLE users (user_id, login, password, full_name, status) VALUES ({}+1,'{}','{}','{}','{}')".format(
            int(max_id),
            self.user_login.content.value,
            self.user_password.content.value,
            self.user_full_name.content.value,
            self.cb_menu_status.content.value
          )
          print(query)
          cursor.execute(query)
          self.user_password.content.value = ""
          self.user_full_name.content.value = ""
          self.user_login.content.value = ""
          self.cb_menu_status.content.value = ""
          self.components_manager.show_block_dialog("Запись успешно добавлена в базу данных", "Успешно")
          print("Запись успешно добавлена в базу данных")
          self.alter_dialog_add_new_users.open = False
          self.show_table()
          
        except Exception as e:
                print(f"Ошибка при добавлении записи в базу данных: {str(e)}")
    
    def toggle_row_selection(self, e, row):
        if row not in self.selected_rows:
            self.selected_rows.add(row)
        else:
            self.selected_rows.remove(row)
    
    def delete_users_from_table(self, e):
        cursor = connection.cursor()
        if not self.selected_rows:
            print('Вы не выбрали строку')
        else:
          for selected_row in self.selected_rows:
              cursor.execute(f'DELETE FROM users WHERE user_id = {selected_row[0]}')
        self.show_table()
        self.components_manager.show_block_dialog("Запись была успешно удалена", "Удаление")
        self.page.update()