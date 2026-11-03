from django.db import models

class Client(models.Model):
    # Клиент фит-клуба
    # null = True - оставить пустое поле формы приложения
    # А blank = True - отправка пустого поля в БД
    full_name = models.CharField('ФИО', max_length=200)
    phone = models.CharField('Телефон', max_length=30)
    email = models.EmailField('Email', blank = True)
    birth_date = models.DateField('Дата рождения', null = True, blank = True)


    #Тренер. Meta - Просто узнать информ о самой таблице, настройки для все БД
    class  Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['full_name']

    def __str__(self):
        return self.full_name

class Trainer(models.Model):
    full_name = models.CharField('ФИО', max_length=200)
    specialization = models.CharField('Специализация', max_length=200)
    phone = models.CharField('Телефон', max_length=30)

    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренеры'
        ordering = ['full_name']

    def __str__(self):
        return f'{self.full_name} ({self.specialization})'

class Class(models.Model):
    # Занятия - тренеровка
    DAY_CHOICES = [
        ('mon', 'Понедельник'),
        ('tue', 'Вторник'),
        ('wed', 'Среда'),
        ('thu', 'Четверг'),
        ('fri', 'Пятница'),
        ('sat', 'Суббота'),
        ('sun', 'Воскресенье'),
    ]
    # on_delete=models.CASCADE - то все его занятия тоже автоматически удалятся
    # related_name='classes - мы сможем из объекта тренера достать все его занятия


    name = models.CharField('Название', max_length=200)
    trainer = models.ForeignKey(
        Trainer,
        # Внешений ключ к классу Trainer
        on_delete=models.CASCADE,
        related_name='classes',
        verbose_name='Тренер',
    )
    day_of_week = models.CharField('Дни недели', max_length=3, choices=DAY_CHOICES)
    time = models.TimeField('Время')
    room = models.CharField('Зал', max_length=50)

    # Связь "многие ко многим" - клиенты могут записываться на занятия
    clients = models.ManyToManyField(
        Client,
        blank=True,
        related_name='classes',
        # Связь с классом
        verbose_name='Записанные клиенты',
    )

    class Meta:
        verbose_name='Занятие'
        verbose_name_plural='Занятия'
        ordering = ['day_of_week', 'time']

    def __str__(self):
        return f'{self.name}, {self.trainer.full_name}'

class Membership(models.Model):
    # Абонемент (связан с клиентом один-к-одному)
    TYPE_CHOICES = [
        ('month', 'Месяц'),
        ('year', 'Год'),
    ]
    STATUS_CHOICES = [
        ('active', 'Активен'),
        ('expired', 'Просрочен'),
        ('frozen', 'Заморожен'),
    ]

    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        related_name='membership',
        verbose_name='Клиент',
    )
    type = models.CharField('Тип', max_length=10, choices = TYPE_CHOICES)
    start_date = models.DateField('Дата начала')
    end_date = models.DateField('Дата окончания')
    status  = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES, default = 'active')

    class Meta:
        verbose_name = 'Абонемент'
        verbose_name_plural = 'Абонементы'

    def __str__ (self):
        return f'{self.client.full_name} - {self.get_type_display()}'

    # get_<имя_поля>_display()
    # из - за choices = TYPE_CHOICES



    # URL (urls.py) (маршруты) — какие адреса будут на сайте (например, /trainers/).
    # Views (представления) — что делать, когда пользователь заходит по этому адресу (какие данные достать из БД).
    # Templates (шаблоны) — как это красиво отобразить (HTML).