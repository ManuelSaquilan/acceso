# Generated by Django 5.0.2 on 2024-02-11 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eventosapp', '0005_rename_idevento_invitados_idevento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitados',
            name='ingreso',
            field=models.BooleanField(default=False, verbose_name='Ingresó'),
        ),
    ]
