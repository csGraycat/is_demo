from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from django.shortcuts import render
from intern.field_sort.utils.utils import sort_enumerated_field


@main_auth(on_cookies=True)
def field_sort(request):
    but = request.bitrix_user_token
    field_name = ''
    if request.method == 'POST':
        field_link = request.POST.get('link')
        for i in field_link.split('/'):
            if i.startswith('UF_CRM_'):
                field_name = i

        # handle invalid links
        if field_name == '':
            return render(request, 'choose_field_to_sort.html')

        try:
            res = but.call_list_method('crm.company.userfield.list', {'FILTER': {'FIELD_NAME': field_name}})[0]
        except IndexError:
            return render(request, 'choose_field_to_sort.html')

        field_id = res['ID']
        field_list = res['LIST']
        sorted_list = sort_enumerated_field(field_list)
        but.call_list_method('crm.company.userfield.update', {'ID': field_id, 'fields': {'LIST': sorted_list}})

        return render(request, 'field_sorted.html')

    return render(request, 'choose_field_to_sort.html')
