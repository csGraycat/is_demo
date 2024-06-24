from django.urls import path, include

from crmfields.views.reload import reload_start
from .import_table_to_bitrix.views.table_to_bitrix_view import table_to_bitrix
from .field_sort.views.field_sort_view import field_sort
from .openai_voice_recognition.views.openai_voice_recognition_view import open_ai_get_text
from . import send_msg_tg_bot


urlpatterns = [
    path('table_to_bitrix/', table_to_bitrix, name='table_to_bitrix'),
    path('field_sort/', field_sort, name='field_sort'),
    path('openai_voice_recognition/', open_ai_get_text, name='open_ai_get_text'),
    path('send_msg_tg_bot/', include('intern.send_msg_tg_bot.urls')),
    path('', reload_start, name='reload_start'),
]
