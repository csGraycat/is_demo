from django.urls import path

from crmfields.views.reload import reload_start
from .import_table_to_bitrix.views.table_to_bitrix_view import table_to_bitrix
from .field_sort.views.field_sort_view import field_sort

urlpatterns = [
    path('table_to_bitrix/', table_to_bitrix, name='table_to_bitrix'),
    path('field_sort/', field_sort, name='field_sort'),
    path('', reload_start, name='reload_start'),
]
