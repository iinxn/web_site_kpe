from flet import *
from utils.colors import * 
from service.connection import *
import datetime
import re
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd

class Report(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page  # Initialize the self.page object
        self.page.theme_mode = ThemeMode.LIGHT  # Set the theme mode
        self.alignment = alignment.center
        self.expand = True
        self.bgcolor = tea_green

        dropdown_options_specialists = []
        dropdown_options_departments = []
#*SELECT QUERY TO DISPLAY SPECIALISTS FROM DB
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT full_name FROM specialists ORDER BY specialist_id')
            results = cursor.fetchall()

            for row in results:
                dropdown_options_specialists.append(dropdown.Option(row[0]))
        except Exception as e:
            print(f"Error fetching data from the database: {str(e)}")

#*SELECT QUERY TO DISPLAY SPECIALISTS FROM DB
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT name FROM name_of_department ORDER BY department_id')
            results = cursor.fetchall()

            for row in results:
                dropdown_options_departments.append(dropdown.Option(row[0]))
        except Exception as e:
            print(f"Error fetching data from the database: {str(e)}")
        
#* DROPDOWN LISTS
        self.report_template = Container(
          content=Dropdown(
            # label='Специалист',
            hint_text='Выберите шаблон',
            color='black',
            # content_padding=30,
            options=[
              dropdown.Option('Карта КПЭ'),
              dropdown.Option('Расчет премии'),
              dropdown.Option('Сводные данные по исполнению')
            ]
          )
        )
        
        self.report_spec = Container(
          content=Dropdown(
            # label='Специалист',
            hint_text='Выберите специалиста',
            color='black',
            # content_padding=30,
            options=dropdown_options_specialists
          )
        )
        
        self.report_depart = Container(
          content=Dropdown(
            # label='Специалист',
            hint_text='Выберите управление',
            color='black',
            # content_padding=30,
            options=dropdown_options_departments
          )
        )
        
        self.report_quater = Container(
          content=Dropdown(
            # label='Специалист',
            hint_text='Выберите квартал',
            color='black',
            # content_padding=30,
            options=[
              dropdown.Option('1 квартал'),
              dropdown.Option('2 квартал'),
              dropdown.Option('3 квартал'),
              dropdown.Option('4 квартал'),
            ]
          )
        )
#*TEXT
        self.number_of_version_kpe = Container(
          Text(
            value=""
          )
        )
        
#*ALTER DIALOG
        self.alter_dialog = AlertDialog(
                modal=True,
                title=Text("Формирование отчета"),
                content=Column(
                  height=250,
                  controls=[
                    self.report_spec,
                    self.report_quater
                  ]
                ),
                actions=[
                    TextButton("Сформировать", on_click=self.alter_dialog_select_columns_data),
                    TextButton("Закрыть", on_click=self.close_dlg),
                ],
                actions_alignment=MainAxisAlignment.END,
                on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.alter_dialog_kpe = AlertDialog(
                modal=True,
                title=Text("Формирование отчета"),
                content=Column(
                  height=250,
                  controls=[
                    self.report_spec,
                  ]
                ),
                actions=[
                    TextButton("Сформировать", on_click=self.select_kpe),
                    TextButton("Закрыть", on_click=self.close_dlg_kpe),
                ],
                actions_alignment=MainAxisAlignment.END,
                on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.alter_dialog_summary = AlertDialog(
                modal=True,
                
                title=Text("Формирование отчета"),
                content=Column(
                  height=250,
                  width=700,
                  controls=[
                    self.report_quater,
                    # self.report_depart
                  ]
                ),
                actions=[
                    TextButton("Сформировать", on_click=self.select_summary),
                    TextButton("Закрыть", on_click=self.close_dlg_summary),
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

















#!UI
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
                                  # width=200,   
                                  bgcolor='white',
                                  width=70,
                                  height=70,
                                  border_radius=50,
                                  content=IconButton(
                                      icons.ARROW_BACK_OUTLINED,
                                      icon_color='#5B7553',
                                      icon_size=30,
                                      on_click=lambda x: x == self.page.go('/home')
                                  )
                                ),
                                Container(
                                    content=Text(
                                    value='Отчеты',
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
                
                #manual buttons
                Container(
                    expand=True,
                    bgcolor='white',
                    content=Column(
                      expand=True,
                      # alignment='center',
                      horizontal_alignment='center',
                      controls=[
                        #1st row
                          Container(height=50),
                          Container(
                            Row(
                              spacing='50',
                              alignment='center',
                              # horizontal_alignment='center',
                              controls=[
                                  self.report_template,
                                  # self.report_spec,
                                  # self.report_quater,
                                  ElevatedButton(
                                    color=white,
                                    bgcolor='#5B7553',
                                    width=250,
                                    height=70,
                                    content=Column(
                                      horizontal_alignment='center',
                                      alignment='center',
                                        controls=[
                                          Container(
                                            Text(
                                              value='Сформировать',
                                              size=16,
                                              color=white,
                                              text_align='center',
                                              weight='bold',
                                            )
                                          )
                                        ]
                                    ),
                                    on_click=self.form_report
                                    # on_click=lambda x: x == self.page.go('/home') 
                                  ),
                                  ElevatedButton(
                                    color=white,
                                    bgcolor='#5B7553',
                                    width=250,
                                    height=70,
                                    content=Column(
                                      horizontal_alignment='center',
                                      alignment='center',
                                        controls=[
                                          Container(
                                            Text(
                                              value='Экспорт',
                                              size=16,
                                              color=white,
                                              text_align='center',
                                              weight='bold',
                                            )
                                          )
                                        ]
                                    ),
                                    on_click=self.export_report_to_excel
                                  )
                              ]
                            )
                          ), 
                          
                          # Container(height=50),
                          #2nd row
                          Container(
                            content=DataTable(
                                    columns=[],
                                    rows=[],  # Leave this empty for now
                                    border=border.all(1, "black"),
                                    vertical_lines=border.BorderSide(1, "black"),
                                    horizontal_lines=border.BorderSide(1, "black"),
                                    sort_column_index=0,
                                    sort_ascending=True,
                                    heading_row_color=colors.BLACK12,
                                    heading_row_height=100,
                                    divider_thickness=0,
                                    
                                ),
                                alignment=alignment.center,
                                padding=padding.all(20),
                          ),
                          Container(
                            content=Row(
                              # width=1000,
                              controls=[
                                Container(width=800),
                                Container(width=700),
                                Container(content=self.number_of_version_kpe)
                              ]
                            )
                          )
                      ],
                  )
                ),
            ]
        )



















#!FUCNTIONS
    def show_success_dialog(self):
            self.page.dialog = self.alter_dialog_succes
            self.alter_dialog_succes.content = Text("Успешно")
            self.alter_dialog_succes.title = Text("Отчет был выгружен в Excel")
            self.alter_dialog_succes.open = True
            self.page.update()    
    def close_dlg_ok(self, e):
        self.page.dialog = self.alter_dialog_succes
        self.alter_dialog_succes.open = False
        print("Вы закрыли модульное окно успеха")
        self.page.update()
  
  #TODO: FOR Premium calculation
    def open_dialog(self):
      self.page.dialog = self.alter_dialog
      self.alter_dialog.open = True
      self.page.update()
    
    def alter_dialog_select_columns_data(self, e):
      cursor = connection.cursor()
      cursor.execute(f"SELECT specialist_id FROM specialists WHERE full_name='{str(self.report_spec.content.value)}';")
      user_id = cursor.fetchone()[0]
      
      query_select = 'SELECT number_of_version FROM kpe_table'
      cursor.execute(query_select)
      version_numbers = cursor.fetchall()

      indicator_versions = {}

      def extract_and_convert_date(version):
          match = re.search(r'-(\d{8})-(\d+)', version)
          if match:
              date_str = match.group(1)
              date = datetime.datetime.strptime(date_str, '%d%m%Y')
              version_number = int(match.group(2))
              return date, version, version_number
          return None

      for version_tuple in version_numbers:
        version = version_tuple[0]  # Получить второй элемент кортежа, который должен быть строкой
        date_version = extract_and_convert_date(version)
        if date_version is not None:
            date, version, version_number = date_version
            if version not in indicator_versions:
                indicator_versions[version] = [(date, version, version_number)]
            else:
                indicator_versions[version].append((date, version, version_number))


      for version, versions in indicator_versions.items():
          versions.sort(key=lambda x: (x[0], x[2]), reverse=True)
          latest_date, latest_version, latest_version_number = versions[0]
      
      quater = self.report_quater.content.value

      if quater == "1 квартал":
          quater_column = "`1st_quater_value`"
          weight_column = "KPE_weight_1"
      elif quater == "2 квартал":
          quater_column = "`2nd_quater_value`"
          weight_column = "KPE_weight_2"
      elif quater == "3 квартал":
          quater_column = "`3rd_quater_value`"
          weight_column = "KPE_weight_3"
      else:
          quater_column = "`4th_quater_value`"
          weight_column = "KPE_weight_4"

      query = f"""
          SELECT
              ROW_NUMBER() OVER () AS "порядковый номер",
              ni.name AS indicator_name,
              um.type AS unit_of_measurement,
              {quater_column},
              av.value AS actual_value,
              {weight_column},
              multiIf({quater_column} <= av.value, {weight_column} / 100, 0) AS bonus_share
          FROM kpe_table AS kt
          INNER JOIN actual_value AS av ON kt.kpe_indicators_id = av.actual_id
          INNER JOIN name_of_indicators AS ni ON kt.kpe_indicators_id = ni.indicators_id
          INNER JOIN units_of_measurement AS um ON kt.kpe_units_id = um.measurement_id
          WHERE kt.kpe_user_id = {user_id} AND kt.number_of_version = '{latest_version}'
          ORDER BY kt.kpe_id ASC
      """

          # Определите структуру колонок для "Премии"
      columns = [
          DataColumn(Text("№ пп."), numeric=True),
          DataColumn(Text("Наименование показателя")),
          DataColumn(Text("Ед.изм.")),
          DataColumn(Text("План")),
          DataColumn(Text("Факт")),
          DataColumn(Text("""Вес КПЭ,
  %""")),
          DataColumn(Text("""Доля премии по
  факту выполнения
  показателя""")),
          # Добавьте другие колонки для Премий
      ]
      
      cursor.execute(query)
      results = cursor.fetchall()

      query_result = results

      data_rows = []

      for row in query_result:
          cells = [DataCell(Text(str(value))) for value in row]
          data_row = DataRow(cells=cells)
          data_rows.append(data_row)
      self.content.controls[1].content.controls[2].content.columns = columns
      self.content.controls[1].content.controls[2].content.rows = data_rows
      
      self.page.dialog = self.alter_dialog
      self.alter_dialog.open = False
      self.page.update()
      

    def close_dlg(self, e):
      self.page.dialog = self.alter_dialog
      self.alter_dialog.open = False
      self.page.update()
    
    
    
#TODO: FOR KPE TABLE
    def open_dialog_kpe(self):
      self.page.dialog = self.alter_dialog_kpe
      self.alter_dialog_kpe.open = True
      self.page.update()
    
    def select_kpe(self, e):
      cursor = connection.cursor()
      cursor.execute(f"SELECT specialist_id FROM specialists WHERE full_name='{str(self.report_spec.content.value)}';")
      user_id = cursor.fetchone()[0]
      
      query_select = 'SELECT MAX(number_of_version) FROM kpe_table'
      cursor.execute(query_select)
      latest_version = cursor.fetchone()[0]

      query = f"""
          SELECT
              ROW_NUMBER() OVER () AS "порядковый номер",
              ni.name AS indicator_name,
              um.type AS unit_of_measurement,
              kt.1st_quater_value,
              kt.2nd_quater_value,
              kt.3rd_quater_value,
              kt.4th_quater_value,
              kt.year,
              kt.KPE_weight_1,
              kt.KPE_weight_2,
              kt.KPE_weight_3,
              kt.KPE_weight_4
          FROM kpe_table AS kt
          JOIN name_of_indicators AS ni ON kt.kpe_indicators_id = ni.indicators_id
          JOIN units_of_measurement AS um ON kt.kpe_units_id = um.measurement_id
          WHERE kt.kpe_user_id = {user_id} AND kt.number_of_version = '{latest_version}'
          ORDER BY kt.kpe_id;
      """

      
      # kt.plan_number_of_version,
      # kt.number_of_version
      # Определите структуру колонок для "Карта КПЭ"
      columns = [
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
      ]
      self.number_of_version_kpe.content.value = latest_version
      
      cursor.execute(query)
      results = cursor.fetchall()

      query_result = results

      data_rows = []

      for row in query_result:
          cells = [DataCell(Text(str(value))) for value in row]
          data_row = DataRow(cells=cells)
          data_rows.append(data_row)
      self.content.controls[1].content.controls[2].content.columns = columns
      self.content.controls[1].content.controls[2].content.rows = data_rows
      self.page.dialog = self.alter_dialog_kpe
      self.alter_dialog_kpe.open = False
      self.page.update()
      

    def close_dlg_kpe(self, e):
      self.page.dialog = self.alter_dialog_kpe
      self.alter_dialog_kpe.open = False
      self.page.update()
    
#TODO: SUMMARY TABLE
    def open_dialog_summary(self):
      self.page.dialog = self.alter_dialog_summary
      self.alter_dialog_summary.open = True
      self.page.update()
    
    def select_summary(self, e):
      cursor = connection.cursor()
      # cursor.execute(f"SELECT specialist_id FROM specialists WHERE full_name='{str(self.report_spec.content.value)}';")
      # user_id = cursor.fetchone()[0]
      query_select = 'SELECT MAX(number_of_version) FROM kpe_table'
      cursor.execute(query_select)
      latest_version = cursor.fetchone()[0]
      quater = self.report_quater.content.value

      if quater == "1 квартал":
          quater_column = "1st_quater_value"
          weight_column = "KPE_weight_1"
      elif quater == "2 квартал":
          quater_column = "2nd_quater_value"
          weight_column = "KPE_weight_2"
      elif quater == "3 квартал":
          quater_column = "3rd_quater_value"
          weight_column = "KPE_weight_3"
      else:
          quater_column = "4th_quater_value"
          weight_column = "KPE_weight_4"
      
      query = f"""
              SELECT
                  ROW_NUMBER() OVER () AS `порядковый номер`,
                  'агентство по труду и занятости населения Сахалинской области' AS `Наименование структурного подразделения Правительства Сахалинской области, государственного органа или органа исполнительной власти Сахалинской области`,
                  nd.name AS `Наименование структурного подразделения органа исполнительной власти Сахалинской области`,
                  s.position AS `Должность`,
                  s.full_name AS `ФИО`,
                  SUM((kt.{weight_column} / 100) * ((av.value * 100) / kt.`{quater_column}`)) AS `Процент выполнения`
              FROM kpe_table AS kt
              INNER JOIN specialists AS s ON kt.kpe_user_id = s.specialist_id
              INNER JOIN name_of_department AS nd ON s.specialist_department_id = nd.department_id
              INNER JOIN actual_value AS av ON kt.kpe_user_id = av.actual_users_id
              WHERE kt.number_of_version = {latest_version}
              GROUP BY
                  `Наименование структурного подразделения Правительства Сахалинской области, государственного органа или органа исполнительной власти Сахалинской области`,
                  `Наименование структурного подразделения органа исполнительной власти Сахалинской области`,
                  `Должность`,
                  `ФИО`
          """
          # Определите структуру колонок для "Премии"
      columns = [
          DataColumn(Text("""№
п/п"""), numeric=True),
          DataColumn(Text("""Наименование структурного
подразделения Правительства
Сахалинской области,
государственного органа
или органа исполнительной
власти Сахалинской области""")),
          DataColumn(Text("""Наименование структурного
подразделения органа
исполнительной власти
Сахалинской области""")),
          DataColumn(Text("Должность")),
          DataColumn(Text("ФИО")),
          DataColumn(Text("""Процент выполнения
КПЭ по итогам
отчетного периода, 
%""")),
          # Добавьте другие колонки для Премий
      ]
      
      cursor.execute(query)
      results = cursor.fetchall()

      query_result = results

      data_rows = []

      for row in query_result:
          cells = [DataCell(Text(str(value))) for value in row]
          data_row = DataRow(cells=cells)
          data_rows.append(data_row)
      self.content.controls[1].content.controls[2].content.columns = columns
      self.content.controls[1].content.controls[2].content.rows = data_rows
      
      self.page.dialog = self.alter_dialog_summary
      self.alter_dialog_summary.open = False
      self.page.update()
      

    def close_dlg_summary(self, e):
      self.page.dialog = self.alter_dialog_summary
      self.alter_dialog_summary.open = False
      self.page.update()















    def form_report(self, e):
      selected_report_type = self.report_template.content.value
      if selected_report_type == "Карта КПЭ":
        self.open_dialog_kpe()
#* РАСЧЕТ ПРЕМИИ
      elif selected_report_type == "Расчет премии":
        self.open_dialog()
#*СВОДНЫЕ ДАННЫЕ ПО ИСПОЛНЕНИЮ
      elif selected_report_type == "Сводные данные по исполнению":
          self.open_dialog_summary()
      else:
          print("Invalid report type")

      


    def export_report_to_excel(self, e):
      self.show_success_dialog()
#       cursor = connection.cursor()

#       # Определите SQL-запрос для получения данных, как показано в вашем коде

#       cursor = connection.cursor()
#       cursor.execute(f"SELECT specialist_id FROM specialists WHERE full_name='{str(self.report_spec.content.value)}';")
#       user_id = cursor.fetchone()[0]
      
#       query_select = 'SELECT number_of_version FROM kpe_table'
#       cursor.execute(query_select)
#       version_numbers = cursor.fetchall()

#       indicator_versions = {}

#       def extract_and_convert_date(version):
#           match = re.search(r'-(\d{8})-(\d+)', version)
#           if match:
#               date_str = match.group(1)
#               date = datetime.datetime.strptime(date_str, '%d%m%Y')
#               version_number = int(match.group(2))
#               return date, version, version_number
#           return None

#       for version_tuple in version_numbers:
#         version = version_tuple[0]  # Получить второй элемент кортежа, который должен быть строкой
#         date_version = extract_and_convert_date(version)
#         if date_version is not None:
#             date, version, version_number = date_version
#             if version not in indicator_versions:
#                 indicator_versions[version] = [(date, version, version_number)]
#             else:
#                 indicator_versions[version].append((date, version, version_number))


#       for version, versions in indicator_versions.items():
#           versions.sort(key=lambda x: (x[0], x[2]), reverse=True)
#           latest_date, latest_version, latest_version_number = versions[0]
#       query = f"""
#           SELECT
#               ROW_NUMBER() OVER () AS "порядковый номер",
#               ni.name AS indicator_name,
#               um.type AS unit_of_measurement,
#               kt.1st_quater_value,
#               kt.2nd_quater_value,
#               kt.3rd_quater_value,
#               kt.4th_quater_value,
#               kt.year,
#               kt.KPE_weight_1,
#               kt.KPE_weight_2,
#               kt.KPE_weight_3,
#               kt.KPE_weight_4
#           FROM kpe_table AS kt
#           JOIN name_of_indicators AS ni ON kt.kpe_indicators_id = ni.indicators_id
#           JOIN units_of_measurement AS um ON kt.kpe_units_id = um.measurement_id
#           WHERE kt.kpe_user_id = {user_id} AND kt.number_of_version = '{latest_version}'
#           ORDER BY kt.kpe_id;
#       """
      
#       # kt.plan_number_of_version,
#       # kt.number_of_version
#       # Определите структуру колонок для "Карта КПЭ"
#       columns = [
#           DataColumn(Text("п/п"), numeric=True),
#           DataColumn(Text("Наименование показателя")),
#           DataColumn(Text("Ед.изм.")),
#           DataColumn(Text("""1
# кв."""), numeric=True),
#           DataColumn(Text("""2
# кв."""), numeric=True),
#           DataColumn(Text("""3
# кв."""), numeric=True),
#           DataColumn(Text("""4
# кв."""), numeric=True),
#           DataColumn(Text("год")),
#           DataColumn(Text("""   Вес КПЭ 
# 1 кв."""), numeric=True),
#           DataColumn(Text("""   Вес КПЭ 
# 2 кв."""), numeric=True),
#           DataColumn(Text("""   Вес КПЭ 
# 3 кв."""), numeric=True),
#           DataColumn(Text("""   Вес КПЭ 
# 4 кв."""), numeric=True),
#       ]
#       self.number_of_version_kpe.content.value = latest_version
      
#       cursor.execute(query)
#       results = cursor.fetchall()

#       # Создайте Pandas DataFrame с результатами запроса
#       data_df = pd.DataFrame(results, columns=[
#           "п/п",
#           "Наименование показателя",
#           "Ед.изм.",
#           "1 квартал",
#           "2 квартал",
#           "3 квартал",
#           "4 квартал",
#           "год",
#           "Вес КПЭ 1 квартал",
#           "Вес КПЭ 2 квартал",
#           "Вес КПЭ 3 квартал",
#           "Вес КПЭ 4 квартал"
#       ])

#       # Запросите у пользователя путь и имя файла для сохранения
#       file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])

#       if file_path:
#           # Создайте новую рабочую книгу и лист
#           workbook = openpyxl.Workbook()
#           sheet = workbook.active

#           # Запишите данные из DataFrame в лист
#           for row in dataframe_to_rows(data_df, index=False, header=True):
#               sheet.append(row)

#           # Сохраните книгу по указанному пути
#           workbook.save(file_path)

#           print(f"Отчет успешно сохранен в {file_path}")
        # output_path = "D:/tniki/Documents/projects/KPE/templates/output.xlsx"
        # cursor = connection.cursor()
        # # Создайте новую рабочую книгу и лист
        # workbook = Workbook()
        # sheet = workbook.active

        # # Здесь вставьте код для извлечения данных из базы данных в Pandas DataFrame
        # # Это предполагает, что у вас уже есть DataFrame с данными для экспорта

        # # Ваш SQL-запрос для извлечения данных из базы данных
        # query = """
        # SELECT
        #           kt.kpe_id,
        #           ni.name AS indicator_name,
        #           um.type AS unit_of_measurement,
        #           kt.1st_quater_value,
        #           kt.2nd_quater_value,
        #           kt.3rd_quater_value,
        #           kt.4th_quater_value,
        #           kt.year,
        #           kt.KPE_weight_1,
        #           kt.KPE_weight_2,
        #           kt.KPE_weight_3,
        #           kt.KPE_weight_4
        #       FROM kpe_table AS kt
        #       JOIN name_of_indicators AS ni ON kt.kpe_indicators_id = ni.indicators_id
        #       JOIN units_of_measurement AS um ON kt.kpe_units_id = um.measurement_id
        #       WHERE kt.kpe_user_id = 1
        #       ORDER BY kt.kpe_id;
        # """

        # cursor.execute(query)
        # results = cursor.fetchall()

        # # Затем, используя Pandas DataFrame, создайте таблицу данных
        # data_df = pd.DataFrame(results, columns=[
        #     "п/п",
        #     "Наименование показателя",
        #     "Ед.изм.",
        #     "1 квартал",
        #     "2 квартал",
        #     "3 квартал",
        #     "4 квартал",
        #     "год",
        #     "Вес КПЭ 1 квартал",
        #     "Вес КПЭ 2 квартал",
        #     "Вес КПЭ 3 квартал",
        #     "Вес КПЭ 4 квартал"
        # ])

        # # Сначала запишите заголовки в лист
        # for col_num, header in enumerate(data_df.columns, 1):
        #     sheet.cell(row=1, column=col_num, value=header)

        # # Затем запишите данные в лист с использованием Pandas DataFrame
        # for row in dataframe_to_rows(data_df, index=False, header=False):
        #     sheet.append(row)

        # # Сохраните книгу
        # workbook.save(output_path)
