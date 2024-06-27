from django.urls import path

from .models.robot_vacancies_model import VacanciesRobot
from .views.install import install
from .views.robot_vacancies_view import robot_vacancies
from .views.uninstall import uninstall

app_name = 'bitrix_robot_vacancies'

urlpatterns = [
    path('home/', robot_vacancies, name='robot_vacancies_home'),
    path('install/', install, name='install_robot'),
    path('uninstall/', uninstall, name='uninstall_robot'),
    path('handler/', VacanciesRobot.as_view(), name='handler_robot'),
]
