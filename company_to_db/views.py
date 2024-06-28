from company_to_db.models import Company, Lead, Deal, Contact
from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def company_to_db(request):
    if request.method == 'POST':
        but = request.bitrix_user_token
        entity = request.POST.get('entity')
        match entity:
            case 'company':
                res = Company.sync_ent(but)
            case 'lead':
                res = Lead.sync_ent(but)
            case 'deal':
                res = Deal.sync_ent(but)
            case 'contact':
                res = Contact.sync_ent(but)
    return render(request, 'company_to_db.html', locals())
