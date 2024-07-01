import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from dateutil import parser as dt


@main_auth(on_cookies=True)
def show_grid(request):
    """Позволяет вывести список юзеров с помощью ag-grid."""

    but = request.bitrix_user_token
    deals = but.call_list_method('crm.deal.list')

    deal_fields = [
        'ID', 'TITLE', 'TYPE_ID', 'CATEGORY_ID', 'STAGE_ID', 'STAGE_SEMANTIC_ID', 'IS_NEW', 'IS_RECURRING',
        'IS_RETURN_CUSTOMER', 'IS_REPEATED_APPROACH', 'PROBABILITY', 'CURRENCY_ID', 'OPPORTUNITY',
        'IS_MANUAL_OPPORTUNITY', 'TAX_VALUE', 'COMPANY_ID', 'CONTACT_ID', 'CONTACT_IDS', 'QUOTE_ID', 'BEGINDATE',
        'CLOSEDATE', 'OPENED', 'CLOSED', 'COMMENTS', 'ASSIGNED_BY_ID', 'CREATED_BY_ID', 'MODIFY_BY_ID', 'MOVED_BY_ID',
        'DATE_CREATE', 'DATE_MODIFY', 'MOVED_TIME', 'SOURCE_ID', 'SOURCE_DESCRIPTION', 'LEAD_ID', 'ADDITIONAL_INFO',
        'LOCATION_ID', 'ORIGINATOR_ID', 'ORIGIN_ID', 'UTM_SOURCE', 'UTM_MEDIUM', 'UTM_CAMPAIGN', 'UTM_CONTENT',
        'UTM_TERM', 'LAST_ACTIVITY_TIME', 'LAST_ACTIVITY_BY'
    ]

    STAGE = {'NEW': 'Новая',
             'PREPARATION': 'Подготовка бумаг',
             'PREPAYMENT_INVOICE': 'Отправка счёта',
             'EXECUTING': 'В процессе выполнения',
             'FINAL_INVOICE': 'Финальный счёт'
             }

    for deal in deals:

        for key in deal_fields:
            deal.setdefault(key, "")

        deal['STAGE'] = STAGE[deal['STAGE_ID']]
        deal['PRICE'] = f'{deal['OPPORTUNITY']} {deal['CURRENCY_ID']}'
        deal['DATE_CREATE'] = dt.parse(deal['DATE_CREATE']).strftime('%d.%m.%Y')

        created_by = (f'{but.call_api_method('user.get', {'ID': deal['CREATED_BY_ID']})['result'][0]['NAME']} '
                      f'{but.call_api_method('user.get', {'ID': deal['CREATED_BY_ID']})['result'][0]['LAST_NAME']}')
        deal['CREATED_BY'] = created_by

    json_deal_list = json.dumps(deals, cls=DjangoJSONEncoder)

    return render(request, 'ag_deal_list.html',
                  context={
                      'json_deal_list': json_deal_list,
                  })
