# Generated by Django 5.0.1 on 2024-01-29 01:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Eventosapp', '0004_remove_evento_hora'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invitados',
            old_name='IdEvento',
            new_name='idEvento',
        ),
    ]
