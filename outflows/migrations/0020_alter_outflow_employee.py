# Generated by Django 5.0 on 2024-12-05 22:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0004_alter_employee_segment'),
        ('outflows', '0019_alter_outflow_sector'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outflow',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employee_outflows', to='employees.employee', verbose_name='Funcionário'),
        ),
    ]
