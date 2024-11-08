# urls.py
from django.urls import path
from . import views

app_name = 'outflows'  # Adicione isso para namespace

urlpatterns = [
    path('relatorio-saidas/', views.generate_pdf_report, name='generate_pdf_report'),    
    path('outflow-chart/', views.OutflowChartView.as_view(), name='outflow_chart'),
    path('api/outflow-data/', views.get_outflow_data, name='outflow_data'),
]
