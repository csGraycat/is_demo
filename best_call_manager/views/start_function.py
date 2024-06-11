from django.shortcuts import render

from best_call_manager.utils.datetime_utils import get_now_date
from best_call_manager.utils.setting_goals import setting_goals
from best_call_manager.utils.api_methods import *
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def start_find_all_call(request):
    """Позволяет получить все звонки, найти среди них подходящие по условию,
    и поставить пользователям задачу на выбор лучшего звонка за каждый день
    когда они были совершены, также пользователям в комментарии к задаче
    отправляется таблица с удобочитаемыми данными, чтобы пользователь смог
    проанализировать информацию и сделать выбор"""

    if request.method == "POST":
        but = request.bitrix_user_token
        now_date = get_now_date()  # получаем сегодняшнюю дату в iso-формате
        try:
            app_date = get_app_date(but)  # забираем дату из опций приложения (api.option.get)

            if app_date == now_date:  # случай если сегодня уже загружали
                return render(request, "best_call_manager_temp.html")
            else:  # если сегодня не загружали - получаем звонки от даты предыдущей загрузки до сегодняшней
                calls = get_new_calls(but, app_date, now_date)

        except (TypeError, KeyError):  # если никогда не загружали - возвращаем все звонки до сегодняшней даты (не включая)
            calls = get_old_calls(but, now_date)

        task_id_list, possible_calls = setting_goals(but, calls)

        app_possible_calls = but.call_api_method("app.option.get", {"option": "possible_calls"})["result"]
        if app_possible_calls and type(app_possible_calls) is dict:
            app_possible_calls.update(possible_calls)
        else:
            app_possible_calls = possible_calls

        app_tasks_id = but.call_list_method("app.option.get", {"option": "tasks"})
        if app_tasks_id and app_tasks_id[0] != '':
            app_tasks_id.extend(task_id_list)
        else:
            app_tasks_id = task_id_list

        set_app_tasks_id(but, app_tasks_id)
        but.call_api_method("app.option.set", {"options": {"possible_calls": app_possible_calls}})
        set_app_date(but, now_date)

    return render(request, "best_call_manager_temp.html")
