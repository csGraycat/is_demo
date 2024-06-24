from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from django.shortcuts import render
from integration_utils.vendors.telegram import Bot
from integration_utils.vendors import telegram


@main_auth(on_cookies=True)
def bot_info(request):
    if request.method == 'POST':
        chat_id = int(request.POST.get('chat_id'))
        bot_token = request.POST.get('bot_token')
        return render(request, 'enter_message.html', locals())
    return render(request, 'bot_info.html')


@main_auth(on_cookies=True)
def send_msg_tg(request):
    if request.method == 'POST':
        chat_id = int(request.POST.get('chat_id'))
        bot_token = request.POST.get('bot_token')
        bot_not_found = False
        success = False
        msg_text = request.POST.get('msg_text')
        bot = Bot(token=bot_token)
        try:
            bot.send_message(text=msg_text, chat_id=chat_id)
        except telegram.error.TelegramError:
            bot_not_found = True
            return render(request, 'enter_message.html', locals())
        success = True
        return render(request, 'enter_message.html', locals())
    return render(request, 'enter_message.html')
