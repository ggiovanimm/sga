from django.db import models

class Office(models.Model):
    name = models.CharField(max_length=500, verbose_name='Cargo')
    description = models.TextField(null=True, blank=True, verbose_name='Descrição')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering = ['name']
        verbose_name = 'Cargo'

    def __str__(self):
        return self.name
