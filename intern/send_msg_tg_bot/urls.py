from django.urls import path

from .send_msg_tg_view import send_msg_tg, bot_info

urlpatterns = [
    path('send_msg_tg/', send_msg_tg, name='send_msg_tg'),
    path('bot_info/', bot_info, name='bot_info')
]
