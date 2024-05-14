from flet import *
from utils.consts import primary_colors
from service.connection import *
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart


class Monitoring(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.theme_mode = ThemeMode.LIGHT
        self.alignment = alignment.center
        self.expand = True
        self.bgcolor = primary_colors['GREEN']
        self.pie_chart = MatplotlibChart()
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
                                      on_click=lambda x: x == self.page.go('/home')
                                  )
                                ),
                                Container(
                                  width=70,
                                  height=70,
                                ),
                              ]
                            )
                          ),
                          Container(
                            content=Text(
                            value='Мониторинг',
                            size=18,
                            color=primary_colors['WHITE'],
                            text_align='center',
                            ),
                          ),
                          Container(width=200),
                        ]
                      )
                    )
                  ],
              )
            ),
            Container(
              expand=True,
              bgcolor=primary_colors['WHITE'],
              content=Column(
                expand=True,
                controls=[
                  #! First Row
                  Container(height=50),
                  Container(
                    Row(
                      spacing='50',
                      alignment='center',
                      controls=[
                        
                      ]
                    )
                  ),
                  #! Second Row
                  Container(
                    content=Column(
                      controls=[
                        Container(
                          Text(
                            value="Количество специалистов, которые не заполнили карту КПЭ по управлениям"
                          )
                        ),
                        Container(
                          self.pie_chart
                        ),
                      ]
                    )
                  ),
                ],
              )
            ),
          ]
        )
        self.create_diagrams()
    def create_pie_chart(self, departments):
      # Создание фигуры и оси для диаграммы
      fig, ax = plt.subplots(figsize=(30,20))

      # Названия и значения для секторов диаграммы
      self.labels = list(departments.keys())
      sizes = list(departments.values())

      # Создание круговой диаграммы
      patches, texts, autotexts = ax.pie(sizes, labels=self.labels, startangle=90, autopct=lambda p: '{:.0f}'.format(p * sum(sizes) / 100))

      # Для круглой диаграммы
      ax.axis('equal')

      # Возвращение фигуры для использования в MatplotlibChart
      return fig
    def create_diagrams(self):
      cursor = connection.cursor()
      query_not_in_kpe_table = """
      SELECT 
          nd.name AS department_name,
          s.full_name AS specialist_name
      FROM 
          specialists s
      JOIN 
          name_of_department nd ON s.specialist_department_id = nd.department_id
      WHERE 
          s.specialist_id NOT IN (
              SELECT 
                  kt.kpe_specialist_id
              FROM 
                  kpe_table kt
              WHERE 
                  toYear(kt.date) = toYear(now()) AND
                  toQuarter(kt.date) = toQuarter(now())
          )
      GROUP BY 
          nd.name,
          s.specialist_id,
          s.full_name
      ORDER BY 
          nd.name,
          s.full_name;
      """
      cursor.execute(query_not_in_kpe_table)
      result = cursor.fetchall()
      departments = {}

      for department, specialist in result:
          if department in departments:
              departments[department] += 1
          else:
              departments[department] = 1

      # Создание круговой диаграммы с данными
      pie_chart_figure = self.create_pie_chart(departments)

      # Добавление MatplotlibChart в интерфейс
      
      self.pie_chart.figure = pie_chart_figure
      self.page.update()

      # Добавление обработчика кликов по секторам диаграммы
      def on_sector_click(event, pie_chart=self.pie_chart, departments=departments):
          # Получение индекса сектора, на который нажали
          hit, ind = pie_chart.figure.gca().contains(event)
          if hit:
              department = self.labels[ind['ind'][0]]
              print(f"Вы выбрали управление: {department}")

      # Связывание события клика с функцией on_sector_click
      self.pie_chart.figure.canvas.mpl_connect('button_press_event', on_sector_click)