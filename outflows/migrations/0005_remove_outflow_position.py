# Generated by Django 5.0 on 2024-10-31 00:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outflows', '0004_outflow_position'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outflow',
            name='position',
        ),
    ]
