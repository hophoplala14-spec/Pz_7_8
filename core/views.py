from django.shortcuts import render
# render — это специальная функция Django.
# Она берет HTML-файл, подставляет в него данные (которые мы передадим) и отправляет браузеру.
from club.models import Client, Trainer, Class
#  Мы говорим: «Загляни в файл models.py приложения club и достань оттуда наши модели».


def home(request):

    """Главная страница клуба."""
#  мы создаем функцию с именем home (core/urls.py). Django автоматически передает в нее объект request
# request В нем хранится вся информация о том, кто зашел, какие данные отправил и т.д
    context = {
    'total_clients': Client.objects.count(),
    # Обращение в html total_clients
    # обращаемся к модели Client
    # берем менеджер objects (который умеет делать запросы)
    # и вызываем метод .count(). Возвращает просто число (например, 3
    'total_trainers': Trainer.objects.count(),
    'total_classes': Class.objects.count(),
}

    return render(request, 'core/home.html', context)
    # 'core/home.html' — путь до HTML-шаблона
    # context — данные, которые надо вставить в этот HTML
