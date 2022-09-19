# Generated by Django 3.2.15 on 2022-09-01 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=256, unique=True, verbose_name='Адрес')),
            ],
            options={
                'ordering': ['address'],
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Наименование документа')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inventory', models.CharField(max_length=30, unique=True, verbose_name='Инвентарный номер')),
                ('name', models.CharField(max_length=256, verbose_name='Наименование')),
                ('type', models.CharField(max_length=256, verbose_name='Тип')),
                ('model', models.CharField(max_length=256, verbose_name='Модель')),
                ('manufacturer', models.CharField(max_length=256, verbose_name='Производитель')),
                ('nomenclature_key', models.PositiveIntegerField(verbose_name='Код ТН ВЭД')),
                ('document_path', models.CharField(max_length=256, verbose_name='Путь к папке с эксплуатационными документами')),
                ('documents', models.ManyToManyField(related_name='equipments', to='equipments.Document', verbose_name='эксплуатационная документация в наличии')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Наименование организации')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата передачи в аренду')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rents', to='equipments.equipment', verbose_name='оборудование')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rents_from_owner', to='equipments.organization', verbose_name='Владелец')),
                ('renter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rents_from_renter', to='equipments.organization', verbose_name='Арендатор')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Movement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата перевозки оборудования на новое место')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movements', to='equipments.destination', verbose_name='место нахождения')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movements', to='equipments.equipment', verbose_name='оборудование')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Calibration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Наименование/номер документа о калибровке')),
                ('date', models.DateField(verbose_name='Дата калибровки')),
                ('validity_period', models.DateField(verbose_name='Дата окончания действия калибровки')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calibrations', to='equipments.equipment', verbose_name='оборудование')),
            ],
            options={
                'ordering': ['-validity_period'],
            },
        ),
        migrations.CreateModel(
            name='Attestation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Наименование/номер аттестата')),
                ('date', models.DateField(verbose_name='Дата аттестации')),
                ('validity_period', models.DateField(verbose_name='Дата окончания действия аттестата')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attestations', to='equipments.equipment', verbose_name='оборудование')),
            ],
            options={
                'ordering': ['-validity_period'],
            },
        ),
    ]
