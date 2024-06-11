from django.db import models
from django.db.utils import IntegrityError


class BizprocModel(models.Model):
    process_id = models.IntegerField(unique=True)
    process_name = models.CharField(max_length=200)

    @staticmethod
    def find_all_bizprocs(but, entity):
        tit = entity.title()
        cap = entity.upper()
        res_bizprocs = but.call_list_method('bizproc.workflow.template.list',
                                            {'select': ["ID", "NAME"],
                                             'filter': {"DOCUMENT_TYPE": [
                                                 "crm",
                                                 f"CCrmDocument{tit}",
                                                 f"{cap}"
                                             ]}})
        BizprocModel.objects.all().delete()
        for item in res_bizprocs:
            BizprocModel.objects.update_or_create(process_id=item['ID'], defaults={"process_name": item['NAME']})

    def run_cur_bizproc(self, but, entity_id, entity):
        tit = entity.title()
        but.call_api_method('bizproc.workflow.start', {
            'TEMPLATE_ID': self.process_id,
            'DOCUMENT_ID': ['crm', f'CCrmDocument{tit}', str(entity_id)]
        })

    def __str__(self):
        return f"Бизнес процесс {self.process_id} - {self.process_name}"