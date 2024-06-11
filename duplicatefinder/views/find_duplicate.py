from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from collections import Counter


@main_auth(on_cookies=True)
def find_entity_duplicates(request):
    """Собирает список дубликатов из сущности, выбранной в select_entity"""
    but = request.bitrix_user_token
    lst = []
    if request.method == 'POST':
        selected_entity = request.POST.get('entity')
        res = but.call_list_method(f'crm.{selected_entity}.list')
        for i in res:
            if selected_entity == 'contact':
                full_name = i['NAME'] + f' {i['SECOND_NAME']}' + f' {i['LAST_NAME']}'
                lst.append(full_name)
            else:
                lst.append(i['TITLE'])
        res = {name: count for name, count in Counter(lst).items() if count > 1}
        return render(request, 'duplicates.html', context={'res': res})
    return render(request, 'select_entity.html')
