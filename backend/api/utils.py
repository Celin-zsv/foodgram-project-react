import io

from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def getpdf(ingredients):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textobj = c.beginText()
    textobj.setTextOrigin(inch, 1 * inch)
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
    textobj.setFont('Arial', 12)

    lines = []
    for ingr in ingredients:
        if ingr.ingredient.name in lines:
            nam_index = lines.index(ingr.ingredient.name)
            lines[nam_index + 1] = str(int(lines[nam_index + 1]) + ingr.amount)
        if ingr.ingredient.name not in lines:
            lines.append(f'{ingr.ingredient.name}')
            lines.append(f'{ingr.amount}')
            lines.append(f'{ingr.ingredient.measurement_unit}')

    x = 144
    y = 14
    textobj.moveCursor(x, 0)
    textobj.textOut('Список покупок')
    textobj.moveCursor(-x, 0)
    textobj.textLine()
    textobj.textLine()
    v_count = 2
    for line in lines:
        textobj.textOut(line)
        if v_count == 0:
            v_count = 3
            textobj.moveCursor(-x * 2, y)
        else:
            textobj.moveCursor(x, 0)
        v_count -= 1

    c.drawText(textobj)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='shopping_list.pdf')
