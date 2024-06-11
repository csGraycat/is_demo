import requests
from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from intern.import_table_to_bitrix.utils.upload_to_bitrix import upload_to_bitrix
from django.conf import settings
import os


@main_auth(on_cookies=True)
def table_to_bitrix(request):
    if request.method == 'POST':
        but = request.bitrix_user_token
        link = request.POST.get('link')
        export_link = link.split("/edit")[0] + "/export"
        res = requests.get(export_link).content
        temp_table = os.path.join(settings.BASE_DIR, 'temp.xlsx')
        with open(temp_table, 'wb') as t:
            t.write(res)
        object_count = upload_to_bitrix(temp_table, but)
        return render(request, 'entities_uploaded.html', locals())
    return render(request, 'enter_link.html')
