from flet import *
from utils.colors import *
from service.connection import *

class Login(Container):
    def __init__(self, page: Page):
        super().__init__()
        
        self.alignment = alignment.center
        self.expand = True
        self.bgcolor = "#5B7553"
#*USER_ID VALUE CONTAINER
        self.took_user_id = 0
        

#*login container
        self.login_box = Container(
            content=TextField(
                # border=InputBorder.NONE, #this thing is turned off boreders
                content_padding=padding.only(top=0, bottom=0, right=20, left=20),
                hint_style=TextStyle(
                  size=12, color='#858796'
                ),
                label='Логин',
                cursor_color='#858796',
                text_style=TextStyle(
                  size=14,
                  color='black',
                )
            ),
                # border=border.all(width=1, color='#bdcbf4'), #this is opposite to the up function, turn on borders
                # border_radius=30 #сглаживание краёв
                # on_click=lambda x: x == self.page.go('/login')
        )
#*password container
        self.password_box = Container(
            content=TextField(
                # border=InputBorder.NONE, #this thing is turned off boreders
                content_padding=padding.only(top=0, bottom=0, right=20, left=20),
                hint_style=TextStyle(
                  size=12, color='#858796'
                ),
                label='Пароль',
                cursor_color='#858796',
                text_style=TextStyle(
                  size=14,
                  color='black',
                ),
                password=True,
                can_reveal_password=True,
            ),
                # border=border.all(width=1, color='#bdcbf4'), #this is opposite to the up function, turn on borders
                # border_radius=30 #сглаживание краёв
        )
#*button container
        self.error_box =  Container(
            alignment=alignment.center,
            content=Text(
              value='',
              color='#FF0000'
            ),
            
        )
#*center of the form container
        self.content = Column(
          alignment='center',
          horizontal_alignment='center',
          controls=[
            Container(
              width=500,
              padding=40,
              bgcolor=white,
              border_radius=15,
              content=Column(
                horizontal_alignment='center',
                controls=[
                  Text(
                    value='Название сайта',
                    size=18,
                    color='black',
                    text_align='center',
                  ),
                  self.login_box,
                  self.password_box,
                  Container(height=0),
                  Container(
                    alignment=alignment.center,
                    bgcolor='#5B7553',
                    height=40,
                    border_radius=30,
                    content=Text(
                      value='Войти'
                    ),
                    on_click=self.login
                  ),
                  self.error_box,
                  
                  # TextField(label="Логин", width=500,color='black'),
                  # TextField(label="Пароль", password=True, can_reveal_password=True, width=500),
                  # ElevatedButton(text='Войти', color='white', width=200, height=50)
                ]
              )
            )
          ]
        )
    
    def login(self, e):
      #*CONNECTION TO THE CLICKHOUSE DB
      cursor = connection.cursor()
      # query_select = 'SELECT plan_indicators_id, number_of_version FROM planned_value';
      # query_select = 'SELECT name FROM name_of_indicators;'
      # query_select = 'DESCRIBE TABLE planned_value;'
      query_select = 'SELECT user_id, login, password FROM users;'
      # query_select = 'TRUNCATE planned_value;'

      
      cursor.execute(query_select)
      results= cursor.fetchall()
      for row in results:
        if self.login_box.content.value == row[1] and self.password_box.content.value == row[2]:
          self.page.go(
            '/home'
          )
          self.took_user_id  = row[0]
          # print(self.took_user_id)
          # print(results)
        else:
          self.error_box.content.value = 'Вы ввели неверный логин или пароль!'
          self.page.update()