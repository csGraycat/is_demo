from django.shortcuts import render
from ..utils.search_manager import search_manager, find_supervisor, find_closest_supervisor
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def employee_list(request):
    but = request.bitrix_user_token
    user_dict, user_fields, departments_dict = search_manager(but)
    departments_str = []
    supervisor_department_dict = {}
    for dep_id, dep in departments_dict.items():
        dep.update({'INT_ID': int(dep_id)})
    if request.method == 'POST':
        chosen_user_id = request.POST.get('chosen_user_id')
        chosen_user = user_dict[chosen_user_id]
        chosen_user, departments_dict = find_closest_supervisor(chosen_user_id, chosen_user, departments_str, departments_dict)
        for dep_id, dep in departments_dict.items():
            if dep_id in chosen_user['UF_DEPARTMENT']:
                sup_id = dep['CLOSEST_SUPERVISOR']
                if sup_id == '':
                    supervisor_department_dict.update({dep['NAME']: 'Нет руководителя'})
                else:
                    supervisor_department_dict.update({dep['NAME']: user_dict[sup_id]['FULL_NAME']})
        return render(request, 'manager_list.html', context={'supers': supervisor_department_dict, 'departments': departments_dict, 'chosen_user': chosen_user})
    return render(request, 'list.html', context={'fields': user_fields, 'users': user_dict, 'departments': departments_dict})
