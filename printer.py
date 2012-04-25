from wx.html import HtmlEasyPrinting
import datetime

class Printer(HtmlEasyPrinting):
    def __init__(self):
        HtmlEasyPrinting.__init__(self)

    def GetHtmlText(self,text):

        html_text = text.replace('\n\n','<P>')
        html_text = text.replace('\n', '<BR>')
        return html_text

    def Print(self, text, doc_name):
        self.SetHeader(doc_name)
        self.PrintText(self.GetHtmlText(text),doc_name)

    def PreviewText(self, text, doc_name):
        self.SetHeader(doc_name)
        HtmlEasyPrinting.PreviewText(self, self.GetHtmlText(text))


class PlanillaCobrador():
    def __init__(self, cobrador):
        self.cobrador = cobrador
        self.printer = Printer()
        self.doc_name = "Planilla de clientes activos del Cobrador %s, el dia %d/%d/%d" % (self.cobrador.nombre.upper(), datetime.date.today().day, datetime.date.today().month, datetime.date.today().year)

    def Imprimir(self):
        self.printer.Print(self.GetHtml(), self.doc_name)

    def VistaPrevia(self):
        self.printer.PreviewText(self.GetHtml(), self.doc_name)

    def GetHtml(self):
        TOTAL = 0
        html = "<html><table width=100\% cellpadding=6 border=1 frame=border cellspacing=0'>"
        html += "<tr><th>Nro</th><th>Nombre</th><th>Cuota</th><th>Pago</th></tr>"
        for i in self.cobrador.clientes:
            if i.saldo != 0:
                TOTAL += i.cuota
                html += "<tr><td width=50>%d</td><td>%s</td><td width=100>$%g</td><td></td></tr>" % (i.id, i.nombre, i.cuota)
        html += "</table><h5 align=right >TOTAL    RECAUDADO: _____________________</h5></html>"

        return html

class PlanillaCobradorMorosos():
    def __init__(self, cobrador):
        self.cobrador = cobrador
        self.printer = Printer()
        self.doc_name = "Planilla de clientes morosos del Cobrador %s, el dia %d/%d/%d" % (self.cobrador.nombre.upper(), datetime.date.today().day, datetime.date.today().month, datetime.date.today().year)

    def Imprimir(self):
        self.printer.Print(self.GetHtml(), self.doc_name)

    def VistaPrevia(self):
        self.printer.PreviewText(self.GetHtml(), self.doc_name)

    def GetHtml(self):
        TOTAL = 0
        html = "<html><table width=100\% cellpadding=6 border=1 frame=border cellspacing=0'>"
        html += "<tr><th>Nro</th><th>Nombre</th><th>Atrasado</th><th>Cuota Comun</th></tr>"
        for i in self.cobrador.clientes:
            if i.esMoroso():
                TOTAL += i.cuota
                html += "<tr><td width=50>%d</td><td>%s</td><td width=100>$%g</td><td>%g</td></tr>" % (i.id, i.nombre, i.saldo_atrasado, i.cuota)
        html += "</table></html>"

        return html

class InformeSaldos():
    def __init__(self, clientes):
        self.clientes = clientes
        self.printer = Printer()
        self.doc_name = "Informe de Saldos de clientes al dia %d/%d/%d" % (datetime.date.today().day, datetime.date.today().month, datetime.date.today().year)

    def Imprimir(self):
        self.printer.Print(self.GetHtml(), self.doc_name)

    def VistaPrevia(self):
        self.printer.PreviewText(self.GetHtml(), self.doc_name)

    def GetHtml(self):
        html = "<html><table width=100\% cellpadding=6 border=1 frame=border cellspacing=0'>"
        html += "<tr><th>Nro</th><th>Nombre</th><th>Productos</th><th>Saldo</th></tr>"
        for i in self.clientes:
            if i.saldo > 0:
                html += "<tr><td width=50>%d</td><td>%s</td><td width=100>%d</td><td>$%g</td></tr>" % (i.id, i.nombre, len(i.productos), i.saldo)
        html += "</table></html>"

        return html


class InformeSaldosAtrasados():
    def __init__(self, clientes):
        self.clientes = clientes
        self.printer = Printer()
        self.doc_name = "Informe de Saldos Atrasados de clientes morosos al dia %d/%d/%d" % (datetime.date.today().day, datetime.date.today().month, datetime.date.today().year)

    def Imprimir(self):
        self.printer.Print(self.GetHtml(), self.doc_name)

    def VistaPrevia(self):
        self.printer.PreviewText(self.GetHtml(), self.doc_name)

    def GetHtml(self):
        html = "<html><table width=100\% cellpadding=6 border=1 frame=border cellspacing=0'>"
        html += "<tr><th>Nro</th><th>Nombre</th><th>Saldo</th><th>Atrasado</th></tr>"
        for i in self.clientes:
            if i.saldo_atrasado > 0:
                html += "<tr><td width=50>%d</td><td>%s</td><td width=100>$%g</td><td>$%g</td></tr>" % (i.id, i.nombre, i.saldo, i.saldo_atrasado)
        html += "</table></html>"

        return html