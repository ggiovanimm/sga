from django.http import JsonResponse
from django.db.models import Count, Sum
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.db.models.functions import TruncDate
from .models import Outflow

@method_decorator(staff_member_required, name='dispatch')
class OutflowChartView(TemplateView):
    template_name = 'admin/outflows/outflow_chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def get_outflow_data(request):
    # Dados por data
    daily_data = (Outflow.objects
                 .annotate(date=TruncDate('created_at'))
                 .values('date')
                 .annotate(total_quantity=Sum('quantity'))
                 .order_by('date'))

    data = {
        'daily': {
            'labels': [item['date'].strftime('%d/%m/%Y') for item in daily_data],
            'data': [item['total_quantity'] for item in daily_data]
        }
    }
    
    return JsonResponse(data)