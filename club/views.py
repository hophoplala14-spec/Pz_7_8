from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Client, Membership, Trainer, Class


# В части 2 мы переходим на классовые представления (CBV).
# Классы уже содержат в себе логику, которую мы писали руками в функциях (FBV).

class TrainerListView(ListView):
    # Список всех тренеров (заменяет функцию trainer_list)
    model = Trainer
    template_name = 'club/trainer_list.html'
    context_object_name = 'trainers'  # Под каким именем список попадет в шаблон

    def get_queryset(self):
        # select_related и prefetch_related — это оптимизация (чтобы не делать 100 запросов к БД)
        return Trainer.objects.prefetch_related('classes').all()


class TrainerDetailView(DetailView):
    # Карточка конкретного тренера (заменяет функцию trainer_detail)
    model = Trainer
    template_name = 'club/trainer_detail.html'
    context_object_name = 'trainer'

    def get_queryset(self):
        # Автоматически ищет по pk из URL. Если не найдет — возвращает ошибку 404
        return Trainer.objects.prefetch_related('classes')


class ClassListView(ListView):
    # Список занятий с фильтром по дням недели (заменяет функцию class_list)
    model = Class
    template_name = 'club/class_list.html'
    context_object_name = 'classes'

    def get_queryset(self):
        # Заранее подгружаем тренеров и клиентов (select_related для ForeignKey, prefetch_related для ManyToMany)
        qs = Class.objects.select_related('trainer').prefetch_related('clients')

        # Читаем параметр из URL (например, ?day=mon)
        day = self.request.GET.get('day', '')

        # Если в URL передан день (например, понедельник), фильтруем занятия
        if day:
            qs = qs.filter(day_of_week=day)
        return qs

    def get_context_data(self, **kwargs):
        # Чтобы шаблон знал, какой день выбран в фильтре, и получил список всех дней
        context = super().get_context_data(**kwargs)
        context['selected_day'] = self.request.GET.get('day', '')
        context['days'] = Class.DAY_CHOICES
        return context


class ClientCreateView(CreateView):
    model = Client
    template_name = 'club/client_form.html'
    fields = ['full_name', 'phone', 'email', 'birth_date']
    success_url = reverse_lazy('club:trainer_list')
    def form_invalid(self, form):
        # Если форма не прошла валидацию (ошибки), мы принудительно передаем ее в шаблон
        # со специальным флагом или просто возвращаем стандартный ответ
        return super().form_invalid(form)

    def form_valid(self, form):
        # Этот метод вызывается, если форма прошла встроенную валидацию Django.
        # Сначала сохраняем клиента (super().form_valid(form))
        response = super().form_valid(form)

        # Достаем данные абонемента из POST-запроса
        membership_type = self.request.POST.get('membership_type', '')

        # Если выбран абонемент, создаем его для только что сохраненного клиента
        if membership_type:
            Membership.objects.create(
                client=self.object,  # self.object — это только что созданный клиент
                type=membership_type,
                start_date=self.request.POST.get('start_date') or None,
                end_date=self.request.POST.get('end_date') or None,
                status='active'
            )

        # Перенаправляем на список тренеров после успешного сохранения
        return response