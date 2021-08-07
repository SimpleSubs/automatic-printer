from reportlab.lib.units import inch, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.utils import ImageReader
from pdf2image import convert_from_path
import json
import os

ORDER = {
    "bread": "sliced sourdough",
    "meat": ["turkey"],
    "cheese": ["swiss"],
    "condiments": ["mustard", "basil", "pickles"],
    "extras": [],
    "chips": "yes",
    "comments": "This is a test"
}

USER = {
    "name": "Emily Sturman",
    "grade": "12",
    "lunchSession": "cohort A",
    "podColor(mon/Tues)": "orange",
    "podColor(thurs/Fri)": "purple",
    "allergies": "none"
}

WIDTH = 62 * mm
HEIGHT = 3.5 * inch
MARGIN = 0.125 * inch
FONT_SIZE = 10

FILENAME = "order.pdf"
IMAGE_RATIO = 1

logo = "lwhs-logo.png"
logo_width = WIDTH - 2 * MARGIN
logo_height = logo_width / 384.0 * 80

section_format = "<font name='Josefin-Sans-Bold'>{}:</font> {}"

pdfmetrics.registerFont(TTFont("Josefin-Sans", "fonts/JosefinSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Josefin-Sans-Bold", "fonts/JosefinSans-Bold.ttf"))


def get_data(input_type, data):
    if data is None:
        return "N/A"
    elif not data:
        return "none"
    elif input_type == "CHECKBOX":
        return ", ".join(data)
    else:
        return data


def setup_background(canvas, doc):
    canvas.saveState()
    image = ImageReader(logo)
    image_height = 28
    padding = 5
    image_width = image_height * IMAGE_RATIO
    canvas.drawImage(image, WIDTH - image_width - padding, HEIGHT - image_height - padding, width=image_width, height=image_height, mask="auto")
    canvas.restoreState()


def create_pdf(filename, order, user, app_data):
    order_options = app_data["orderOptions"]
    user_fields = app_data["userFields"]
    doc = SimpleDocTemplate(filename, pagesize=(WIDTH, HEIGHT), rightMargin=MARGIN, leftMargin=MARGIN,
                            topMargin=MARGIN, bottomMargin=MARGIN)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Default", fontName="Josefin-Sans", leading=FONT_SIZE, spaceBefore=3,
                              fontSize=FONT_SIZE))
    styles.add(ParagraphStyle(name="Heading", fontName="Josefin-Sans-Bold", leading=FONT_SIZE, spaceBefore=5,
                              spaceAfter=5, fontSize=FONT_SIZE, alignment=TA_CENTER))
    content = [Paragraph("<u>Order</u>", styles["Heading"])]

    for option in order_options:
        section_data = get_data(option["type"], order.get(option["key"]))
        section_text = section_format.format(option["title"], section_data)
        content.append(Paragraph(section_text, styles["Default"]))

    content.append(Paragraph("<u>User</u>", styles["Heading"]))

    for field in user_fields:
        section_data = get_data(field["inputType"], user.get(field["key"]))
        section_text = section_format.format(field["title"], section_data)
        content.append(Paragraph(section_text, styles["Default"]))

    doc.build(content, onFirstPage=setup_background, onLaterPages=setup_background)


def create_printable(order, user, app_data):
    create_pdf(FILENAME, order, user, app_data)
    printable = convert_from_path(FILENAME)
    os.remove(FILENAME)
    return printable


with open("app-data.json") as file:
    app_data = json.load(file)

create_pdf("test.pdf", ORDER, USER, app_data)
