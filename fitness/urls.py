from django.contrib import admin
from django.urls import path, include

# Что это: Импорт двух инструментов из библиотеки маршрутизации.
# path — создает конкретный маршрут (например, /trainers/).
# include — «включатель». Он говорит: «Я не буду сейчас описывать все маршруты,
# а передам управление другому файлу (club.urls или core.urls)».
# Без него нам пришлось бы писать все 4 страницы клуба прямо здесь, в главном файле.


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('club.urls', 'club'), namespace='club')),
    # Разбор: Пустая строка '' означает «любой URL, который не начался на admin/».
    # Почему '', Потому что в самом файле club/urls.py мы уже указали префиксы (trainers/, classes/)
    path('', include(('core.urls', 'core'), namespace='core')),
    # club.urls идет первее core.urls так как в 1-ом у нас прописаны все пути
]
