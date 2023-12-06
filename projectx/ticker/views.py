from moviepy.editor import ImageClip, TextClip, CompositeVideoClip
from wsgiref.util import FileWrapper
from PIL import Image

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import query

# Create your views here.

def index(request):
    return render(request, 'ticker/index.html')

@csrf_exempt
def ticker(request):

    if request.method == "POST":
        #получаем текст из запроса
        text_tick = request.POST.get("text_tick")

        #провереряем текст на заполненность, иначе редирект
        if len(text_tick) == 0:
            return redirect(request.META.get('HTTP_REFERER'))
            
        #заносим запрос в бд
        query_new = query(query_text=text_tick)
        query_new.save()


        duration = 3
        txt_fontsize = 50
        width = 100
        height = 100
        video_fps = 25

        #Генерируем изображение
        img  = Image.new( mode = "RGB", size = (width, height), color = (65, 105, 225) )
        img.save("ticker/templates/background.jpg")

        #создаем бэк видео из изображения
        clip = ImageClip('ticker/templates/background.jpg').set_duration(duration)
        #создаем видео - текст. Сами параметры перемещения текста (скорость, направление и позиции)
        #настраиваются внутри лямбда функции. Тут нужна более точная настройка, чем сейчас
        txt_on_clip = TextClip(text_tick, fontsize = txt_fontsize, color= 'white')
        txt_on_clip = txt_on_clip.set_duration(duration)
      
        text_width, text_height = txt_on_clip.size

        txt_on_clip = txt_on_clip.set_position(
              lambda t: (width - t / duration * (width + text_width),'center'))

        #склеиваем два клипа и сохраняем их в файл
        video = CompositeVideoClip([clip, txt_on_clip])
        video.write_videofile('ticker/templates/video.mp4', fps=video_fps)

        #упаковываем готовый файл с помощью FileWrapper (тут не получалось без него)
        #посылаем файл на скачку
        file = FileWrapper(open('ticker/templates/video.mp4', 'rb'))
        response = HttpResponse(file, content_type='video/mp4')
        response['Content-Disposition'] = 'attachment; filename=video.mp4'
        
        return response

    return None
