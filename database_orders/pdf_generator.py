import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas 
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime

def break_text_to_lines(text, max_width, canvas, font_name, font_size):
    canvas.setFont(font_name, font_size)
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        if canvas.stringWidth(current_line + " " + word) <= max_width:
            current_line += " " + word
        else:
            lines.append(current_line.strip())
            current_line = word
        
    if current_line:
        lines.append(current_line.strip())

    return lines

def generate_contract_pdf(client_name: str, product_name: str, quantity: int, product_price: float, total_price: float):
    documents_dir = os.path.join(os.getcwd(), "documents")
    if not os.path.exists(documents_dir):
        os.makedirs(documents_dir)

    json_path = os.path.join(os.getcwd(), "static", "contract_conditions.json")
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Файл {json_path} не найден. Проверьте путь и наличие файла.")

    with open(json_path, "r", encoding="utf-8") as json_file:
        contract_data = json.load(json_file)

    file_name = f"contract_{client_name}_gost.pdf"
    file_path = os.path.join(documents_dir, file_name)  # Исправлено

    pdfmetrics.registerFont(TTFont('TimesNewRoman', 'C:/Windows/Fonts/times.ttf'))
    pdfmetrics.registerFont(TTFont('TimesNewRomanBold', 'C:/Windows/Fonts/timesbd.ttf'))

    c = canvas.Canvas(file_path, pagesize=A4)

    width, height = A4
    margin_left = 30 * mm
    margin_right = A4[0] - 10 * mm
    margin_top = A4[1] - 20 * mm

    c.setFont('TimesNewRomanBold', 14)
    firm_name = contract_data["company_info"]["name"]
    firm_name_width = c.stringWidth(firm_name, 'TimesNewRomanBold', 14)
    c.drawString((width - firm_name_width) / 2, margin_top, firm_name)

    contract_title = contract_data["title"]
    contract_title_width = c.stringWidth(contract_title, 'TimesNewRomanBold', 14)
    c.drawString((width - contract_title_width) / 2, margin_top - 20, contract_title)

    c.setFont ("TimesNewRoman", 12)
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    time_text = f"Дата и время создания документа: {current_time}"
    time_text_width = c.stringWidth(time_text, "TimesNewRoman", 12)
    c.drawString((width - time_text_width) / 2, margin_top - 40, time_text)

    c.setFont("TimesNewRoman", 12)

    table_data = [
        ["Клиент", "Продукт", "Количество", "Цена за продукт", "Итоговая сумма"],
        [client_name, product_name, str(quantity), f"{product_price} руб.", f"{total_price} руб."]
    ]

    table = Table(table_data, colWidths=[100, 100, 80, 100, 120])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Исправлено
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'TimesNewRomanBold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTNAME', (0, 1), (-1, -1), 'TimesNewRoman'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    table.wrapOn(c, width, height)
    table.drawOn(c, margin_left, margin_top - 120)

    y_position = margin_top - 200
    c.setFont("TimesNewRoman", 12)
    c.drawString(margin_left, y_position, "Права и обязанности:")

    combined_text = " ".join(contract_data["rights_and_duties"])

    c.setFont("TimesNewRoman", 12)
    y_position -= 20
    lines = break_text_to_lines(combined_text, margin_right - margin_left, c, "TimesNewRoman", 12)
    for line in lines:
        c.drawString(margin_left, y_position, line)
        y_position -= 20
        if y_position < 60 * mm:
            c.showPage()
            c.setFont("TimesNewRoman", 12)
            y_position = margin_top - 40

    y_position -= 40

    company_info = [
        f"Название фирмы: {contract_data['company_info']['name']}",
        f"Адрес: {contract_data['company_info']['address']}",
        f"ИНН: {contract_data['company_info']['inn']}",
        f"ОГРН: {contract_data['company_info']['ogrn']}",
        f"Контактное лицо: {contract_data['company_info']['contact_person']}",
        f"Телефон: {contract_data['company_info']['phone']}"
    ]

    for info in company_info:
        c.drawString(margin_left, y_position, info)
        y_position -= 20
        if y_position < 40 * mm:
            c.showPage()
            y_position = margin_top - 40

    y_position -= 40

    image_path = "static/images/stiker.png"
    image_width = 45 * mm
    image_height = 45 * mm
    c.drawImage(image_path, margin_left + 10, y_position - 70, image_width, mask='auto')

    c.setFont("TimesNewRoman", 12)
    c.drawString(margin_left, y_position, "___________/Иванов И.И./")
    c.drawString(margin_left, y_position - 20, "подпись М.П.")

    c.save()
    print(f"PDF saved to: {file_path}")  # Для отладки

    return file_path