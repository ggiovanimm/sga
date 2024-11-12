from django.db import models
from django.core.exceptions import ValidationError
from products.models import Product
from employees.models import Employee
from segments.models import Segment

class Outflow(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_outflows', verbose_name='Produto')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='outflows', verbose_name='Funcionário')
    sector = models.ForeignKey(Segment, on_delete=models.PROTECT, related_name='outflows', null=True, verbose_name='Setor')
    quantity = models.IntegerField(default=0, verbose_name='Quantidade')
    description = models.TextField(null=True, blank=True, verbose_name='Descrição')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Saída'

    def __str__(self):
        return str(self.product)
    
    def clean(self):
        if self.pk is None:  # Novo registro
            if self.product.quantity < self.quantity:
                raise ValidationError("Estoque insuficiente para realizar esta saída.")
        else:  # Atualização de saída existente
            old_quantity = Outflow.objects.get(pk=self.pk).quantity
            new_quantity = self.quantity - old_quantity
            if self.product.quantity < new_quantity:
                raise ValidationError("Estoque insuficiente para atualizar esta saída.")
            
        # Validação para garantir que a quantidade seja maior que zero
        if self.quantity <= 0:
            raise ValidationError({'quantity': 'A quantidade deve ser maior que zero.'})
        

    def save(self, *args, **kwargs):
        self.clean()
        if self.pk is None:
            self.product.quantity -= self.quantity
        else:
            old_quantity = Outflow.objects.get(pk=self.pk).quantity
            self.product.quantity -= self.quantity - old_quantity
        self.product.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.product.quantity += self.quantity
        self.product.save()
        super().delete(*args, **kwargs)
