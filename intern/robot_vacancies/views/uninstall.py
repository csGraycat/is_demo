from django.http import HttpResponse

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from intern.robot_vacancies.models.robot_vacancies_model import VacanciesRobot


@main_auth(on_cookies=True)
def uninstall(request):
    try:
        VacanciesRobot.uninstall(request.bitrix_user_token)
    except Exception as exc:
        return HttpResponse(str(exc))

    return HttpResponse('ok')
