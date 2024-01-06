import openpyxl
from flet import *
from openpyxl.styles import Font, Alignment, DEFAULT_FONT, Border, Side
from service.connection import *
from utils.colors import *


class Report(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.theme_mode = ThemeMode.LIGHT
        self.alignment = alignment.center
        self.expand = True
        self.bgcolor = tea_green

        dropdown_options_specialists = []
        dropdown_options_departments = []
        # *SELECT QUERY TO DISPLAY SPECIALISTS FROM DB
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT full_name FROM specialists ORDER BY specialist_id')
            results = cursor.fetchall()

            for row in results:
                dropdown_options_specialists.append(dropdown.Option(row[0]))
        except Exception as e:
            print(f"Error fetching data from the database: {str(e)}")

        # *SELECT QUERY TO DISPLAY SPECIALISTS FROM DB
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT name FROM name_of_department ORDER BY department_id')
            results = cursor.fetchall()

            for row in results:
                dropdown_options_departments.append(dropdown.Option(row[0]))
            dropdown_options_departments.append(dropdown.Option("Все управления"))

        except Exception as e:
            print(f"Error fetching data from the database: {str(e)}")

        # * DROPDOWN LISTS
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
        # *TEXT
        self.number_of_version_kpe = Container(
            Text(
                value=""
            )
        )

        # *ALTER DIALOG
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

        # !UI
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

                # manual buttons
                Container(
                    expand=True,
                    bgcolor='white',
                    content=Column(
                        expand=True,
                        # alignment='center',
                        horizontal_alignment='center',
                        controls=[
                            # 1st row
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
                            # 2nd row
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

    # !FUCNTIONS
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

    # TODO: FOR Premium calculation
    def open_dialog(self):
        self.page.dialog = self.alter_dialog
        self.alter_dialog.open = True
        self.page.update()

    def alter_dialog_select_columns_data(self, e):
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT specialist_id FROM specialists WHERE full_name='{str(self.report_spec.content.value)}';")
        user_id = cursor.fetchone()[0]

        # cursor.execute()

        query_select_kpe = f'SELECT MAX(number_of_version) FROM kpe_table WHERE kpe_user_id = {user_id}'# AND kpe_indicators_id = {}
        cursor.execute(query_select_kpe)
        latest_version = cursor.fetchone()[0]

        query_select_actual = f'SELECT MAX(number_of_version) FROM actual_value WHERE actual_users_id = {user_id}'# AND kpe_indicators_id = {}
        cursor.execute(query_select_actual)
        latest_version_actual = cursor.fetchone()[0]

        print(latest_version_actual, latest_version)

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
          WHERE kt.kpe_user_id = {user_id} 
          AND kt.number_of_version = '{latest_version}'
          AND av.number_of_version = '{latest_version_actual}'
          AND av.actual_users_id = kt.kpe_user_id
          AND av.actual_indicators_id = kt.kpe_indicators_id
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
        global results_premi
        results_premi = cursor.fetchall()

        query_result = results_premi

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

    # TODO: FOR KPE TABLE
    def open_dialog_kpe(self):
        self.page.dialog = self.alter_dialog_kpe
        self.alter_dialog_kpe.open = True
        self.page.update()

    def select_kpe(self, e):
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT specialist_id FROM specialists WHERE full_name='{str(self.report_spec.content.value)}';")
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

    # TODO: SUMMARY TABLE
    # ! THIS TABLE DOESN'T WORK
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
        query_select_actual = f'SELECT MAX(number_of_version) FROM actual_value'
        cursor.execute(query_select_actual)
        latest_version_actual = cursor.fetchone()[0]

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
                    AND av.number_of_version = '{latest_version_actual}'
                    AND kt.status = 'Активно'
                GROUP BY
                    `Наименование структурного подразделения Правительства Сахалинской области, государственного органа или органа исполнительной власти Сахалинской области`,
                    `Наименование структурного подразделения органа исполнительной власти Сахалинской области`,
                    `Должность`,
                    `ФИО`
            """
        else:
            query_select_dep_id = "SELECT department_id FROM name_of_department WHERE name = '{}'".format(
                self.report_depart.content.value)
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
                    AND av.number_of_version = '{latest_version_actual}'
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
        global results_summary
        results_summary = cursor.fetchall()
        print(results_summary)

        query_result = results_summary

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
        # * РАСЧЕТ ПРЕМИИ
        elif selected_report_type == "Расчет премии":
            self.open_dialog()
        # *СВОДНЫЕ ДАННЫЕ ПО ИСПОЛНЕНИЮ
        elif selected_report_type == "Сводные данные по исполнению":
            self.open_dialog_summary()
        else:
            print("Вы не выбрали шаблон отчета")

    def export_report_to_excel(self, e):
        global results
        global results_summary
        global results_premi
        selected_report_type = self.report_template.content.value
        if selected_report_type == "Карта КПЭ":
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
            DEFAULT_FONT.name = 'Times New Roman'
            sheet = workbook.active
            headers = ["п/п", "Наименование показателя", "Ед.изм.", "1 кв.", "2 кв.", "3 кв.", "4 кв.", "год",
                      "Вес КПЭ 1 кв.", "Вес КПЭ 2 кв.", "Вес КПЭ 3 кв.", "Вес КПЭ 4 кв."]

            sheet.column_dimensions["B"].width = 50
            sheet.column_dimensions["C"].width = 15
            sheet.column_dimensions["D"].width = 15
            sheet.column_dimensions["E"].width = 15
            sheet.column_dimensions["F"].width = 15
            sheet.column_dimensions["G"].width = 15
            sheet.column_dimensions["I"].width = 15
            sheet.column_dimensions["J"].width = 15
            sheet.column_dimensions["K"].width = 15
            sheet.column_dimensions["L"].width = 15
            
            sheet.row_dimensions[8].height = 30
            
            for col, header in enumerate(headers, start=1):
                sheet.cell(row=8, column=col).value = header
                cell = sheet.cell(row=8, column=col)
                cell.border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
                
                
            wrap_text_cells = ['A8', 'B8', 'C8', 'D8', 'E8', 'F8','G8','H8','I8','J8','K8','L8']
            for cell in wrap_text_cells:
                sheet[cell].alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')
                sheet[cell].font = Font(size=11)

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
                  cell = sheet.cell(row=i, column=col)
                  sheet.cell(row=i, column=col).value = value
                  sheet.cell(row=i, column=col).alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')
                  cell.border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
                sheet.row_dimensions[i].height = 75
                    
            sheet['B8'].font = Font(bold=True)  # Set "Наименование показателя" as bold

            # Set alignment for the entire sheet
            last_row = sheet.max_row + 2
            print(potition_name_dep[0])
            print(potition_name_dep[1])
            sheet.cell(row=last_row, column=1).value = "{} {} _______________________ {}".format(potition_name_dep[0], str(
                potition_name_dep[1]).lower(), self.report_spec.content.value)
            sheet.merge_cells(f'A{last_row}:I{last_row}')  # Merge the cells for the record
            sheet.row_dimensions[last_row].height = 40  # Set the height for the new row (2 cm)

            filename = "E:/tniki/Desktop/карта_кпэ.xlsx"
            print(filename)

            if filename:
                workbook.save(filename)

            self.show_success_dialog()
        
        
# * РАСЧЕТ ПРЕМИИ
        elif selected_report_type == "Расчет премии":
            workbook = openpyxl.Workbook()
            DEFAULT_FONT.name = 'Times New Roman'
            sheet = workbook.active
            headers = ["№ пп.", 
                      "Наименование показателя",
                      "Единица измерения или срок",
                      "План",
                      "Факт",
                      "Вес КПЭ, %",
                      "Доля премии по факту выполнения показателя*",
                      ]

            for col, header in enumerate(headers, start=1):
                sheet.cell(row=18, column=col).value = header
                cell = sheet.cell(row=18, column=col)
                cell.border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
    

            #Columns width
            # sheet.column_dimensions["A"].width = 25
            sheet.column_dimensions["B"].width = 45
            sheet.column_dimensions["C"].width = 15
            sheet.column_dimensions["D"].width = 35
            sheet.column_dimensions["E"].width = 15
            sheet.column_dimensions["F"].width = 25
            sheet.column_dimensions["G"].width = 25
            
            #Rows height
            sheet.row_dimensions[2].height = 80
            sheet.row_dimensions[6].height = 80
            sheet.row_dimensions[18].height = 50
            
            wrap_text_cells = ['A18', 'B18', 'C18', 'D18', 'E18', 'F18','G18']
            for cell in wrap_text_cells:
                sheet[cell].alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')
                sheet[cell].font = Font(size=11)
            # Merge cells D1 to I1 and add the specified phrase
            sheet.merge_cells('E1:G1')
            sheet['E1'].value = 'ПРИЛОЖЕНИЕ'
            sheet['E1'].alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            sheet['E1'].font = Font(size=10)
            
            sheet.merge_cells('E2:G2')
            sheet['E2'].value = 'к распоряжению агентства по труду и занятости населения Сахалинской области «О внесении изменений в Положение о порядке осуществления дополнительных выплат государственным гражданским служащим агентства по труду и занятости населения Сахалинской области, утвержденное распоряжением агентства по труду и занятости населения Сахалинской области от 15.09.2022 № 458-р»'
            sheet['E2'].alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            sheet['E2'].font = Font(size=10)
            
            sheet.merge_cells('E3:G3')
            sheet['E3'].value = 'от ________________ № _______		'
            sheet['E3'].alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            sheet['E3'].font = Font(size=10)
            
            sheet.merge_cells('E5:G5')
            sheet['E5'].value = 'ПРИЛОЖЕНИЕ'
            sheet['E5'].alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            sheet['E5'].font = Font(size=10)
            
            sheet.merge_cells('E6:G6')
            sheet['E6'].value = 'к Положению о порядке осуществления дополнительных выплат государственным гражданским служащим агентства по труду и занятости населения Сахалинской области, утвержденному распоряжением агентства по труду и занятости населения Сахалинской области от 15.09.2022 № 458-р'
            sheet['E6'].alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            sheet['E6'].font = Font(size=10)
            
            sheet.merge_cells('B8:F8')
            sheet['B8'].value = 'Расчет коэффициента выполнения'
            sheet['B8'].alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            sheet['B8'].font = Font(bold=True, size=13)
            
            sheet.merge_cells('B9:F9')
            sheet['B9'].value = 'ключевых показателей эффективности				'
            sheet['B9'].alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            sheet['B9'].font = Font(bold=True, size=13)
            
            sheet.merge_cells('B10:F10')
            sheet['B10'].value = 'профессиональной служебной деятельности'
            sheet['B10'].alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            sheet['B10'].font = Font(bold=True, size=13)
            
            sheet.merge_cells('B11:F11')
            sheet['B11'].value = 'по итогам работы за ____________ квартал'
            sheet['B11'].alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            sheet['B11'].font = Font(bold=True, size=13)
            
            sheet.merge_cells('B13:F13')
            sheet['B13'].value = '_______________________________'
            sheet['B13'].alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            sheet['B13'].font = Font(bold=True, size=14)
            
            sheet.merge_cells('B14:F14')
            sheet['B14'].value = '(должность, ФИО гражданского служащего)'
            sheet['B14'].alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            sheet['B14'].font = Font(bold=True, size=8)
            
            sheet.merge_cells('B15:F15')
            sheet['B15'].value = '_____________________________________________________'
            sheet['B15'].alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            sheet['B15'].font = Font(bold=True, size=14)
            
            sheet.merge_cells('B16:F16')
            sheet['B16'].value = '(наименование управления)'
            sheet['B16'].alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            sheet['B16'].font = Font(bold=True, size=8)
            
            for col in range(1, 8):
              sheet.cell(row=19, column=col).value = col
              sheet.cell(row=19, column=col).alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
              cell = sheet.cell(row=19, column=col)
              cell.border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
            
            # цикл для заполнения таблицы
            for i, row_data in enumerate(results_premi, start=20):  # Start the data from row 9
                for col, value in enumerate(row_data, start=1):
                  cell = sheet.cell(row=i, column=col)
                  sheet.cell(row=i, column=col).value = value
                  sheet.cell(row=i, column=col).alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')
                  cell.border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
                sheet.row_dimensions[i].height = 75
            
            # текст расположенный снизу таблицы
            last_row = sheet.max_row
            sheet.cell(row=last_row+1, column=2).value = "Коэффициент выполнения КПЭ:"
            sheet.cell(row=last_row+1, column=2).alignment = Alignment(wrap_text=True)
            sheet.row_dimensions[last_row+1].height = 25
            
            for col in range(1, 8):
              cell = sheet.cell(row=last_row+1, column=col)
              cell.border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
            
            sheet.cell(row=last_row+3, column=1).value = "_____________________________________"
            sheet.merge_cells(f'A{last_row+3}:C{last_row+3}')
            
            sheet.cell(row=last_row+3, column=7).value = "_______________"
            sheet.merge_cells(f'A{last_row+3}:C{last_row+3}')
            
            sheet.cell(row=last_row+4, column=1).value = "_________________________"
            sheet.merge_cells(f'A{last_row+4}:B{last_row+4}')
            
            sheet.cell(row=last_row+5, column=1).value = "(должность непосредственного руководителя гражданского служащего)"
            sheet.merge_cells(f'A{last_row+5}:C{last_row+5}')
            sheet.row_dimensions[last_row+5].height = 30
            sheet.cell(row=last_row+5, column=1).alignment = Alignment(wrap_text=True)
            
            sheet.cell(row=last_row+5, column=5).value = "(подпись)"
            
            sheet.cell(row=last_row+5, column=7).value = "(ФИО)"
            
            sheet.cell(row=last_row+7, column=1).value = "Ознакомлен:"
            sheet.merge_cells(f'A{last_row+7}:C{last_row+7}')
            
            sheet.cell(row=last_row+8, column=1).value = "____________________________________"
            sheet.merge_cells(f'A{last_row+7}:C{last_row+7}')
            
            sheet.cell(row=last_row+8, column=7).value = "___________________"
            
            sheet.cell(row=last_row+9, column=4).value = "(подпись)"
            
            sheet.cell(row=last_row+9, column=6).value = "(ФИО гражданского служащего)"
            sheet.cell(row=last_row+9, column=6).alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')
            sheet.merge_cells(f'F{last_row+9}:G{last_row+9}')
            
            sheet.cell(row=last_row+10, column=1).value = "Согласовано:"
            sheet.merge_cells(f'A{last_row+10}:C{last_row+10}')
            
            sheet.cell(row=last_row+11, column=1).value = "____________________________________"
            sheet.merge_cells(f'A{last_row+11}:C{last_row+11}')
            
            sheet.cell(row=last_row+12, column=7).value = "___________________"
            
            sheet.cell(row=last_row+13, column=4).value = "(подпись)"
            
            sheet.cell(row=last_row+13, column=6).value = "(ФИО курирующего заместителя руководителя агентства)"
            sheet.cell(row=last_row+13, column=6).alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')
            sheet.row_dimensions[last_row+13].height = 30
            sheet.merge_cells(f'F{last_row+13}:G{last_row+13}')
            
            sheet.cell(row=last_row+15, column=1).value = "_____________________________________________________________"
            sheet.merge_cells(f'A{last_row+15}:D{last_row+15}')
            
            sheet.cell(row=last_row+16, column=2).value = "* - Гр. 7 = гр. 6/100 – если установленный показатель выполнен в полном объеме или перевыполнен.				"
            sheet.merge_cells(f'B{last_row+16}:F{last_row+16}')
            
            sheet.cell(row=last_row+17, column=2).value = "- Гр. 7 = 0 – если установленный показатель не выполнен или выполнен не в полном объеме.»				"
            sheet.merge_cells(f'B{last_row+17}:F{last_row+17}')

            filename = "E:/tniki/Desktop/расчет_премии.xlsx"
            print(filename)

            if filename:
                workbook.save(filename)

            self.show_success_dialog()
# *СВОДНЫЕ ДАННЫЕ ПО ИСПОЛНЕНИЮ
        elif selected_report_type == "Сводные данные по исполнению":
            workbook = openpyxl.Workbook()
            DEFAULT_FONT.name = 'Times New Roman'
            sheet = workbook.active
            headers = ["№ п/п", 
                      "Наименование структурного подразделения Правительства Сахалинской области, государственного органа или органа исполнительной власти Сахалинской области",
                      "Наименование структурного подразделения органа исполнительной власти Сахалинской области",
                      "Должность",
                      "ФИО",
                      "Процент выполнения КПЭ по итогам отчетного периода, %"
                      ]

            for col, header in enumerate(headers, start=1):
                sheet.cell(row=3, column=col).value = header
                cell = sheet.cell(row=3, column=col)
                cell.border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

            #Columns width
            sheet.column_dimensions["A"].width = 25
            sheet.column_dimensions["B"].width = 25
            sheet.column_dimensions["C"].width = 25
            sheet.column_dimensions["D"].width = 25
            sheet.column_dimensions["E"].width = 25
            sheet.column_dimensions["F"].width = 25
            
            #Rows height
            sheet.row_dimensions[1].height = 34
            sheet.row_dimensions[2].height = 68
            sheet.row_dimensions[3].height = 108
            
            wrap_text_cells = ['A3', 'B3', 'C3', 'D3', 'E3', 'F3']
            for cell in wrap_text_cells:
                sheet[cell].alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')
            # Merge cells D1 to I1 and add the specified phrase
            sheet.merge_cells('D1:F1')
            merged_cell = sheet['D1']
            merged_cell.alignment = Alignment(horizontal='center', vertical='center')  # Center the text

            # Set the value for one of the constituent cells
            sheet['D1'].value = 'Приложение №4 к распоряжению министерства государственного управления Сахалинской области\n от "__"___________20____ года № __________ '
            
            sheet['D1'].alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

            # Merge the cells for the long text
            sheet.merge_cells('A2:F2')

            # Set the value for the merged cell (only set in the top-left cell of the merged range)
            sheet['A2'].value = f"РЕКОМЕНДУЕМАЯ ФОРМА СВЕДЕНИЙ О ВЫПОЛНЕНИИ КЛЮЧЕВЫХ ПОКАЗАТЕЛЕЙ ЭФФЕКТИВНОСТИ ПРОФЕССИОНАЛЬНОЙ СЛУЖЕБНОЙ ДЕЯТЕЛЬНОСТИ ГОСУДАРСТВЕННЫХ ГРАЖДАНСКИХ СЛУЖАЩИХ САХАЛИНСКОЙ ОБЛАСТИ\nза ___{self.report_quater.content.value}____ 20____г.\n(отчетный период)"
            sheet['A2'].font = Font(bold=True)
            sheet['A2'].alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')

            for col in range(1, 7):
              sheet.cell(row=4, column=col).value = col
              sheet.cell(row=4, column=col).font = Font(italic=True)
              sheet.cell(row=4, column=col).alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
              cell = sheet.cell(row=4, column=col)
              cell.border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
            
            for i, row_data in enumerate(results_summary, start=5):  # Start the data from row 9
                for col, value in enumerate(row_data, start=1):
                  cell = sheet.cell(row=i, column=col)
                  sheet.cell(row=i, column=col).value = value
                  sheet.cell(row=i, column=col).alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')
                  cell.border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
                sheet.row_dimensions[i].height = 34

              # Adjust the width of column "B"
            sheet['B8'].font = Font(bold=True)  # Set "Наименование показателя" as bold


            filename = "E:/tniki/Desktop/сводный_отчет.xlsx"
            print(filename)

            if filename:
                workbook.save(filename)

            self.show_success_dialog()
        else:
            print("Вы не выбрали шаблон отчет")
