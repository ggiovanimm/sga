import csv
import io
from django.contrib import admin, messages
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Employee
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer, PageTemplate, BaseDocTemplate, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display =['name', 'segment', 'position', 'cpf', 'email']
    search_fields = ['name', 'cpf']
    list_filter = ['segment']
    actions = ['fill_outflow_form', 'generate_pdf_report', 'generate_csv_report']   

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
        title = Paragraph("Relatório de Funcionários", title_style)
        elements.append(title)
        elements.append(Spacer(1, 12))

        # Preparar dados da tabela
        data = [["Funcionário", "Setor", "Cargo"]]
        for employee in queryset:
            data.append([
                str(employee.name),
                str(employee.segment),
                str(employee.position)                
            ])

        # Criar e estilizar a tabela
        table = Table(data, colWidths=[140, 180, 240])
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
        writer.writerow(['Nome', 'Setor', 'CPF', 'Cargo', 'Celular', 'e-mail'])
        
        # Adiciona os dados do queryset no CSV
        for employee in queryset:
            writer.writerow([
                employee.name,
                employee.segment,
                employee.cpf,
                employee.position,
                employee.cell_phone,
                employee.email
            ])
        
        # Cria o HttpResponse com o conteúdo do CSV e codificação utf-8-sig
        response = HttpResponse(buffer.getvalue().encode('utf-8-sig'), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="relatorio_marcas_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv"'
        
        return response

    generate_csv_report.short_description = "Gerar exportação para CSV"

    def fill_outflow_form(self, request, queryset):
        # Verifica se apenas um funcionário foi selecionado
        if queryset.count() != 1:
            self.message_user(request, "Por favor, selecione apenas um funcionário para preencher no formulário de saída.", level=messages.WARNING)
            return HttpResponseRedirect(request.get_full_path())

        # Obtém o funcionário selecionado
        employee = queryset.first()
        
        # Gera a URL para o formulário de saída com os dados do funcionário preenchidos
        url = reverse('admin:outflows_outflow_add') + f'?employee_id={employee.id}&sector={employee.segment.id}'
        return HttpResponseRedirect(url)

    fill_outflow_form.short_description = "Abrir no formulário de saída"
