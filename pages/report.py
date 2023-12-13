from flet import *
from utils.colors import * 
from service.connection import *
import datetime
import re
import openpyxl
from openpyxl.styles import Font, Alignment


class Report(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page  # Initialize the self.page object
        self.page.theme_mode = ThemeMode.LIGHT  # Set the theme mode
        self.alignment = alignment.center
        self.expand = True
        self.bgcolor = tea_green
        
        # self.file_picker = FilePicker()
        # page.overlay.append(self.file_picker)
        # page.update()

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
            dropdown_options_departments.append(dropdown.Option("Все управления"))
                
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
                    self.report_depart
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
                                    # on_click=lambda _: self.file_picker.pick_files()
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
      
      # query_select = 'SELECT number_of_version FROM kpe_table'
      # cursor.execute(query_select)
      # version_numbers = cursor.fetchall()

      # indicator_versions = {}

      # def extract_and_convert_date(version):
      #     match = re.search(r'-(\d{8})-(\d+)', version)
      #     if match:
      #         date_str = match.group(1)
      #         date = datetime.datetime.strptime(date_str, '%d%m%Y')
      #         version_number = int(match.group(2))
      #         return date, version, version_number
      #     return None

      # for version_tuple in version_numbers:
      #   version = version_tuple[0]  # Получить второй элемент кортежа, который должен быть строкой
      #   date_version = extract_and_convert_date(version)
      #   if date_version is not None:
      #       date, version, version_number = date_version
      #       if version not in indicator_versions:
      #           indicator_versions[version] = [(date, version, version_number)]
      #       else:
      #           indicator_versions[version].append((date, version, version_number))


      # for version, versions in indicator_versions.items():
      #     versions.sort(key=lambda x: (x[0], x[2]), reverse=True)
      #     latest_date, latest_version, latest_version_number = versions[0]
      
      query_select = f'SELECT MAX(number_of_version) FROM kpe_table WHERE kpe_user_id = {user_id}'
      cursor.execute(query_select)
      latest_version = cursor.fetchone()[0]
      
      quater = self.report_quater.content.value

      if quater == "1 квартал":
          quater_column = "`1st_quater_value`"
          weight_column = "KPE_weight_1"
          actual_quater_value = "1-й квартал"
      elif quater == "2 квартал":
          quater_column = "`2nd_quater_value`"
          weight_column = "KPE_weight_2"
          actual_quater_value = "2-й квартал"
      elif quater == "3 квартал":
          quater_column = "`3rd_quater_value`"
          weight_column = "KPE_weight_3"
          actual_quater_value = "3-й квартал"
      else:
          quater_column = "`4th_quater_value`"
          weight_column = "KPE_weight_4"
          actual_quater_value = "4-й квартал"

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
          INNER JOIN actual_value AS av ON kt.kpe_indicators_id = av.actual_indicators_id
          INNER JOIN name_of_indicators AS ni ON kt.kpe_indicators_id = ni.indicators_id
          INNER JOIN units_of_measurement AS um ON kt.kpe_units_id = um.measurement_id
          WHERE kt.kpe_user_id = {user_id} AND kt.number_of_version = '{latest_version}'
          AND av.actual_users_id = kt.kpe_user_id
          AND av.quarter_number = '{actual_quater_value}'
          AND kt.status = 'Активно'
          ORDER BY kt.kpe_id ASC
      """
      print(query)
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
      
      query_select = "SELECT MAX(number_of_version) FROM kpe_table WHERE kpe_user_id = {}".format(user_id)
      cursor.execute(query_select)
      latest_version = cursor.fetchone()[0]
      print(user_id)
      print(latest_version)
      
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
          WHERE kt.kpe_user_id = {user_id} AND kt.number_of_version = '{latest_version}' AND kt.status = 'Активно'
          ORDER BY kt.kpe_id;
      """
      print(query)
      
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
      global results
      results = cursor.fetchall()
      # print(results)
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
      # self.export_report_to_excel(results)

    def close_dlg_kpe(self, e):
      self.page.dialog = self.alter_dialog_kpe
      self.alter_dialog_kpe.open = False
      self.page.update()



#TODO: SUMMARY TABLE
#! THIS TABLE DOESN'T WORK
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
          actual_quater_value = "1-й квартал"
      elif quater == "2 квартал":
          quater_column = "2nd_quater_value"
          weight_column = "KPE_weight_2"
          actual_quater_value = "2-й квартал"
      elif quater == "3 квартал":
          quater_column = "3rd_quater_value"
          weight_column = "KPE_weight_3"
          actual_quater_value = "3-й квартал"
      else:
          quater_column = "4th_quater_value"
          weight_column = "KPE_weight_4"
          actual_quater_value = "4-й квартал"
      
      if self.report_depart.content.value == "Все управления":
        query = f"""
                SELECT
                    ROW_NUMBER() OVER () AS `порядковый номер`,
                    'агентство по труду и занятости населения Сахалинской области' AS `Наименование структурного подразделения Правительства Сахалинской области, государственного органа или органа исполнительной власти Сахалинской области`,
                    nd.name AS `Наименование структурного подразделения органа исполнительной власти Сахалинской области`,
                    s.position AS `Должность`,
                    s.full_name AS `ФИО`,
                    SUM( (kt.`{weight_column}` / 100) * ( (av.value * 100) / NULLIF(kt.`{quater_column}`, 0)
                        )
                    ) AS `Процент выполнения`
                FROM kpe_table AS kt
                    INNER JOIN specialists AS s ON kt.kpe_user_id = s.specialist_id
                    INNER JOIN name_of_department AS nd ON s.specialist_department_id = nd.department_id
                    INNER JOIN actual_value AS av ON kt.kpe_user_id = av.actual_users_id AND kt.kpe_indicators_id = av.actual_indicators_id
                WHERE
                    kt.number_of_version = '{latest_version}'
                    AND av.quarter_number = '{actual_quater_value}'
                    AND kt.status = 'Активно'
                GROUP BY
                    `Наименование структурного подразделения Правительства Сахалинской области, государственного органа или органа исполнительной власти Сахалинской области`,
                    `Наименование структурного подразделения органа исполнительной власти Сахалинской области`,
                    `Должность`,
                    `ФИО`
            """
      else:
        query_select_dep_id = "SELECT department_id FROM name_of_department WHERE name = '{}'".format(self.report_depart.content.value)
        cursor.execute(query_select_dep_id)
        department_id = cursor.fetchone()[0]
        
        query = f"""
                SELECT
                    ROW_NUMBER() OVER () AS `порядковый номер`,
                    'агентство по труду и занятости населения Сахалинской области' AS `Наименование структурного подразделения Правительства Сахалинской области, государственного органа или органа исполнительной власти Сахалинской области`,
                    nd.name AS `Наименование структурного подразделения органа исполнительной власти Сахалинской области`,
                    s.position AS `Должность`,
                    s.full_name AS `ФИО`,
                    SUM( (kt.`{weight_column}` / 100) * ( (av.value * 100) / NULLIF(kt.`{quater_column}`, 0)
                        )
                    ) AS `Процент выполнения`
                FROM kpe_table AS kt
                    INNER JOIN specialists AS s ON kt.kpe_user_id = s.specialist_id
                    INNER JOIN name_of_department AS nd ON s.specialist_department_id = nd.department_id
                    INNER JOIN actual_value AS av ON kt.kpe_user_id = av.actual_users_id AND kt.kpe_indicators_id = av.actual_indicators_id
                WHERE
                    kt.number_of_version = '{latest_version}'
                    AND s.specialist_department_id = {department_id}
                    AND av.quarter_number = '{actual_quater_value}'
                    AND kt.status = 'Активно'
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
        global results
      
        cursor = connection.cursor()
        
        cursor.execute(f"""
        SELECT sp.position, di.name
        FROM specialists AS sp
            INNER JOIN name_of_department AS di ON di.department_id = sp.specialist_department_id
        WHERE sp.full_name = '{str(self.report_spec.content.value)}'
        """)
        potition_name_dep = cursor.fetchone()
        print(potition_name_dep)
        print(potition_name_dep[0])
        print(potition_name_dep[1])
      
      
        print(results)
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        headers = ["п/п", "Наименование показателя", "Ед.изм.", "1 кв.", "2 кв.", "3 кв.", "4 кв.", "год", "Вес КПЭ 1 кв.", "Вес КПЭ 2 кв.", "Вес КПЭ 3 кв.", "Вес КПЭ 4 кв."]

        for col, header in enumerate(headers, start=1):
            sheet.cell(row=8, column=col).value = header

        # Merge cells D1 to I1 and add the specified phrase
        sheet.merge_cells('D1:I1')
        merged_cell = sheet['D1']
        merged_cell.alignment = Alignment(horizontal='center', vertical='center')  # Center the text

        # Set the value for one of the constituent cells
        sheet['D1'].value = "УТВЕРЖДАЮ\nРуководитель агентства по труду и занятости населения Сахалинской области"
        sheet.row_dimensions[1].height = 40
        sheet['D1'].alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

        # Repeat this pattern for other merged cells
        sheet.merge_cells('D2:I2')
        sheet['D2'].value = "______________Т.Г. Бабич"
        sheet['D2'].alignment = Alignment(horizontal='center', vertical='center')

        sheet.merge_cells('D3:I3')
        sheet['D3'].value = '"__" _________20__ года'
        sheet['D3'].alignment = Alignment(horizontal='center', vertical='center')

        long_text = (
            "КАРТА КЛЮЧЕВЫХ ПОКАЗАТЕЛЕЙ ЭФФЕКТИВНОСТИ ПРОФЕССИОНАЛЬНОЙ СЛУЖЕБНОЙ ДЕЯТЕЛЬНОСТИ "
            "ГОСУДАРСТВЕННОГО ГРАЖДАНСКОГО СЛУЖАЩЕГО САХАЛИНСКОЙ ОБЛАСТИ"
        )
        
        # Merge the cells for the long text
        sheet.merge_cells('A4:I4')
        
        # Set the value for the merged cell (only set in the top-left cell of the merged range)
        sheet['A4'].value = long_text
        sheet['A4'].font = Font(bold=True)
        sheet['A4'].alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')

        sheet.row_dimensions[4].height = 40  # Set the height for row 4 (2 cm)

        sheet.merge_cells('A5:I5')
        sheet['A5'].value = 'Агентство по труду и занятости населения Сахалинской области'
        sheet['A5'].font = Font(bold=True)
        sheet['A5'].alignment = Alignment(horizontal='center', vertical='center')

        sheet.merge_cells('A6:I6')
        sheet['A6'].value = f'Карта КПЭ на 2023 год {str(potition_name_dep[0]).lower()}a {str(potition_name_dep[1]).lower()} {str(self.report_spec.content.value)}'
        sheet['A6'].font = Font(bold=True)
        sheet['A6'].alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')

        sheet.row_dimensions[6].height = 40  # Set the height for row 6 (2 cm)

        for i, row_data in enumerate(results, start=9):  # Start the data from row 9
            for col, value in enumerate(row_data, start=1):
                sheet.cell(row=i, column=col).value = value

        sheet.column_dimensions["B"].width = 20  # Adjust the width of column "B"
        sheet['B8'].font = Font(bold=True)  # Set "Наименование показателя" as bold

        # Set alignment for the entire sheet
        # for row in sheet.iter_rows(min_row=1, max_col=sheet.max_column, max_row=sheet.max_row):
        #     for cell in row:
        #         cell.alignment = Alignment(horizontal='center', vertical='center')
        last_row = sheet.max_row + 2
        print(potition_name_dep[0])
        print(potition_name_dep[1])
        sheet.cell(row=last_row, column=1).value = "{} {} _______________________ {}".format(potition_name_dep[0], str(potition_name_dep[1]).lower(), self.report_spec.content.value)
        sheet.merge_cells(f'A{last_row}:I{last_row}')  # Merge the cells for the record
        sheet.row_dimensions[last_row].height = 40  # Set the height for the new row (2 cm)

        filename = "D:/tniki/Desktop/output1.xlsx"
        print(filename)

        if filename:
            workbook.save(filename)

        self.show_success_dialog()
