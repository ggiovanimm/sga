from django.db import models
from categories.models import Category
from brands.models import Brand


class Product(models.Model):
    title = models.CharField(max_length=500, verbose_name='Produto')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name='Catagoria')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products', verbose_name='Marca')
    description = models.TextField(null=True, blank=True, verbose_name='Descrição')
    quantity = models.IntegerField(default=0, verbose_name='Quantidade')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering = ['title']
        verbose_name = 'Produto'

    def __str__(self):
        return self.title
