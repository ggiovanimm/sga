# Generated by Django 5.0 on 2024-10-27 02:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inflows', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inflow',
            options={'ordering': ['-created_at'], 'verbose_name': 'Entrada'},
        ),
    ]
