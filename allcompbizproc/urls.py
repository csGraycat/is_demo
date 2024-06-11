from django.urls import path

from allcompbizproc.views.runbizproc import run_bizproc, choose_bp
from crmfields.views.reload import reload_start

urlpatterns = [
    path('run_bizproc/', run_bizproc, name='run'),
    path('choose_bp/', choose_bp, name='choose_bp'),
    path('', reload_start, name='reload_start')
]
