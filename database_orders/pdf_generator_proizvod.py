from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from datetime import datetime

def generate_processing_pdf(material):

    output_dir = "processing_documents"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf_file_path = os.path.join(output_dir, f"processing_{material[0]}.pdf")


    pdfmetrics.registerFont(TTFont('TimesNewRoman', 'times.ttf'))


    c = canvas.Canvas(pdf_file_path, pagesize=A4)


    current_date = datetime.now().strftime("%Y-%m-%d")


    c.setFont("TimesNewRoman", 16)
    c.drawString(100, 800, "Документ о переработке материала")


    c.setFont("TimesNewRoman", 12)
    c.drawString(100, 780, f"Дата: {current_date}")
    c.drawString(100, 760, "Город: ______________")


    table_data = [
        ["Название сырья", material[1]],
        ["Артикул", material[2]],
        ["Количество входного сырья", f"{material[3]} кг"],
        ["Масса выходного продукта", f"{material[4]} кг"],
        ["Поставщик", material[5]],
        ["Дата поставки", material[6]],
        ["Бригада", material[7]],
        ["Дата начала выполнения", material[8]],
        ["Что должно получиться", material[9]],
        ["Коэффициент переработки", f"{material[10]} кг"],
        ["Статус", material[11]],
    ]


    table = Table(table_data, colWidths=[150, 300])
    table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'TimesNewRoman', 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
    ]))


    table_x = 50
    table_y = 500
    table.wrapOn(c, 100, 600)
    table.drawOn(c, table_x, table_y)


    table_height = len(table_data) * 10
    signatures_y = table_y - table_height - 10



    signature_data = [
        ["Представитель Фирмы:", "Представитель Заказчика:"],
        ["________ /________ /", "_________ / __________ /"],
        ["Дата: ____________", "Дата: ____________"],
        [f"Проверил: ({material[7]}):"],
        ["________ /________ /", ], 
        ["________ /________ /", ""],   
        ["________ /________ /", ""], 
        ["________ /________ /", ""], 
        ["Приянл материал:", ""], 
        ["________ /________ /", ""], 
        ["Зав. складом", ""]   
    ]


    signature_table = Table(signature_data, colWidths=[250, 250])
    signature_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'TimesNewRoman', 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))


    signature_table.wrapOn(c, 100, 600)
    signature_table.drawOn(c, table_x, signatures_y - 100)


    c.showPage()
    c.save()

    return pdf_file_path