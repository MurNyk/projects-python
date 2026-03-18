from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import mm
import os

def generate_business_trip_pdf(trip):
    # Extract trip details
    employee_name, destination, start_date, end_date, status, trip_purpose = trip[1], trip[2], trip[3], trip[4], trip[6], trip[5]

    # Create documents directory if it doesn't exist
    documents_dir = os.path.join(os.getcwd(), "documents")
    if not os.path.exists(documents_dir):
        os.makedirs(documents_dir)

    # Define file name and path
    file_name = f"business_trip_{trip[0]}.pdf"
    file_path = os.path.join(documents_dir, file_name)

    # Register the font correctly
    pdfmetrics.registerFont(TTFont('TimesNewRoman', 'C:/Windows/Fonts/times.ttf'))

    # Create a PDF canvas
    c = canvas.Canvas(file_path, pagesize=A4)

    # Set the font
    c.setFont("TimesNewRoman", 12)

    # Draw strings on the canvas
    c.drawString(30 * mm, 270 * mm, f"ФИО сотрудника: {employee_name}")
    c.drawString(30 * mm, 260 * mm, f"Место назначения: {destination}")
    c.drawString(30 * mm, 250 * mm, f"Дата начала: {start_date}")
    c.drawString(30 * mm, 240 * mm, f"Дата окончания: {end_date}")
    c.drawString(30 * mm, 230 * mm, f"Цель поездки: {trip_purpose}")
    c.drawString(30 * mm, 220 * mm, f"Статус: {status or 'Без статуса'}")

    c.drawString(30 * mm, 50 * mm, "Подпись: ____________")
    c.drawString(30 * mm, 40 * mm, "Дата: ____________")

    # Save the PDF
    c.save()

    return file_path