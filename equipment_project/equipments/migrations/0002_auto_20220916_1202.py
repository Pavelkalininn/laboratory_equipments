# Generated by Django 3.2.15 on 2022-09-16 09:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('equipments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rent',
            options={'ordering': ['-date', '-id']},
        ),
        migrations.AddField(
            model_name='attestation',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attestations', to=settings.AUTH_USER_MODEL, verbose_name='Создатель'),
        ),
        migrations.AddField(
            model_name='calibration',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='calibrations', to=settings.AUTH_USER_MODEL, verbose_name='Создатель'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipments', to=settings.AUTH_USER_MODEL, verbose_name='Создатель'),
        ),
        migrations.AddField(
            model_name='movement',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movements', to=settings.AUTH_USER_MODEL, verbose_name='Создатель'),
        ),
        migrations.AddField(
            model_name='rent',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rents', to=settings.AUTH_USER_MODEL, verbose_name='Создатель'),
        ),
    ]
