# Generated by Django 5.0.1 on 2024-01-18 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eventosapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitados',
            name='hora_ingreso',
            field=models.DateField(blank=True, null=True, verbose_name='Hora de Ingreso'),
        ),
    ]
