from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Document(models.Model):
    name = models.CharField(
        unique=True,
        max_length=256,
        verbose_name='Наименование документа'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


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
    type = models.CharField(
        max_length=256,
        verbose_name='Тип'
    )
    model = models.CharField(
        max_length=256,
        verbose_name='Модель'
    )
    manufacturer = models.CharField(
        max_length=256,
        verbose_name='Производитель'
    )
    nomenclature_key = models.PositiveIntegerField(
        verbose_name='Код ТН ВЭД'
    )
    documents = models.ManyToManyField(
        Document,
        related_name='equipments',
        verbose_name='эксплуатационная документация в наличии',
    )
    document_path = models.CharField(
        max_length=256,
        verbose_name='Путь к папке с эксплуатационными документами'
    )
    creator = models.ForeignKey(
        User,
        null=True,
        related_name='equipments',
        on_delete=models.CASCADE,
        verbose_name='Создатель'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']


class Organization(models.Model):
    name = models.CharField(
        unique=True,
        max_length=256,
        verbose_name='Наименование организации'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']


class Rent(models.Model):
    owner = models.ForeignKey(
        Organization,
        related_name='rents_from_owner',
        on_delete=models.CASCADE,
        verbose_name='Владелец'
    )
    renter = models.ForeignKey(
        Organization,
        related_name='rents_from_renter',
        on_delete=models.CASCADE,
        verbose_name='Арендатор'
    )
    date = models.DateField(
        verbose_name='Дата передачи в аренду'
    )
    equipment = models.ForeignKey(
        Equipment,
        related_name='rents',
        verbose_name='оборудование',
        on_delete=models.CASCADE
    )
    creator = models.ForeignKey(
        User,
        null=True,
        related_name='rents',
        on_delete=models.CASCADE,
        verbose_name='Создатель'
    )

    def __str__(self):
        return f'Арендодатель: {self.owner}, арендатор: {self.renter}.'

    class Meta:
        ordering = ['-date', '-id']


class Attestation(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Наименование/номер аттестата'
    )
    date = models.DateField(
        verbose_name='Дата аттестации'
    )
    validity_period = models.DateField(
        verbose_name='Дата окончания действия аттестата'
    )
    equipment = models.ForeignKey(
        Equipment,
        related_name='attestations',
        verbose_name='оборудование',
        on_delete=models.CASCADE
    )
    creator = models.ForeignKey(
        User,
        null=True,
        related_name='attestations',
        on_delete=models.CASCADE,
        verbose_name='Создатель'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-validity_period']


class Calibration(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Наименование/номер документа о калибровке'
    )
    date = models.DateField(
        verbose_name='Дата калибровки'
    )
    validity_period = models.DateField(
        verbose_name='Дата окончания действия калибровки'
    )
    equipment = models.ForeignKey(
        Equipment,
        related_name='calibrations',
        verbose_name='оборудование',
        on_delete=models.CASCADE
    )
    creator = models.ForeignKey(
        User,
        null=True,
        related_name='calibrations',
        on_delete=models.CASCADE,
        verbose_name='Создатель'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-validity_period']


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
        verbose_name='Дата перевозки оборудования на новое место'
    )
    destination = models.ForeignKey(
        Destination,
        related_name='movements',
        verbose_name='место нахождения',
        on_delete=models.CASCADE
    )
    equipment = models.ForeignKey(
        Equipment,
        related_name='movements',
        verbose_name='оборудование',
        on_delete=models.CASCADE
    )
    creator = models.ForeignKey(
        User,
        null=True,
        related_name='movements',
        on_delete=models.CASCADE,
        verbose_name='Создатель'
    )

    def __str__(self):
        return f'По адресу {self.destination} расположен {self.equipment}'

    class Meta:
        ordering = ['-id']
