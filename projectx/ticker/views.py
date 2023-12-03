from moviepy.editor import ImageClip, TextClip, CompositeVideoClip
from wsgiref.util import FileWrapper

from django.shortcuts import render
from django.http import HttpResponse

from .models import query

# Create your views here.

def index(request):
    return render(request, 'ticker/index.html')

def ticker(request):

    if request.method == "POST":
        
        #получаем текст из запроса
        text_tick = request.POST.get("text_tick")

        #провереряем текст на заполненность и присваиваем ему пробел для корректности обработки
        if len(text_tick) == 0:
            text_tick = " "

        #заносим запрос в бд
        query_new = query(query_text=text_tick)
        query_new.save()

        #создаем бэк видео из изображения
        clip = ImageClip('ticker/templates/background.jpg').set_duration(3)
        #создаем видео - текст. Сами параметры перемещения текста (скорость, направление и позиции)
        #настраиваются внутри лямбда функции. Тут нужна более точная настройка, чем сейчас
        txt_on_clip = TextClip(text_tick, fontsize = 60, color= 'white').set_position(
            lambda t: (max((len(text_tick) * 60), 300) - t * max((len(text_tick) * 35), 180),'center')).set_duration(3)

        #склеиваем два клипа и сохраняем их в файл
        video = CompositeVideoClip([clip, txt_on_clip])
        video.write_videofile('ticker/templates/video.mp4', fps=25)

        #упаковываем готовый файл с помощью FileWrapper (тут не получалось без него)
        #посылаем файл на скачку
        file = FileWrapper(open('ticker/templates/video.mp4', 'rb'))
        response = HttpResponse(file, content_type='video/mp4')
        response['Content-Disposition'] = 'attachment; filename=video.mp4'
        
        return response

    return None
