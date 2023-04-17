from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.graphics.barcode import qr
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing 

from PIL import Image
from reportlab.lib.units import mm
import webbrowser as wb
import sys
import datetime
import pyomo.environ as pyo

def new_page(c):
    c.drawImage('../img/encabezado.png', 0, c._pagesize[1] - 35*mm, (c._pagesize[0]), (35*mm))
    c.drawImage('../img/pie.png', 0, -2, (c._pagesize[0]), (25*mm))
    return None

def crear_reporte(model, localization):
    # Proveedores
    for i in model.I:
        
        c = canvas.Canvas('../proveedores/'+str(i)+".pdf", pagesize=letter)
        c.drawImage('../img/encabezado.png', 0, c._pagesize[1] - 35*mm, (c._pagesize[0]), (35*mm))
        c.drawImage('../img/pie.png', 0, -2, (c._pagesize[0]), (25*mm))

        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(c._pagesize[0]/2, 630 , 'INFORME DE PLANEACIÓN - PROVEEDOR')
        c.setFont("Helvetica-Bold", 14)
        c.drawString(15*mm, 205*mm , 'FECHA:')
        c.drawString(15*mm, 195*mm , 'RESPONSABLE:')
        c.drawString(15*mm, 185*mm , 'DEPARTAMENTO:')

        c.setFont("Helvetica", 14)
        c.drawString(35*mm, 205*mm , str(datetime.date.today().strftime("%d/%m/%Y")))
        c.drawString(56*mm, 195*mm , str(i))
        c.drawString(60*mm, 185*mm , localization)

        c.drawString(15*mm, 170*mm , 'A través de la presente circular se le comunica su compromiso de producción')
        c.drawString(15*mm, 160*mm , 'de LECHE como se relaciona a continuación:')

        c.rect(15*mm, 135*mm, width=95*mm, height=12.5*mm, stroke=1, fill=0)
        c.rect(110*mm, 135*mm, width=40*mm, height=12.5*mm, stroke=1, fill=0)
        c.rect(150*mm, 135*mm, width=30*mm, height=12.5*mm, stroke=1, fill=0)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(62.5*mm, 138*mm , 'CLIENTE')
        c.drawCentredString(130*mm, 138*mm , 'CANTIDAD')
        c.drawCentredString(165*mm, 138*mm , 'CHECK')
        c.setFont("Helvetica", 12)

        y = 127*mm
        aux_cont = 0
        for k in model.K:
            if pyo.value(model.x1[i, k, 0]) > 0:
                c.rect(15*mm, y, width=95*mm, height=8*mm, stroke=1, fill=0)
                c.rect(110*mm, y, width=40*mm, height=8*mm, stroke=1, fill=0)
                c.rect(150*mm, y, width=30*mm, height=8*mm, stroke=1, fill=0)
                if len(str(k)) > 32:
                    c.setFont("Helvetica", 11)
                c.drawCentredString(62.5*mm, y+2*mm , str(k))
                c.setFont("Helvetica", 12)
                c.drawCentredString(130*mm, y+2*mm , str(round(pyo.value(model.x1[i, k, 0]), 1)))
                aux_cont += 1
                if aux_cont > 12:
                    c.showPage()
                    c.drawImage('../img/encabezado.png', 0, c._pagesize[1] - 35*mm, (c._pagesize[0]), (35*mm))
                    c.drawImage('../img/pie.png', 0, -2, (c._pagesize[0]), (25*mm))
                    y = 225*mm
                    aux_cont = -30
                y -= 8*mm
        
        y -= 5*mm

        c.drawString(15*mm, y , 'En caso de tener alguna dificultad para cumplir con los compromisos antes ')
        y -= 10*mm
        c.drawString(15*mm, y , 'descritos de forma competa o parcial, por favor comunicarlo al líder de su ')
        y -= 10*mm
        c.drawString(15*mm, y , 'asociación o al grupo de investigación queso costeño en el correo ')
        y -= 10*mm
        c.drawString(15*mm, y , 'quesocostenogr@unimagdalena.edu.co')

        c.save()
    
    # Productor
    for k in model.K:
        c = canvas.Canvas('../productores/'+str(k)+".pdf", pagesize=letter)
        c.drawImage('../img/encabezado.png', 0, c._pagesize[1] - 35*mm, (c._pagesize[0]), (35*mm))
        c.drawImage('../img/pie.png', 0, -2, (c._pagesize[0]), (25*mm))

        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(c._pagesize[0]/2, 650 , 'INFORME DE PLANEACIÓN - PRODUCTOR')
        c.setFont("Helvetica-Bold", 14)
        c.drawString(15*mm, 215*mm , 'FECHA:')
        c.drawString(15*mm, 205*mm , 'RESPONSABLE:')
        c.drawString(15*mm, 195*mm , 'DEPARTAMENTO:')

        c.setFont("Helvetica", 14)
        c.drawString(35*mm, 215*mm , str(datetime.date.today().strftime("%d/%m/%Y")))
        c.drawString(56*mm, 205*mm , str(k))
        c.drawString(60*mm, 195*mm , localization)

        c.setFont("Helvetica", 12)
        c.drawString(15*mm, 180*mm , 'A través de la presente circular se le comunica su compromiso de producción de QUESO')
        c.drawString(15*mm, 173*mm , 'como se relaciona a continuación:')

        # Tabla a recibir

        c.rect(15*mm, 160*mm, width=95*mm, height=8*mm, stroke=1, fill=0)
        c.rect(110*mm, 160*mm, width=40*mm, height=8*mm, stroke=1, fill=0)
        c.rect(150*mm, 160*mm, width=30*mm, height=8*mm, stroke=1, fill=0)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(62.5*mm, 162*mm , 'PROVEEDOR')
        c.drawCentredString(130*mm, 162*mm , 'CANTIDAD (L)')
        c.drawCentredString(165*mm, 162*mm , 'CHECK')
        c.setFont("Helvetica", 12)

        y = 152*mm
        for i in model.I:
            if pyo.value(model.x1[i, k, 0]) > 0:
                c.rect(15*mm, y, width=95*mm, height=8*mm, stroke=1, fill=0)
                c.rect(110*mm, y, width=40*mm, height=8*mm, stroke=1, fill=0)
                c.rect(150*mm, y, width=30*mm, height=8*mm, stroke=1, fill=0)
                c.drawCentredString(62.5*mm, y+2*mm , str(i))
                c.drawCentredString(130*mm, y+2*mm , str(round(pyo.value(model.x1[i, k, 0]), 1)))
                
                y -= 8*mm
        
        y -= 5*mm

        #Tabla a entregar

        c.rect(15*mm, y, width=95*mm, height=8*mm, stroke=1, fill=0)
        c.rect(110*mm, y, width=40*mm, height=8*mm, stroke=1, fill=0)
        c.rect(150*mm, y, width=30*mm, height=8*mm, stroke=1, fill=0)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(62.5*mm, y+2*mm , 'ACOPIO')
        c.drawCentredString(130*mm, y+2*mm , 'CANTIDAD (Kg)')
        c.drawCentredString(165*mm, y+2*mm , 'CHECK')
        c.setFont("Helvetica", 12)

        y -= 8*mm
        for r in model.R:
            if pyo.value(model.x3[k, r, 0]) > 0.1:
                c.rect(15*mm, y, width=95*mm, height=8*mm, stroke=1, fill=0)
                c.rect(110*mm, y, width=40*mm, height=8*mm, stroke=1, fill=0)
                c.rect(150*mm, y, width=30*mm, height=8*mm, stroke=1, fill=0)
                c.drawCentredString(62.5*mm, y+2*mm , str(r))
                c.drawCentredString(130*mm, y+2*mm , str(round(pyo.value(model.x3[k, r, 0]), 1)))
                
                y -= 8*mm
        
        y -= 5*mm

        c.drawString(15*mm, y , 'En caso de tener alguna dificultad para cumplir con los compromisos antes descritos')
        y -= 7*mm
        c.drawString(15*mm, y , 'de forma competa o parcial, por favor comunicarlo al líder de su asociación o al grupo')
        y -= 7*mm
        c.drawString(15*mm, y , 'de investigación queso costeño en el correo quesocostenogr@unimagdalena.edu.co')
        y -= 7*mm
        c.drawString(15*mm, y , '')

        c.save()
    
    # Acopios
    for r in model.R:
        if pyo.value(model.y[r]) >= 1:
            c = canvas.Canvas('../acopios/'+str(r)+".pdf", pagesize=letter)
            c.drawImage('../img/encabezado.png', 0, c._pagesize[1] - 35*mm, (c._pagesize[0]), (35*mm))
            c.drawImage('../img/pie.png', 0, -2, (c._pagesize[0]), (25*mm))

            c.setFont("Helvetica-Bold", 20)
            c.drawCentredString(c._pagesize[0]/2, 650 , 'INFORME DE PLANEACIÓN - ACOPIO')
            c.setFont("Helvetica-Bold", 14)
            c.drawString(15*mm, 215*mm , 'FECHA:')
            c.drawString(15*mm, 205*mm , 'RESPONSABLE:')
            c.drawString(15*mm, 195*mm , 'DEPARTAMENTO:')

            c.setFont("Helvetica", 14)
            c.drawString(35*mm, 215*mm , str(datetime.date.today().strftime("%d/%m/%Y")))
            c.drawString(56*mm, 205*mm , str(r))
            c.drawString(60*mm, 195*mm , localization)

            c.setFont("Helvetica", 12)
            c.drawString(15*mm, 180*mm , 'A través de la presente circular se le comunica su compromiso de acopio de QUESO')
            c.drawString(15*mm, 173*mm , 'como se relaciona a continuación:')

            # Tabla a recibir

            c.rect(15*mm, 160*mm, width=95*mm, height=8*mm, stroke=1, fill=0)
            c.rect(110*mm, 160*mm, width=40*mm, height=8*mm, stroke=1, fill=0)
            c.rect(150*mm, 160*mm, width=30*mm, height=8*mm, stroke=1, fill=0)
            c.setFont("Helvetica-Bold", 12)
            c.drawCentredString(62.5*mm, 162*mm , 'PRODUCTOR')
            c.drawCentredString(130*mm, 162*mm , 'CANTIDAD (Kg)')
            c.drawCentredString(165*mm, 162*mm , 'CHECK')
            c.setFont("Helvetica", 12)

            y = 152*mm
            aux_cont = 0
            for k in model.K:
                if pyo.value(model.x3[k, r, 0]) > 0:
                    c.rect(15*mm, y, width=95*mm, height=8*mm, stroke=1, fill=0)
                    c.rect(110*mm, y, width=40*mm, height=8*mm, stroke=1, fill=0)
                    c.rect(150*mm, y, width=30*mm, height=8*mm, stroke=1, fill=0)
                    c.drawCentredString(62.5*mm, y+2*mm , str(k))
                    c.drawCentredString(130*mm, y+2*mm , str(round(pyo.value(model.x3[k, r, 0]), 1)))
                    aux_cont += 1
                    if aux_cont > 11:
                        c.showPage()
                        c.drawImage('../img/encabezado.png', 0, c._pagesize[1] - 35*mm, (c._pagesize[0]), (35*mm))
                        c.drawImage('../img/pie.png', 0, -2, (c._pagesize[0]), (25*mm))
                        y = 225*mm
                        aux_cont = -30
                    y -= 8*mm
            
            y -= 5*mm

            #Tabla a entregar

            c.rect(15*mm, y, width=95*mm, height=8*mm, stroke=1, fill=0)
            c.rect(110*mm, y, width=40*mm, height=8*mm, stroke=1, fill=0)
            c.rect(150*mm, y, width=30*mm, height=8*mm, stroke=1, fill=0)
            c.setFont("Helvetica-Bold", 12)
            c.drawCentredString(62.5*mm, y+2*mm , 'COMERCIALIZADOR')
            c.drawCentredString(130*mm, y+2*mm , 'CANTIDAD (Kg)')
            c.drawCentredString(165*mm, y+2*mm , 'CHECK')
            c.setFont("Helvetica", 12)

            y -= 8*mm
            
            for m in model.M:
                if pyo.value(model.x4[r, m, 0]) > 0.1:
                    c.rect(15*mm, y, width=95*mm, height=8*mm, stroke=1, fill=0)
                    c.rect(110*mm, y, width=40*mm, height=8*mm, stroke=1, fill=0)
                    c.rect(150*mm, y, width=30*mm, height=8*mm, stroke=1, fill=0)
                    c.drawCentredString(62.5*mm, y+2*mm , str(m))
                    c.drawCentredString(130*mm, y+2*mm , str(round(pyo.value(model.x4[r, m, 0]), 1)))
                    aux_cont += 1
                    if aux_cont > 12:
                        c.showPage()
                        c.drawImage('../img/encabezado.png', 0, c._pagesize[1] - 35*mm, (c._pagesize[0]), (35*mm))
                        c.drawImage('../img/pie.png', 0, -2, (c._pagesize[0]), (25*mm))
                        y = 225*mm
                        aux_cont = -30
                    y -= 8*mm
            
            y -= 5*mm

            c.drawString(15*mm, y , 'En caso de tener alguna dificultad para cumplir con los compromisos antes descritos')
            y -= 7*mm
            c.drawString(15*mm, y , 'de forma competa o parcial, por favor comunicarlo al líder de su asociación o al grupo')
            y -= 7*mm
            c.drawString(15*mm, y , 'de investigación queso costeño en el correo quesocostenogr@unimagdalena.edu.co')
            y -= 7*mm
            c.drawString(15*mm, y , '')

            c.save()
    return None

def proveedor(i, model, localization):

    c = canvas.Canvas('prov_'+str(i)+".pdf", pagesize=letter)
    c.drawImage('../img/encabezado.png', 0, c._pagesize[1] - 35*mm, (c._pagesize[0]), (35*mm))
    c.drawImage('../img/pie.png', 0, -2, (c._pagesize[0]), (25*mm))

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(c._pagesize[0]/2, 630 , 'INFORME DE PLANEACIÓN - PROVEEDOR')
    c.setFont("Helvetica-Bold", 14)
    c.drawString(15*mm, 205*mm , 'FECHA:')
    c.drawString(15*mm, 195*mm , 'RESPONSABLE:')
    c.drawString(15*mm, 185*mm , 'DEPARTAMENTO:')

    c.setFont("Helvetica", 14)
    c.drawString(35*mm, 205*mm , str(datetime.date.today().strftime("%d/%m/%Y")))
    c.drawString(56*mm, 195*mm , str(i))
    c.drawString(60*mm, 185*mm , localization)

    c.drawString(15*mm, 170*mm , 'A través de la presente circular se le comunica su compromiso de producción')
    c.drawString(15*mm, 160*mm , 'de LECHE como se relaciona a continuación:')

    c.rect(25*mm, 135*mm, width=75*mm, height=12.5*mm, stroke=1, fill=0)
    c.rect(100*mm, 135*mm, width=50*mm, height=12.5*mm, stroke=1, fill=0)
    c.rect(150*mm, 135*mm, width=30*mm, height=12.5*mm, stroke=1, fill=0)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(62.5*mm, 138*mm , 'PRODUCTOR')
    c.drawCentredString(125*mm, 138*mm , 'CANTIDAD (L)')
    c.drawCentredString(165*mm, 138*mm , 'CHECK')
    c.setFont("Helvetica", 14)

    y = 123*mm
    for k in model.K:
        if pyo.value(model.x1[i, k, 0]) > 0:
            c.rect(25*mm, y, width=75*mm, height=12*mm, stroke=1, fill=0)
            c.rect(100*mm, y, width=50*mm, height=12*mm, stroke=1, fill=0)
            c.rect(150*mm, y, width=30*mm, height=12*mm, stroke=1, fill=0)
            c.drawCentredString(62.5*mm, y+3*mm , str(k))
            c.drawCentredString(125*mm, y+3*mm , str(round(pyo.value(model.x1[i, k, 0]), 1)))
            
            y -= 12
    
    y -= 10*mm

    c.drawString(15*mm, y , 'En caso de tener alguna dificultad para cumplir con los compromisos antes ')
    y -= 10*mm
    c.drawString(15*mm, y , 'descritos de forma competa o parcial, por favor comunicarlo al líder de su ')
    y -= 10*mm
    c.drawString(15*mm, y , 'asociación o al grupo de investigación queso costeño en el correo ')
    y -= 10*mm
    c.drawString(15*mm, y , 'quesocostenogr@unimagdalena.edu.co')

    # print(c._pagesize)
    c.save()
    return None

def productor(k, model, localization):
    c = canvas.Canvas('prod_'+str(k)+".pdf", pagesize=letter)
    c.drawImage('../img/encabezado.png', 0, c._pagesize[1] - 35*mm, (c._pagesize[0]), (35*mm))
    c.drawImage('../img/pie.png', 0, -2, (c._pagesize[0]), (25*mm))

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(c._pagesize[0]/2, 650 , 'INFORME DE PLANEACIÓN - PRODUCTOR')
    c.setFont("Helvetica-Bold", 14)
    c.drawString(15*mm, 215*mm , 'FECHA:')
    c.drawString(15*mm, 205*mm , 'RESPONSABLE:')
    c.drawString(15*mm, 195*mm , 'DEPARTAMENTO:')

    c.setFont("Helvetica", 14)
    c.drawString(35*mm, 215*mm , str(datetime.date.today().strftime("%d/%m/%Y")))
    c.drawString(56*mm, 205*mm , str(k))
    c.drawString(60*mm, 195*mm , localization)

    c.setFont("Helvetica", 12)
    c.drawString(15*mm, 180*mm , 'A través de la presente circular se le comunica su compromiso de producción de QUESO')
    c.drawString(15*mm, 173*mm , 'como se relaciona a continuación:')

    # Tabla a recibir

    c.rect(25*mm, 160*mm, width=75*mm, height=8*mm, stroke=1, fill=0)
    c.rect(100*mm, 160*mm, width=50*mm, height=8*mm, stroke=1, fill=0)
    c.rect(150*mm, 160*mm, width=30*mm, height=8*mm, stroke=1, fill=0)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(62.5*mm, 162*mm , 'PROVEEDOR')
    c.drawCentredString(125*mm, 162*mm , 'CANTIDAD (L)')
    c.drawCentredString(165*mm, 162*mm , 'CHECK')
    c.setFont("Helvetica", 12)

    y = 152*mm
    for i in model.I:
        if pyo.value(model.x1[i, k, 0]) > 0:
            c.rect(25*mm, y, width=75*mm, height=8*mm, stroke=1, fill=0)
            c.rect(100*mm, y, width=50*mm, height=8*mm, stroke=1, fill=0)
            c.rect(150*mm, y, width=30*mm, height=8*mm, stroke=1, fill=0)
            c.drawCentredString(62.5*mm, y+2*mm , str(i))
            c.drawCentredString(125*mm, y+2*mm , str(round(pyo.value(model.x1[i, k, 0]), 1)))
            
            y -= 8*mm
    
    y -= 5*mm

    #Tabla a entregar

    c.rect(25*mm, y, width=75*mm, height=8*mm, stroke=1, fill=0)
    c.rect(100*mm, y, width=50*mm, height=8*mm, stroke=1, fill=0)
    c.rect(150*mm, y, width=30*mm, height=8*mm, stroke=1, fill=0)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(62.5*mm, y+2*mm , 'ACOPIO')
    c.drawCentredString(125*mm, y+2*mm , 'CANTIDAD (Kg)')
    c.drawCentredString(165*mm, y+2*mm , 'CHECK')
    c.setFont("Helvetica", 12)

    y -= 8*mm
    for r in model.R:
        if pyo.value(model.x3[k, r, 0]) > 0:
            c.rect(25*mm, y, width=75*mm, height=8*mm, stroke=1, fill=0)
            c.rect(100*mm, y, width=50*mm, height=8*mm, stroke=1, fill=0)
            c.rect(150*mm, y, width=30*mm, height=8*mm, stroke=1, fill=0)
            c.drawCentredString(62.5*mm, y+2*mm , str(r))
            c.drawCentredString(125*mm, y+2*mm , str(round(pyo.value(model.x3[k, r, 0]), 2)))
            
            y -= 8*mm
    
    y -= 5*mm

    c.drawString(15*mm, y , 'En caso de tener alguna dificultad para cumplir con los compromisos antes descritos')
    y -= 7*mm
    c.drawString(15*mm, y , 'de forma competa o parcial, por favor comunicarlo al líder de su asociación o al grupo')
    y -= 7*mm
    c.drawString(15*mm, y , 'de investigación queso costeño en el correo quesocostenogr@unimagdalena.edu.co')
    y -= 7*mm
    c.drawString(15*mm, y , '')

    c.save()
    return None


def acopio(r, model, localization):
    c = canvas.Canvas('acop_'+str(r)+".pdf", pagesize=letter)
    c.drawImage('../img/encabezado.png', 0, c._pagesize[1] - 35*mm, (c._pagesize[0]), (35*mm))
    c.drawImage('../img/pie.png', 0, -2, (c._pagesize[0]), (25*mm))

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(c._pagesize[0]/2, 650 , 'INFORME DE PLANEACIÓN - ACOPIO')
    c.setFont("Helvetica-Bold", 14)
    c.drawString(15*mm, 215*mm , 'FECHA:')
    c.drawString(15*mm, 205*mm , 'RESPONSABLE:')
    c.drawString(15*mm, 195*mm , 'DEPARTAMENTO:')

    c.setFont("Helvetica", 14)
    c.drawString(35*mm, 215*mm , str(datetime.date.today().strftime("%d/%m/%Y")))
    c.drawString(56*mm, 205*mm , str(r))
    c.drawString(60*mm, 195*mm , localization)

    c.setFont("Helvetica", 12)
    c.drawString(15*mm, 180*mm , 'A través de la presente circular se le comunica su compromiso de acopio de QUESO')
    c.drawString(15*mm, 173*mm , 'como se relaciona a continuación:')

    # Tabla a recibir

    c.rect(25*mm, 160*mm, width=75*mm, height=8*mm, stroke=1, fill=0)
    c.rect(100*mm, 160*mm, width=50*mm, height=8*mm, stroke=1, fill=0)
    c.rect(150*mm, 160*mm, width=30*mm, height=8*mm, stroke=1, fill=0)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(62.5*mm, 162*mm , 'PRODUCTOR')
    c.drawCentredString(125*mm, 162*mm , 'CANTIDAD (Kg)')
    c.drawCentredString(165*mm, 162*mm , 'CHECK')
    c.setFont("Helvetica", 12)

    y = 152*mm
    for k in model.K:
        if pyo.value(model.x3[k, r, 0]) > 0:
            c.rect(25*mm, y, width=75*mm, height=8*mm, stroke=1, fill=0)
            c.rect(100*mm, y, width=50*mm, height=8*mm, stroke=1, fill=0)
            c.rect(150*mm, y, width=30*mm, height=8*mm, stroke=1, fill=0)
            c.drawCentredString(62.5*mm, y+2*mm , str(k))
            c.drawCentredString(125*mm, y+2*mm , str(round(pyo.value(model.x3[k, r, 0]), 2)))
            
            y -= 8*mm
    
    y -= 5*mm

    #Tabla a entregar

    c.rect(25*mm, y, width=75*mm, height=8*mm, stroke=1, fill=0)
    c.rect(100*mm, y, width=50*mm, height=8*mm, stroke=1, fill=0)
    c.rect(150*mm, y, width=30*mm, height=8*mm, stroke=1, fill=0)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(62.5*mm, y+2*mm , 'CLIENTE')
    c.drawCentredString(125*mm, y+2*mm , 'CANTIDAD (Kg)')
    c.drawCentredString(165*mm, y+2*mm , 'CHECK')
    c.setFont("Helvetica", 12)

    y -= 8*mm
    for m in model.M:
        if pyo.value(model.x4[r, m, 0]) > 0:
            c.rect(25*mm, y, width=75*mm, height=8*mm, stroke=1, fill=0)
            c.rect(100*mm, y, width=50*mm, height=8*mm, stroke=1, fill=0)
            c.rect(150*mm, y, width=30*mm, height=8*mm, stroke=1, fill=0)
            c.drawCentredString(62.5*mm, y+2*mm , str(m))
            c.drawCentredString(125*mm, y+2*mm , str(round(pyo.value(model.x4[r, m, 0]), 2)))
            
            y -= 8*mm
    
    y -= 5*mm

    c.drawString(15*mm, y , 'En caso de tener alguna dificultad para cumplir con los compromisos antes descritos')
    y -= 7*mm
    c.drawString(15*mm, y , 'de forma competa o parcial, por favor comunicarlo al líder de su asociación o al grupo')
    y -= 7*mm
    c.drawString(15*mm, y , 'de investigación queso costeño en el correo quesocostenogr@unimagdalena.edu.co')
    y -= 7*mm
    c.drawString(15*mm, y , '')

    c.save()
    return None