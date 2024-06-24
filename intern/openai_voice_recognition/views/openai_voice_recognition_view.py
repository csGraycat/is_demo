import whisper
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from intern.openai_voice_recognition.views.forms import UploadFileForm
from settings import BASE_DIR
import os
from django.shortcuts import render


@main_auth(on_cookies=True)
def open_ai_get_text(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = request.FILES['file']
            file_path = os.path.join(BASE_DIR, 'media', 'transcript_samples', 'last_sample.mp3')

            with open(file_path, 'wb+') as local_file:
                for chunk in audio_file.chunks():
                    local_file.write(chunk)

            model = whisper.load_model('base')
            res = model.transcribe(os.path.join(BASE_DIR, 'media', 'transcript_samples', 'last_sample.mp3'))
            transcribed_text_base = res['text']
            return render(request, 'file_transcribed.html', locals())
    else:
        form = UploadFileForm()
    return render(request, "upload_file.html", {"form": form})
