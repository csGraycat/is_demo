from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
import json

@main_auth(on_cookies=True)
def company_on_map(request):
    but = request.bitrix_user_token
    comp_id = but.call_list_method('crm.company.list')
    address = but.call_list_method('crm.address.list')
    try:
        chosen_comp = json.loads(request.POST['PLACEMENT_OPTIONS'])['ID']
    except:
        pass
    return render(request, 'company_on_map_temp.html', locals())
