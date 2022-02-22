from flask import make_response
import flask_excel as excel
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.tables import Table
from reportlab.platypus.tables import TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from io import BytesIO


def get_xls(data,title):
    return excel.make_response_from_array(
        data, "xls", file_name=title)


def get_pdf(data,title):

    output = BytesIO()
    elements = []
    doc = SimpleDocTemplate(
        output, pagesize=letter)

    table = Table(data)
    style = TableStyle([
        ('BACKGROUND',(0,0),(-1,0), colors.gray),
        ('ALING',(0,0),(-1,-1), 'CENTER'),
        ('GRID',(0,0),(-1,-1),0.5, colors.black)
    ])
    table.setStyle(style)
    elements.append(table)
    doc.build(elements)
    pdf_out = output.getvalue()
    output.close()
    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename={}.pdf".format(title)
    response.mimetype = 'application/pdf'
    return response
