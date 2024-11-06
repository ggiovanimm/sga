from django.db import models
from segments.models import Segment
from offices.models import Office

class Employee(models.Model):
    name = models.CharField(max_length=500, verbose_name='Funcionário')
    segment = models.ForeignKey(Segment, on_delete=models.PROTECT, related_name='employees', null=True, verbose_name='Segmento')
    cpf = models.CharField(max_length=20, null=True, blank=True, verbose_name='CPF')    
    position = models.ForeignKey(Office, on_delete=models.PROTECT, related_name='offices', null=True, verbose_name='Cargo')
    cell_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Celular')
    email = models.CharField(max_length=200, null=True, blank=True, verbose_name='E-mail')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering = ['name']
        verbose_name = 'Funcionário'

    def __str__(self):
        return self.name
