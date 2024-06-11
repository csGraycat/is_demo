from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from allcompbizproc.forms.select_bp import BPForm
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

from allcompbizproc.models.bizprocmodel import BizprocModel


@main_auth(on_cookies=True)
def run_bizproc(request):
    global selected_entity_bp
    if request.method == 'POST':
        but = request.bitrix_user_token
        entity_id = but.call_list_method(f'crm.{selected_entity_bp}.list', {'select': ['ID']})
        form = BPForm(request.POST)
        if form.is_valid():
            cur_bp = form.cleaned_data['bp']
            for entity in entity_id:
                cur_bp.run_cur_bizproc(but, entity['ID'], selected_entity_bp)
            return HttpResponseRedirect(reverse('reload_start'))
    return render(request, 'select_entity_bp.html')


@main_auth(on_cookies=True)
def choose_bp(request):
    global selected_entity_bp
    selected_entity_bp = request.POST.get('entity')
    but = request.bitrix_user_token
    BizprocModel.find_all_bizprocs(but, selected_entity_bp)
    form = BPForm()
    return render(request, 'allcompbizproc.html', context={'form': form})
