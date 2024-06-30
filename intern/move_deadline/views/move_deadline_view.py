from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
import json
from integration_utils.bitrix24.models import BitrixUser
import datetime as dt

global TASK_ID


@main_auth(on_cookies=True)
def move_deadline_js(request):
    global TASK_ID
    TASK_ID = json.loads(request.POST['PLACEMENT_OPTIONS'])['taskId']
    context = {'task_id': TASK_ID}
    return render(request, 'move_deadline_template.html', context)


@main_auth(on_cookies=True)
def move_deadline(request):
    global TASK_ID
    context = {'task_id': TASK_ID}
    but = BitrixUser.objects.filter(is_admin=True,
                                    user_is_active=True).first().bitrix_user_token
    user_id = request.bitrix_user.bitrix_id
    task_user_id = but.call_api_method("tasks.task.get", {"taskId": TASK_ID,
                                                           "select": ["CREATED_BY"]})
    task_user_id = task_user_id['result']['task']['createdBy']
    if str(user_id) == task_user_id:
        date_info = but.call_api_method('tasks.task.get', {'taskId': TASK_ID, 'select': ['DEADLINE']})
        deadline = date_info['result']['task']['deadline']
        deadline = deadline.replace('T', ' ')
        deadline_dt = dt.datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S%z')
        new_deadline = deadline_dt + dt.timedelta(days=1)
        but.call_api_method("tasks.task.update", {"taskId": TASK_ID, "fields":
            {"DEADLINE": str(new_deadline)}})
    return render(request, 'move_deadline_template.html', context)
