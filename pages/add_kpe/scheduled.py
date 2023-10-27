from flet import *
from utils.colors import * 
from service.connection import *
import datetime
import re

class Scheduled(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        # page.theme = theme.Theme(color_scheme_seed="green")
        self.page.theme_mode = ThemeMode.LIGHT
        self.alignment = alignment.center
        self.expand = True
        self.bgcolor = tea_green
        self.end_edit = False

        self.use_truncated_options = True
        self.dropdown_options_indicators = []
        self.dropdown_options_indicators_truncated = []
        dropdown_options_units = []
        dropdown_options_specialists = []
#*SELECT QUERY TO DIPLAY NAMES OF INDICATORS FROM DB
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT name FROM name_of_indicators ORDER BY indicators_id')
            results = cursor.fetchall()
            max_length = 40
            for row in results:
              truncated_text = row[0] if len(row[0]) <= max_length else row[0][:max_length] + "..."
              self.dropdown_options_indicators.append(dropdown.Option(row[0]))
              self.dropdown_options_indicators_truncated.append(dropdown.Option(truncated_text))

            # Add "Нет в списке" option at the end
            self.dropdown_options_indicators.append(dropdown.Option('Нет в списке'))
        except Exception as e:
            print(f"Error fetching data from the database: {str(e)}")
#*SELECT QUERY TO DISPLAY UNITS FROM DB
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT type FROM units_of_measurement ORDER BY measurement_id')
            results = cursor.fetchall()

            for row in results:
                dropdown_options_units.append(dropdown.Option(row[0]))
        except Exception as e:
            print(f"Error fetching data from the database: {str(e)}")
        
#*SELECT QUERY TO DISPLAY SPECIALISTS FROM DB
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT full_name FROM specialists ORDER BY specialist_id')
            results = cursor.fetchall()

            for row in results:
                dropdown_options_specialists.append(dropdown.Option(row[0]))
        except Exception as e:
            print(f"Error fetching data from the database: {str(e)}")
        
#*THERE ARE MY BOXES FOR 2ND ROW
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
#* THERE ARE MY NEXT BOXES FOR MY 3RD ROW
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
                  width=100
              ),
        )
#*DROPDOWN MENU
        # Create the Dropdown container
        self.cb_menu_spec = Container(
            content=Dropdown(
                label='Выберите наименование показателя',
                color="black",
                width=330,
                # filled=True,
                options=self.dropdown_options_indicators_truncated,
                on_change=self.added_new_to_indicators,
                # on_focus=self.toggle_options# Set the event handler
            ),
        )
        self.units_menu_box = Container(
          content=Dropdown(
                hint_text='Выберите измерения',
                color="black",
                width=330,
                options=dropdown_options_units,  # Set the options from the fetched data
            ),
        )
        self.specialist_menu_box = Container(
          content=Dropdown(
            hint_text='Выберите специалиста',
            color="black",
            width=330,
            options=dropdown_options_specialists, 
          )
        )
#*MODULE FORM
        self.alter_dialog = AlertDialog(
                modal=True,
                title=Text("Добавление показателя в справочник"),
                content=self.textfiled_input_new_indicator,
                actions=[
                    TextButton("Добавить", on_click=self.alter_dialoge_input_data),
                    TextButton("Назад", on_click=self.close_dlg),
                ],
                actions_alignment=MainAxisAlignment.END,
                on_dismiss=lambda e: print("Modal dialog dismissed!"),
                
            )
        self.alter_dialog_succes = AlertDialog(
            modal=True,
            title=Text("Default Title"),
            content=Text("Default Content"),
            actions=[TextButton("OK", on_click=self.close_dlg_ok)],
            on_dismiss=lambda e: print("Modal dialog dismissed!")
        )
        self.alter_dialog_error = AlertDialog(
            modal=True,
            title=Text("Default Title"),
            content=Text("Default Content"),
            actions=[TextButton("OK", on_click=self.close_dlg_error)],
            on_dismiss=lambda e: print("Modal dialog dismissed!")
        )
        self.alter_dialog_block = AlertDialog(
            modal=True,
            title=Text("Default Title"),
            content=Text("Default Content"),
            actions=[TextButton("OK", on_click=self.close_dlg_block)],
            on_dismiss=lambda e: print("Modal dialog dismissed!")
        )

#*ELEVATED BUTTNON
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
#*THIS IS A HEADER
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
                                    value='Плановое',
                                    size=18,
                                    color='white',
                                    text_align='center',
                                  ),
                                ),
                                Container(
                                  self.elevated_button_end,
                                ),
                              ]
                            )
                          )  
                        ],
                    )
                ),
                
#*THERE ARE MANUAL BUTTONS FOR THIS FORM
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
                              # horizontal_alignment='center',
                              controls=[
                                  # Container(width=90)
                                  self.cb_menu_spec,
                                #*dropdown 1st row
                                  #specialist
                                  self.specialist_menu_box,
                                  #*NAME OF INDICATOR
                                  # self.units_menu_box,
                              ]
                            )
                          ), 
                          
                          Container(height=50),
#*2ND ROW
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
                                  #*Name of indicator
                                  self.first_qr_box,
                                  self.second_qr_box,
                                  self.third_qr_box,
                                  self.fourtht_qr_box,
                                  self.year_box,
                              ]
                            )
                          ), 
                          
                          Container(height=50),
#*3RD ROW
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
#*4TH ROW
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
    def end_input_data(self,e):
      self.show_blocked()

#TODO: These are a functions that i use for spawn alter dialog and insert data to name_of_indicator table in DB
    # def toggle_options(self, e):
    #   # Переключайтесь между сокращенными и полными опциями
    #   if not self.use_truncated_options:
    #       self.cb_menu_spec.content.options = self.dropdown_options_indicators
    #       self.use_truncated_options = True

    #   self.page.update()

    def added_new_to_indicators(self, e):
        selected_item = self.cb_menu_spec.content.value  # Получите выбранную опцию
        # max_length = 20
        # truncated_text = selected_item if len(selected_item) <= max_length else selected_item[:max_length] + "..."
        # self.cb_menu_spec.content.options = self.dropdown_options_indicators_truncated  # Используйте сокращенные версии опций
        # self.showing_full_options = True
        # self.cb_menu_spec.content.value = truncated_text
        # self.cb_menu_spec.content.disabled = True
        # self.page.update()
        print(f"Selected item: {selected_item}")  # Отладочный вывод: Выведите выбранную опцию
        if selected_item == "Нет в списке":
            self.page.dialog = self.alter_dialog
            print("Opening dialog...")  # Отладочный вывод: Откройте диалоговое окно
            self.alter_dialog.open = True
        self.page.update()




    def alter_dialoge_input_data(self, e):
      try:
          cursor = connection.cursor()
          cursor.execute(f"SELECT max(indicators_id) FROM name_of_indicators;")
          max_id = cursor.fetchone()[0]
          query = "INSERT INTO TABLE name_of_indicators (indicators_id, name) VALUES ({},'{}')".format(int(max_id) + 1,self.textfiled_input_new_indicator.content.value)
          cursor.execute(query)
          print("Запись успешно добавлена в базу данных")
          self.page.dialog = self.alter_dialog
          self.alter_dialog.open = False
          self.page.update()
      except Exception as e:
          print(f"Ошибка при добавлении записи в базу данных: {str(e)}")
      

    def close_dlg(self, e):
        self.page.dialog = self.alter_dialog
        self.alter_dialog.open = False
        self.page.update()


#TODO: These two functions for succes message
    def show_success_dialog(self):
            self.page.dialog = self.alter_dialog_succes
            self.alter_dialog_succes.content = Text("Успешно")
            self.alter_dialog_succes.title = Text("Запись успешно добавлена в базу данных")
            self.alter_dialog_succes.open = True
            self.page.update()    
    def close_dlg_ok(self, e):
        self.page.dialog = self.alter_dialog_succes
        self.alter_dialog_succes.open = False
        print("Вы закрыли модульное окно успеха")
        self.page.update()


#TODO: These two functions for error message
    def show_error_dialog(self):
        self.page.dialog = self.alter_dialog_error
        self.alter_dialog_error.title = Text("Ошибка")
        self.alter_dialog_error.content = Text("Ошибка при добавлении записи в базу данных")
        self.alter_dialog_error.open = True
        self.page.update()    
    def close_dlg_error(self, e):
        self.page.dialog = self.alter_dialog_error
        self.alter_dialog_error.open = False
        print("Вы закрыли модульное окно ошибки")
        self.page.update()




#TODO: These two functions for blocked message
    def show_blocked(self):
      # try:
        date = datetime.datetime.now()
        formatted_date = date.strftime("%d%m%Y")
        self.page.dialog = self.alter_dialog_block
        self.alter_dialog_block.title = Text("Карта КПЭ сформирована")
        self.alter_dialog_block.content = Text("Вы завершили формирование карты КПЭ")
        self.alter_dialog_block.open = True
        self.page.update()

        #*FOR AUTO ID INCRIPTION
        cursor = connection.cursor()
        cursor.execute(f"SELECT max(kpe_id) FROM kpe_table;")
        max_kpe_id = cursor.fetchone()
        
        query_select = 'SELECT plan_indicators_id FROM planned_value'
        cursor.execute(query_select)
        indicator = cursor.fetchall()
        print(indicator)

        query_select = 'SELECT MAX(number_of_version) FROM planned_value'
        cursor.execute(query_select)
        latest_version = cursor.fetchone()[0]

        # Получение данных из planned_value
        query_select = """
            SELECT plan_indicators_id, plan_user_id, plan_units_id, 1st_quater_value, 2nd_quater_value, 3rd_quater_value, 4th_quater_value, year,
                  KPE_weight_1, KPE_weight_2, KPE_weight_3, KPE_weight_4
            FROM planned_value
            WHERE number_of_version = '{}';
        """.format(latest_version)
        cursor.execute(query_select)
        data = cursor.fetchone()

        if data:
            plan_indicators_id, user_id, units_id, first_qr_value, second_qr_value, third_qr_value, fourth_qr_value, year, weight_1, weight_2, weight_3, weight_4 = data
            check_query = """
                SELECT MAX(number_of_version) FROM kpe_table 
                WHERE kpe_indicators_id = {}
            # """.format(indicator)
            cursor.execute(check_query)
            existing_versions = cursor.fetchone()[0]
            print(existing_versions)
            # Создание номера версии
            number_of_version_get = existing_versions.split("-")
            print(number_of_version_get)
            try:
              if existing_versions is not None:
                  number_of_current_version = int(number_of_version_get[2])
              else:
                  number_of_current_version = 0  # Если номер версии не найден, начнем с 0
              number_of_verison_plus = f"{1}-{formatted_date}-{number_of_current_version + 1}"
            except:
              number_of_verison_plus = f"{1}-{formatted_date}-{1}"


            # Вставка данных в kpe_table
            # Вставка данных в kpe_table
            insert_query_to_kpe_table = "INSERT INTO kpe_table (kpe_id, kpe_indicators_id, kpe_user_id, kpe_units_id, 1st_quater_value, 2nd_quater_value, 3rd_quater_value, 4th_quater_value, year, KPE_weight_1, KPE_weight_2, KPE_weight_3, KPE_weight_4, number_of_version, plan_number_of_version) VALUES ({}+1, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, '{}','{}');".format(
                int(max_kpe_id),
                int(plan_indicators_id),
                int(user_id),  # Похоже, здесь нужно вставить правильное значение для kpe_user_id
                int(units_id),
                int(first_qr_value),
                int(second_qr_value),
                int(third_qr_value),
                int(fourth_qr_value),
                int(year),
                int(weight_1),
                int(weight_2),
                int(weight_3),
                int(weight_4),
                str(number_of_verison_plus),
                str(latest_version)
            )
            print("SQL Query:", insert_query_to_kpe_table)

            cursor.execute(insert_query_to_kpe_table)
            connection.commit()
            print("Success")

    def close_dlg_block(self, e):
      self.page.dialog = self.alter_dialog_block
      self.alter_dialog_block.open = False
      print("Вы закрыли модульное окно блокировки")
      self.page.update()






#TODO: This is a insert function for add new data to planned table
    def insert_into_db(self, e): 
      if self.end_edit == False:
        # try:
              date = datetime.datetime.now()
              formatted_date = date.strftime("%d%m%Y")
              # print(formatted_date)
            #*FOR USER DATA INFORMATION
              cursor = connection.cursor()
              cursor.execute(f"SELECT specialist_id FROM specialists WHERE full_name='{str(self.specialist_menu_box.content.value)}';")
              user_id = cursor.fetchone()[0]
              
            #*FOR AUTO ID INCRIPTION
              cursor = connection.cursor()
              cursor.execute(f"SELECT max(plan_id) FROM planned_value;")
              max_id = cursor.fetchone()[0]
              # print(f"{user_id}-{formatted_date}-{max_id}")
            #*FOR INDICATORS
              selected_indicator = self.cb_menu_spec.content.value
              cursor = connection.cursor()
              selected_indicator_without_dots = selected_indicator.replace(".", "")
              cursor.execute(f"SELECT indicators_id FROM name_of_indicators WHERE name LIKE '{selected_indicator_without_dots}%'")
              indicator_id = cursor.fetchone()[0]
            #*FRO PLAN_INDICATOR
              cursor = connection.cursor()
              cursor.execute(f"SELECT plan_indicators_id FROM planned_value")
              plan_indicator_id = cursor.fetchone()
            #*FOR UNITS
              # selected_unit = self.units_menu_box.content.value
              cursor = connection.cursor()
              # cursor.execute(f"SELECT measurement_id FROM name_of_indicators WHERE name LIKE '{selected_indicator}%'")
              cursor.execute(f"SELECT measurement_id FROM name_of_indicators WHERE name LIKE '{selected_indicator_without_dots}%'")
              units_id = cursor.fetchone()[0]
              
              # Определите максимальное значение номера версии для данного показателя
              cursor.execute(f"SELECT MAX(number_of_version) FROM planned_value WHERE plan_indicators_id = {int(indicator_id)}")
              # max_version = cursor.fetchone()[0]

              # Если max_version равен None (то есть нет записей для этого показателя), начните с 1
              number_of_version_get = cursor.fetchone()[0]
              current_version = number_of_version_get.split("-")
              try:
                if current_version is not None:
                    number_of_current_version = int(current_version[2])
                else:
                    number_of_current_version = 0  # Если номер версии не найден, начнем с 0
                number_of_verison_plus = f"{user_id}-{formatted_date}-{number_of_current_version + 1}"
              except:
                number_of_verison_plus = f"{user_id}-{formatted_date}-{1}"

              query = """
                  INSERT INTO planned_value (plan_id, plan_indicators_id, plan_user_id, plan_units_id, 1st_quater_value, 2nd_quater_value, 3rd_quater_value, 4th_quater_value, year, KPE_weight_1, KPE_weight_2, KPE_weight_3, KPE_weight_4, number_of_version)
                  VALUES ({}+1, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {},'{}');
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
                  int(self.weight_first_qr_box.content.value),
                  int(self.weight_second_qr_box.content.value),
                  int(self.weight_third_qr_box.content.value),
                  int(self.weight_fourth_qr_box.content.value),
                  str(number_of_verison_plus),
              )

              cursor.execute(query)
              connection.commit()
              self.show_success_dialog()
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
              self.specialist_menu_box.content.value = ""
              print("Запись успешно добавлена в базу данных")

        # except Exception as e:
        #     self.show_error_dialog()
        #     print(f"Ошибка при добавлении записи в базу данных: {str(e)}")
      else:
        print("Blocked")

