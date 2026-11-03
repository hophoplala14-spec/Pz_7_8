from django.urls import path
from .views import TrainerListView, TrainerDetailView, ClassListView, ClientCreateView

add_name = 'club'

urlpatterns = [
    path('trainers/', TrainerListView.as_view(), name='trainer_list'),
    path('trainers/<int:pk>/', TrainerDetailView.as_view(), name='trainer_detail'),
    # Вот эта штука <int:pk> — это динамическая часть URL (параметр). Она означает:
    # < > — здесь будет меняться значение.
    # int — Django должен проверить, что там число (а не буквы).
    # pk — название переменной (Primary Key — ID записи в базе данных).
    # Когда ты кликаешь на Иванова (у него в базе ID=1), ссылка ведёт на /trainers/1/
    path('classes/', ClassListView.as_view(), name='class_list'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
]








