from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from django.http import HttpResponse


@main_auth(on_cookies=True)
def select_user(request):
    but = request.bitrix_user_token
    user_id = None
    if request.method == 'POST':
        user_id = request.POST.get('user')
        user_info = but.call_api_method('user.get', {"ID": user_id})['result'][0]

        return render(request, 'output.html', locals())
    return render(request, 'select_user_template.html')
