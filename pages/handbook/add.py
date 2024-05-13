from flet import *
from utils.consts import primary_colors 
from utils.components import *
from service.connection import *

class Add(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.theme_mode = ThemeMode.LIGHT
        self.alignment = alignment.center
        self.components_manager = Components(page)
        self.expand = True
        self.bgcolor = primary_colors['WHITE']
        self.selected_rows = set()
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
            border=border.all(1, primary_colors['BLACK']),
            vertical_lines=border.BorderSide(1, primary_colors['BLACK']),
            horizontal_lines=border.BorderSide(1, primary_colors['BLACK']),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=colors.BLACK12,
            heading_row_height=100,
            width=2000,
            data_row_max_height=100
        )
        
        self.dropdown_options_specialists = []
        self.dropdown_options_specialists_alter_dialoge = []
        dropdown_options_units_1 = []
        dropdown_options_units_2 = []
        dropdown_options_departments = []
        
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT name FROM name_of_department ORDER BY department_id')
            results = cursor.fetchall()

            for row in results:
                dropdown_options_departments.append(dropdown.Option(row[0]))

        except Exception as e:
            print(f"Error fetching data from the database: {str(e)}")
        
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
              size=12, color=primary_colors['MANATEE']
            ),
            label='Поле ввода',
            cursor_color=primary_colors['MANATEE'],
            text_style=TextStyle(
              size=14,
              color=primary_colors['GREEN'],
            ),
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
        self.cb_units = Container(
          content=Dropdown(
                hint_text='Выберите измерения',
                color=primary_colors['BLACK'],
                width=230,
                options=dropdown_options_units_1,  # Set the options from the fetched data
            ),
        )
        self.dp_units = Container(
          content=Dropdown(
                hint_text='Выберите измерения',
                color=primary_colors['BLACK'],
                width=300,
                options=dropdown_options_units_2,  # Set the options from the fetched data
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
        
        self.specialist_menu_box = Container(
            content=Dropdown(
                hint_text='Выберите специалиста',
                color=primary_colors['BLACK'],
                width=330,
                options=self.dropdown_options_specialists,
            )
        )
        self.specialist_menu_box_alter_dialoge = Container(
            content=Dropdown(
                hint_text='Выберите специалиста',
                color=primary_colors['BLACK'],
                width=330,
                options=self.dropdown_options_specialists_alter_dialoge,
            )
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
                self.specialist_menu_box_alter_dialoge
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
        self.content = ListView(
            spacing=0,
            # scroll=ScrollMode.ADAPTIVE,
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
                                    value='Добавление показателя в справочник',
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
                
#*MANUAL BUTTONS
                Container(
                    expand=True,
                    bgcolor=primary_colors['WHITE'],
                    content=Column(
                      expand=True,
                      # alignment='center',
                      horizontal_alignment='center',
                      controls=[
#*1ST ROW
                          Container(height=20),
                          Container(
                            Row(
                              spacing='50',
                              alignment='center',
                              controls=[
                                self.name_of_department_menu_box,
                                self.specialist_menu_box,
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
                                                  value='Сформировать',
                                                  size=16,
                                                  color=primary_colors['WHITE'],
                                                  text_align='center',
                                                  weight='bold',
                                              )
                                          )
                                      ]
                                  ),
                                  on_click=self.show_indicators,
                                ),
                              ]
                            )
                          ),
                          Container(
                            Row(
                              spacing='50',
                              alignment='center',
                              controls=[
                                  # Container(width=90),
                                  
                                  self.add_textfield_box,
                                  self.cb_units,
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
                                      on_click=self.show_edit_dialog,
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
                                                      value='Удалить',
                                                      size=16,
                                                      color=primary_colors['WHITE'],
                                                      text_align='center',
                                                      weight='bold',
                                                  )
                                              )
                                          ]
                                      ),
                                      on_click=self.delete_indicators,
                                  ),
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
            self.dropdown_options_specialists_alter_dialoge.append(dropdown.Option(row[0]))
            
        self.page.update()
      except Exception as e:
          print(f"Error fetching data from the database: {str(e)}")

    def show_indicators(self, e): 
      try:
        cursor = connection.cursor()
        sql_select_specialist_id = "SELECT specialist_id FROM specialists WHERE full_name = '{}'".format(self.specialist_menu_box.content.value)
        cursor.execute(sql_select_specialist_id)
        specialist_id = cursor.fetchone()[0]
        query_select = '''
        SELECT
            ni.indicators_id,
            um.type,
            ni.name,
        FROM name_of_indicators AS ni
        JOIN units_of_measurement AS um ON ni.measurement_id = um.measurement_id
        WHERE specialist_id = {}
        ORDER BY ni.indicators_id;
        '''.format(specialist_id)
        cursor.execute(query_select)
        results = cursor.fetchall()
        query_result = results
        if not query_result:
          self.components_manager.show_block_dialog("У пользователя нет заполненных показателей", "Информация")
        else:
          data_rows = []
          for row in query_result:
              cells = [DataCell(Text(str(value))) for value in row]
              data_row = DataRow(cells=cells)
              checkbox = Checkbox(value=False, on_change=lambda e, row=row: self.toggle_row_selection(e, row))
              cells.append(DataCell(checkbox))
              data_rows.append(data_row)
          self.data_table.rows = data_rows
          self.selected_rows.clear()
          self.page.dialog = self.alter_dialog_add_new_specialists
          self.alter_dialog_add_new_specialists.open = False
          self.page.update()
      except:
        self.components_manager.show_block_dialog("Вы не выбрали управление или специалиста", "Ошибка")

    def insert_into_db(self, e):
      selected_unit = self.cb_units.content.value
      if self.add_textfield_box.content.value == "" or selected_unit == "" or self.specialist_menu_box.content.value == "":
        self.components_manager.show_block_dialog("Вы не заполнили все поля", "Ошибка")
      else:
        try:
          cursor = connection.cursor()
          sql_select_specialist_id = "SELECT specialist_id FROM specialists WHERE full_name = '{}'".format(self.specialist_menu_box.content.value)
          cursor.execute(sql_select_specialist_id)
          specialist_id = cursor.fetchone()[0]
          cursor.execute(f"SELECT measurement_id FROM units_of_measurement WHERE type = '{selected_unit}'")
          units_id = cursor.fetchone()[0]
          cursor.execute("SELECT max(indicators_id) FROM name_of_indicators;")
          max_id = cursor.fetchone()[0]
          query = "INSERT INTO TABLE name_of_indicators (indicators_id, measurement_id, name, specialist_id) VALUES ({}+1,{},'{}',{})".format(int(max_id), units_id, self.add_textfield_box.content.value, int(specialist_id))
          cursor.execute(query)
          print("Запись успешно добавлена в базу данных")
          query_select = '''
          SELECT
              ni.indicators_id,
              um.type,
              ni.name,
          FROM name_of_indicators AS ni
          JOIN units_of_measurement AS um ON ni.measurement_id = um.measurement_id
          WHERE specialist_id = {}
          ORDER BY ni.indicators_id;
          '''.format(specialist_id)
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
          self.add_textfield_box.content.value = ""
          self.cb_units.content.value = ""
          self.page.update()
        except Exception as e:
          self.components_manager.show_block_dialog("Ошибка при добавлении записи в базу данных", "Ошибка")
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
            selected_data = selected_row[2]
            self.edit_name.content.value = selected_data
            self.dp_units.content.value = selected_row[1]
            self.specialist_menu_box_alter_dialoge.content.value = self.specialist_menu_box.content.value
            self.page.dialog = self.alter_dialog_add_new_specialists
            self.alter_dialog_add_new_specialists.open = True
            self.page.update()


    def edit_name_in_table(self, e):
        selected_row = next(iter(self.selected_rows))
        cursor = connection.cursor()
        sql_select_specialist_id = "SELECT specialist_id FROM specialists WHERE full_name = '{}'".format(self.specialist_menu_box.content.value)
        cursor.execute(sql_select_specialist_id)
        specialist_id = cursor.fetchone()[0]
        cursor.execute(f"SELECT measurement_id FROM units_of_measurement WHERE type = '{self.dp_units.content.value}'")
        units_id = cursor.fetchone()[0]
        sql_select_specialist_id_alter_dialoge = "SELECT specialist_id FROM specialists WHERE full_name = '{}'".format(self.specialist_menu_box_alter_dialoge.content.value)
        cursor.execute(sql_select_specialist_id_alter_dialoge)
        specialist_id_alter_dialoge = cursor.fetchone()[0]
        print(specialist_id_alter_dialoge)
        if self.edit_name.content.value != selected_row[2]:
            query_name = "ALTER TABLE name_of_indicators UPDATE name = '{}' WHERE indicators_id = {}".format(self.edit_name.content.value, selected_row[0])
            print(query_name)
            cursor.execute(query_name)
            self.show_indicators(e)
        elif self.dp_units.content.value != selected_row[1]:
            query_units = "ALTER TABLE name_of_indicators UPDATE measurement_id = {} WHERE indicators_id = {}".format(int(units_id), selected_row[0])
            print(query_units)
            cursor.execute(query_units)
            self.show_indicators(e)
        elif self.specialist_menu_box_alter_dialoge.content.value != self.specialist_menu_box.content.value:
            query_specialist = "ALTER TABLE name_of_indicators UPDATE specialist_id = {} WHERE indicators_id = {}".format(int(specialist_id_alter_dialoge), selected_row[0])
            print(query_specialist)
            cursor.execute(query_specialist)
            self.show_indicators(e)
        else:
            self.components_manager.show_block_dialog("Предупреждение","Изменений не было обнаружено")

    def close_edit_dialog(self, e):
        self.page.dialog = self.alter_dialog_add_new_specialists
        self.alter_dialog_add_new_specialists.open = False
        self.page.update()

    def delete_indicators(self, e):
      if not self.selected_rows:
            self.components_manager.show_block_dialog("Вы не выбрали строку в таблице", "Ошибка")
      else:
        cursor = connection.cursor()
        for selected_row in self.selected_rows:
            query_delete_department = f"DELETE FROM name_of_indicators WHERE indicators_id = {selected_row[0]}"
            cursor.execute(query_delete_department)
            connection.commit()
            print(query_delete_department)
        self.show_indicators(e)
        self.selected_rows.clear()
        self.components_manager.show_block_dialog("Запись удалена", "Успешно")
        self.page.update()