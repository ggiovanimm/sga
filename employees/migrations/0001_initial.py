# Generated by Django 5.0 on 2024-10-27 00:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('segments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Funcionário')),
                ('cpf', models.TextField(blank=True, null=True, verbose_name='CPF')),
                ('position', models.TextField(blank=True, null=True, verbose_name='Cargo')),
                ('cell_phone', models.TextField(blank=True, null=True, verbose_name='Celular')),
                ('email', models.TextField(blank=True, null=True, verbose_name='E-mail')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('segment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='employees', to='segments.segment', verbose_name='Segmento')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
