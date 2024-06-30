from integration_utils.bitrix_robots.models import BaseRobot
import requests as req


class VacanciesRobot(BaseRobot):
    CODE = 'vacancies_robot'
    NAME = 'Робот возвращает вакансии компании с hh.ru'
    USE_SUBSCRIPTION = True
    APP_DOMAIN = "vervet-top-manually.ngrok-free.app"

    PROPERTIES = {
        'user': {
            'Name': {'ru': 'Получатель'},
            'Value': {'ru': 'Ответственный'},
            'Type': 'user',
            'Required': 'Y',
        },
        'employer_id': {
            'Name': {'ru': 'ID работодателя'},
            'Type': 'string',
            'Required': 'Y',
        },
    }

    RETURN_PROPERTIES = {
        'vacancies': {
            'Name': {'ru': 'Вакансии'},
            'Type': 'string',
            'Required': 'Y',
        },
        'ok': {
            'Name': {'ru': 'ok'},
            'Type': 'bool',
            'Required': 'Y',
        },
        'error': {
            'Name': {'ru': 'error'},
            'Type': 'string',
            'Required': 'N',
        },
    }

    def process(self) -> dict:
        vacancies = ''
        try:
            response = req.get(f'https://api.hh.ru/vacancies/?employer_id={self.props['employer_id']}')
            data = response.json()
            for item in data['items']:
                area = item['area']['name']
                vacancies += f'{item['name']}, {area}\n'
            self.dynamic_token.call_api_method('bizproc.event.send', {"event_token": self.event_token,
                                                                      "return_values": {"vacancies": vacancies,
                                                                                        }})

        except Exception as exc:
            return dict(ok=False, error=str(exc))

        return dict(ok=True)
