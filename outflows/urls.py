# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('relatorio-saidas/', views.generate_pdf_report, name='generate_pdf_report'),
]
