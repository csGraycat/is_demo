import json

from django.db import models


class Entity(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    data = models.JSONField()

    entity = 'entity'

    class Meta:
        abstract = True

    @classmethod
    def sync_ent(cls, but):
        crms = but.call_list_method(f'crm.{cls.entity}.list')
        crms = {item['ID']: item for item in crms}

        crms_obj = []
        for index, data in crms.items():
            data_json = json.dumps(data)
            crms_obj.append(cls(id=index, data=data_json))

        if len(crms_obj) != 0:
            cls.objects.bulk_create(crms_obj, update_conflicts=True, unique_fields=['id'], update_fields=['data'])

        return "Данные загружены"


class Company(Entity):
    entity = 'company'
    pass


class Lead(Entity):
    entity = 'lead'
    pass


class Contact(Entity):
    entity = 'contact'
    pass


class Deal(Entity):
    entity = 'deal'
    pass
