from django.urls import path, include

from crmfields.views.reload import reload_start
from .import_table_to_bitrix.views.table_to_bitrix_view import table_to_bitrix
from .field_sort.views.field_sort_view import field_sort
from .openai_voice_recognition.views.openai_voice_recognition_view import open_ai_get_text
from . import send_msg_tg_bot
from .powerbi.powerbi_view import powerbi_export_deals
from .move_deadline.views.move_deadline_view import move_deadline_js
from .select_user.select_user_view import select_user


urlpatterns = [
    path('table_to_bitrix/', table_to_bitrix, name='table_to_bitrix'),
    path('field_sort/', field_sort, name='field_sort'),
    path('openai_voice_recognition/', open_ai_get_text, name='open_ai_get_text'),
    path('send_msg_tg_bot/', include('intern.send_msg_tg_bot.urls')),
    path('export_powerbi/', powerbi_export_deals, name='powerbi_export_deals'),
    path('robot/', include('intern.robot_vacancies.urls', namespace='bitrix_robot_vacancies')),
    path('move_deadline/', include('intern.move_deadline.urls')),
    path('select_user/', select_user, name='select_user_intern'),
    path('', reload_start, name='reload_start'),
]
