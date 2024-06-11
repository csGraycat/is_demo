import pandas as pd
import time
from callsuploader.models.models import CallInfo
import os
from django.conf import settings
import requests

OBJECT_CRM = {"Лиды": 1,
              "Сделки": 2,
              "Контакты": 3,
              "Компании": 4,
              "Коммерческие предложения": 7,
              "Новые счета": 31}


def make_links_from_origin(data, excel_field, b24_field, source_map, prefix):
    """Заменяет excel_field=COMPANY_ORIGIN_ID на b24_field=COMPANY_ID учитывая предыдущую замену при импорте демоданных
    для создания правильной адресации на только что созданные сущности"""
    for d in data:
        if d.get(excel_field):
            d[b24_field] = \
                source_map["{}_{}".format(prefix, d.get(excel_field))]['ID']
    return data


def add_origin_prefix(data, prefix):
    for d in data:
        # Добавляем префикс для ORIGIN_ID
        if d.get('ORIGIN_ID'):
            d['ORIGIN_ID'] = "{}_{}".format(prefix, d.get('ORIGIN_ID'))
    return data


def load_crm(crm_items, but, type_id):
    # выгружает элементы crm в битрикс
    methods = []
    for item in crm_items:
        methods.append(('crm.item.import',
                        {"entityTypeId": type_id, "fields": item}))
    but.batch_api_call(methods)


def upload_to_bitrix(table, but):
    """Загружает сущности (компании, контакты, сделки, лиды, звонки) из гугл-таблицы в битрикс"""
    global companies_origin_id_dict
    excel_file = pd.ExcelFile(table)
    sheet_names = excel_file.sheet_names
    # для всего пакета загрузки будет одинаковый префикс у ORIGIN_ID
    load_origin_id_prefix = time.time()
    object_count = {}
    for sheet in sheet_names:
        object_count.update({sheet: '0'})

    if 'Звонки' in sheet_names:
        call_data = excel_file.parse('Звонки').to_dict('records')
        object_count['Звонки'] = len(call_data)
        for c in call_data:
            call = CallInfo(
                user_phone=c["user_phone"],
                user_id=int(c["user_id"]),
                phone_number=c["phone_number"],
                call_date=c["call_date"],
                type=int(c["type"]),
                add_to_chat=int(c["add_to_chat"])
            )

            drive_id = c["file"].split("/")[-2]
            download_link = "https://drive.google.com/uc?id=" + drive_id + "&export=download"

            call_file = requests.get(download_link).content
            file_path = os.path.join(call.inner_media_path, str(call.id) + '.mp3')  # rings/id.mp3
            with open(os.path.join(settings.MEDIA_ROOT, file_path), 'wb') as file:  # base/media/rings/id.mp3
                file.write(call_file)

            call.file.name = file_path
            call.save()

            call.telephony_externalcall_register(but)
            call.telephony_externalcall_finish(but)

    if 'Компании' in sheet_names:
        company_data = excel_file.parse('Компании').to_dict("records")
        company_data = add_origin_prefix(company_data, load_origin_id_prefix)
        object_count["Компании"] = len(company_data)
        load_crm(company_data, but, "4")

        companies = but.call_list_method('crm.company.list', {
            "SELECT": ["ORIGIN_ID", "ID"],
            "FILTER": {"%ORIGIN_ID": "{}_".format(load_origin_id_prefix)}})
        companies_origin_id_dict = {item['ORIGIN_ID']: item for item in
                                    companies}
        for d in company_data:
            but.call_api_method("crm.address.add", {"fields": {
                "TYPE_ID": "1",
                "ENTITY_TYPE_ID": "4",
                "ENTITY_ID": companies_origin_id_dict[d['ORIGIN_ID']]['ID'],
                "CITY": d["ADDRESS_CITY"],
                "ADDRESS_1": d["ADDRESS"],
            }})

    if 'Контакты' in sheet_names:
        contacts_data = excel_file.parse('Контакты').to_dict("records")
        contacts_data = add_origin_prefix(contacts_data, load_origin_id_prefix)
        contacts_data = make_links_from_origin(contacts_data,
                                               'COMPANY_ORIGIN_ID',
                                               'COMPANY_ID',
                                               companies_origin_id_dict,
                                               load_origin_id_prefix)  # меняем company_origin_id на company_id
        for c in contacts_data:
            c["PHONE"] = [{"VALUE": str(c["PHONE"]), "VALUE_TYPE": "WORK"}]

        object_count["Контакты"] = len(contacts_data)
        load_crm(contacts_data, but, "3")

    if 'Лиды' in sheet_names:
        lead_data = excel_file.parse('Лиды').to_dict('records')
        load_crm(lead_data, but, 1)
        object_count['Лиды'] = len(lead_data)

    if 'Сделки' in sheet_names:
        deal_data = excel_file.parse('Сделки').to_dict('records')
        load_crm(deal_data, but, 2)
        object_count['Сделки'] = len(deal_data)

    return object_count
