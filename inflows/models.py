from django.db import models
from django.core.exceptions import ValidationError
from products.models import Product

class Inflow(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_inflows', verbose_name='Produto')
    quantity = models.IntegerField(default=0, verbose_name='Quantidade')
    description = models.TextField(null=True, blank=True, verbose_name='Descrição')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Entrada'

    def __str__(self):
        return str(self.product)
    
    def clean(self):
        # Validação para garantir que a quantidade seja maior que zero
        if self.quantity <= 0:
            raise ValidationError({'quantity': 'A quantidade deve ser maior que zero.'})
    
    def save(self, *args, **kwargs):
        # Chama o método clean() para garantir a validação antes de salvar
        self.full_clean()

        # Atualizar a quantidade do produto ao salvar uma entrada
        if self.pk is None:  # Verifica se é um novo registro
            self.product.quantity += self.quantity
        else:
            # Caso de atualização, subtrai a quantidade antiga e adiciona a nova
            old_quantity = Inflow.objects.get(pk=self.pk).quantity
            self.product.quantity += self.quantity - old_quantity
        self.product.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Atualizar a quantidade do produto ao deletar uma entrada
        self.product.quantity -= self.quantity
        self.product.save()
        super().delete(*args, **kwargs)
