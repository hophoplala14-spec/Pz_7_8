from django import template
from django.db.models import Count
from club.models import Trainer, Class

register = template.Library()

@register.simple_tag
def total_trainers():
    # Простой тег: возвращает общее количество тренеров
    return Trainer.objects.count()

@register.inclusion_tag('club/tags/popular_classes.html')
def show_popular_classes(count=3):
    # Тег включения: подготавливает данные и рендерит для них HTML-шаблон
    classes = Class.objects.annotate(
        clients_count=Count('clients')
    ).order_by('-clients_count')[:count]
    return {'classes': classes}

@register.filter
def capitalize_first(value):
    # Фильтр: делает первую букву заглавной
    if not value:
        return value
    return str(value).capitalize()