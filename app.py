from flet import *

from pages.add_kpe.actual import Actual
from pages.add_kpe.card import Card
from pages.add_kpe.edit_kpe import EditKPE
from pages.add_kpe.scheduled import Scheduled
from pages.handbook.add import Add
from pages.handbook.department import Department
from pages.handbook.handbook import Handbook
from pages.handbook.measurement_handbook import MeasurementHandbook
from pages.handbook.scheduled_view import ScheduledView
from pages.handbook.specialists_handbook import SpecialistsHandbook
from pages.handbook.users import Users
from pages.home import Home
from pages.login import Login
from pages.report import Report
from pages.settings.monitoring import Monitoring
from pages.settings.settings import Settings


class Main(UserControl):
    def __init__(self, page: Page, ):
        super().__init__()
        self.page = page
        self.init_helper()

    def init_helper(self, ):
        self.page.on_route_change = self.on_route_change
        self.page.go('/home')

    def on_route_change(self, route):
        new_page = {
            "/home": Home,
            "/login": Login,
            "/card": Card,
            "/scheduled": Scheduled,
            "/actual": Actual,
            "/handbook": Handbook,
            "/add": Add,
            "/report": Report,
            "/settings": Settings,
            "/monitoring": Monitoring,
            "/measurement_handbook": MeasurementHandbook,
            "/specialists_handbook": SpecialistsHandbook,
            "/scheduled_handbook": ScheduledView,
            "/department": Department,
            "/users": Users,
            "/edit_kpe": EditKPE,
        }[self.page.route](self.page)

        self.page.views.clear()
        self.page.views.append(
            View(route, [new_page])
        )


# app(target=Main, assets_dir='assets')
app(target=Main, assets_dir='assets', view=WEB_BROWSER)
