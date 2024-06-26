from django.http import HttpResponse
from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from calls_to_telegram.utils.main_utils import export_calls_to_telegram


@main_auth(on_cookies=True)
def export_all_calls(request):
    pass
