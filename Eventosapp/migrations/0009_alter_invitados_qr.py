# Generated by Django 5.0.2 on 2024-02-13 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eventosapp', '0008_invitados_qr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitados',
            name='qr',
            field=models.ImageField(blank=True, null=True, upload_to='qr'),
        ),
    ]
