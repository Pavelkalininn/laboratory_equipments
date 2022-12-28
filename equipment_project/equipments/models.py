from django.contrib.auth.models import (
    AbstractUser,
)
from django.core.validators import (
    RegexValidator,
)
from django.db import (
    models,
)


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name', 'telegram_id')
    username = models.CharField(
        unique=True,
        max_length=150,
        verbose_name='Логин',
        validators=(RegexValidator(regex=r'^[\w.@+-]+\Z'),)
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='Почта'
    )
    telegram_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        unique=True,
        verbose_name='Телеграм id'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Equipment(models.Model):
    inventory = models.CharField(
        unique=True,
        max_length=30,
        verbose_name='Инвентарный номер'
    )
    name = models.CharField(
        max_length=256,
        verbose_name='Наименование'
    )
    model = models.CharField(
        max_length=256,
        verbose_name='Модель'
    )
    nomenclature_key = models.PositiveBigIntegerField(
        verbose_name='Код ТН ВЭД'
    )
    manual = models.FileField(
        upload_to='manuals',
        verbose_name='Руководство по эксплуатации',
    )
    document_path = models.CharField(
        max_length=256,
        verbose_name='Путь к папке с эксплуатационными документами'
    )
    creator = models.ForeignKey(
        User,
        related_name='equipments',
        on_delete=models.CASCADE,
        verbose_name='Создатель'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']


class Destination(models.Model):
    address = models.CharField(
        unique=True,
        max_length=256,
        verbose_name='Адрес'
    )

    def __str__(self):
        return self.address

    class Meta:
        ordering = ['address']


class Movement(models.Model):
    date = models.DateField(
        verbose_name='Дата передачи'
    )
    recipient = models.ForeignKey(
        User,
        related_name='recipient_movements',
        on_delete=models.CASCADE,
        verbose_name='Получатель'
    )
    early = models.BooleanField(
        verbose_name='Раньше фактической'
    )
    late = models.BooleanField(
        verbose_name='Позже фактической'
    )
    destination = models.ForeignKey(
        Destination,
        null=True,
        blank=True,
        related_name='movements',
        verbose_name='Место нахождения',
        on_delete=models.CASCADE
    )
    equipment = models.ForeignKey(
        Equipment,
        related_name='movements',
        verbose_name='Оборудование',
        on_delete=models.CASCADE
    )
    creator = models.ForeignKey(
        User,
        related_name='movements',
        on_delete=models.CASCADE,
        verbose_name='Создатель'
    )

    def __str__(self):
        return f'По адресу {self.destination} с {self.date}'

    class Meta:
        ordering = ['-date', '-id']
