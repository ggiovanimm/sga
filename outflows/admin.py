import csv
import io
from django import forms
from products.models import Product
from employees.models import Employee
from django.contrib import admin, messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path, reverse
from .views import OutflowChartView, get_outflow_data
# from django.utils.html import format_html
from .models import Outflow
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer, PageTemplate, BaseDocTemplate, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime

class OutflowForm(forms.ModelForm):
    class Meta:
        model = Outflow
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OutflowForm, self).__init__(*args, **kwargs)
        # Captura o 'product_id' da URL, se disponível
        if 'product_id' in self.initial:
            product_id = self.initial['product_id']
            try:
                # Pré-seleciona o produto no formulário
                self.fields['product'].initial = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                pass

        # Verifica se employee_id e sector estão presentes na URL e preenche o formulário
        if 'employee_id' in self.initial:
            employee_id = self.initial['employee_id']
            try:
                self.fields['employee'].initial = Employee.objects.get(id=employee_id)
            except Employee.DoesNotExist:
                pass

        # if 'sector' in self.initial:
        #     sector_id = self.initial['sector']
        #     try:
        #         self.fields['sector'].initial = segment.objects.get(id=sector_id)
        #     except segment.DoesNotExist:
        #         pass


@admin.register(Outflow)
class OutflowAdmin(admin.ModelAdmin):
    form = OutflowForm
    list_display = ['product', 'employee', 'sector', 'description',  'quantity', 'created_at']
    search_fields = ['product__title', 'employee__name', 'sector__name', 'quantity']
    list_filter = ['created_at']
    actions = ['generate_pdf_report', 'generate_csv_report', 'generate_chart_report', 'view_dashboard']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('chart/', self.admin_site.admin_view(OutflowChartView.as_view()), 
                 name='outflow_chart'),
            path('data/', self.admin_site.admin_view(get_outflow_data), 
                 name='outflows_outflow_data'),  # Adicione esta linha
        ]
        return custom_urls + urls

    def view_dashboard(self, request, queryset):
        url = reverse('admin:outflow_chart')
        return HttpResponseRedirect(url)
    view_dashboard.short_description = "Visualizar Dashboard de Saídas"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        # Verificar o estoque mínimo após salvar
        if obj.product.quantity <= 3:
            messages.warning(request, f"Aviso: O estoque mínimo foi atingido para o produto {obj.product}. Quantidade atual: {obj.product.quantity}")


    def generate_pdf_report(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="relatorio_saidas_{datetime.now().strftime("%Y%m%d%H%M%S")}.pdf"'

        # Criar o documento PDF com BaseDocTemplate
        doc = BaseDocTemplate(
            response,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=52,
            bottomMargin=52
        )

        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            alignment=1,  # Centralizado
            spaceAfter=30
        )

            # Lista para armazenar os elementos do PDF
        elements = []

            # Adicionar título
        title = Paragraph("Relatório de Saídas de Produtos", title_style)
        elements.append(title)
        elements.append(Spacer(1, 12))

        # Preparar dados da tabela
        data = [["Produto", "Funcionário", "Quantidade", "Data do Pedido"]]
        for outflow in queryset:
            data.append([
                str(outflow.product),
                str(outflow.employee),
                str(outflow.quantity),
                outflow.created_at.strftime("%d/%m/%Y")
            ])

        # Criar e estilizar a tabela
        table = Table(data, colWidths=[150, 150, 100, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWHEIGHT', (0, 0), (-1, -1), 30),
        ]))
        elements.append(table)

        # Função para cabeçalho e rodapé
        def header_footer(canvas, doc):
            # Cabeçalho
            canvas.saveState()
            canvas.setFont('Helvetica', 10)
            canvas.drawString(72, A4[1] - 40, "Instituto Auxiliadora")
            canvas.drawString(450, A4[1] - 40, f"Data: {datetime.now().strftime('%d/%m/%Y')}")

            # Rodapé com número da página
            canvas.drawString(72, 40, "Rua Nossa Senhora Auxiliadora, 56 - (32)3371-7272")
            canvas.drawString(450, 40, f"Página {doc.page}")
            canvas.restoreState()

        # Configurar o Frame e o PageTemplate
        frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
        doc.addPageTemplates([PageTemplate(id='ContentPage', frames=frame, onPage=header_footer)])

        # Gerar o PDF com os elementos e o rodapé personalizado
        doc.build(elements)
        return response

    generate_pdf_report.short_description = "Gerar Relatório em PDF"

    def generate_csv_report(self, request, queryset):
    # Cria um buffer de memória com codificação UTF-8 e BOM para compatibilidade com o Excel
        buffer = io.StringIO()
        writer = csv.writer(buffer, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        
        # Escreve o cabeçalho do CSV
        writer.writerow(['Produto', 'Funcionário', 'Setor', 'Quantidade', 'Data de Saída'])
        
        # Adiciona os dados do queryset no CSV
        for outflow in queryset:
            writer.writerow([
                outflow.product,
                outflow.employee,
                outflow.sector,
                outflow.quantity,
                outflow.created_at.strftime("%d/%m/%Y")
            ])
        
        # Cria o HttpResponse com o conteúdo do CSV e codificação utf-8-sig
        response = HttpResponse(buffer.getvalue().encode('utf-8-sig'), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="relatorio_marcas_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv"'
        
        return response

    generate_csv_report.short_description = "Gerar exportação para CSV"
        