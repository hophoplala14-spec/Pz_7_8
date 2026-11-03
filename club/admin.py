from django.contrib import admin
from .models import Client, Membership, Trainer, Class


@admin.register(Client)
# @admin.register(Client) говорит Django: «Покажи модель Client в админке»
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email')
    # list_display — какие колонки показывать в общем списке (а не просто название)
    search_fields = ('full_name', 'phone')
    # search_fields — по каким полям можно искать (появится строка поиска)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('client', 'type', 'start_date', 'end_date', 'status')
    list_filter = ('type', 'status')
    # list_filter — добавит фильтры справа (например, фильтр по дням недели для занятий)


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'specialization', 'phone')

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'trainer', 'day_of_week', 'time', 'room')
    list_filter = ('day_of_week', 'trainer')
    filter_horizontal = ('clients',)
    # filter_horizontal — для связи «многие-ко-многим», сделает удобный выбор в две колонки со стрелочками.
    # запятая в конце нужна для разделения переменной, если переменная 1, то он ее разберет как строку, а не как переменную(относ ко всему)




