# Generated by Django 5.0 on 2024-12-05 22:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_alter_employee_position'),
        ('segments', '0002_alter_segment_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='segment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='employee_segments', to='segments.segment', verbose_name='Segmento'),
        ),
    ]
