# Generated by Django 5.0 on 2024-10-27 01:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
        ('outflows', '0001_initial'),
        ('products', '0002_alter_product_category_alter_product_title'),
        ('segments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Outflow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0, verbose_name='Quantidade')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='outflows', to='employees.employee', verbose_name='Funcionário')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_outflows', to='products.product', verbose_name='Produto')),
                ('sector', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='outflows', to='segments.segment', verbose_name='Setor')),
            ],
        ),
        migrations.DeleteModel(
            name='Inflow',
        ),
    ]
