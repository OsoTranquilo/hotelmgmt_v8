# -*- coding: utf-8 -*-

from openerp import models, fields, api
import base64  
import datetime
import calendar
import xml.etree.cElementTree as ET

import logging
_logger=logging.getLogger(__name__)

def get_years():
    year_list = []
    for i in range(2016, get_year()+1):
        year_list.append((i, str(i)))
    return year_list

def get_year():
    now = datetime.datetime.now()
    return int(now.year)

def get_month():
    now = datetime.datetime.now()
    month = int(now.month)-1
    if month <= 0:
        month = 12
    return month

class Wizard(models.TransientModel):
    _name = 'ine.wizard'

    txt_filename = fields.Char()
    txt_binary = fields.Binary()
    ine_month = fields.Selection([(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
                          (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), 
                          (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December'), ], 
                          string='Month', default=get_month())
    ine_year = fields.Selection(get_years(), default=get_year(), string='Year')

    @api.one
    def generate_file(self):
        compan = self.env.user.company_id
        #compan.rooms
        #compan.seats

        encuesta = ET.Element("ENCUESTA")
        cabezera = ET.SubElement(encuesta, "CABEZERA")

        fecha = ET.SubElement(cabezera,"FECHA_REFERENCIA")
        ET.SubElement(fecha, "MES").text = '{:02d}'.format(self.ine_month)
        ET.SubElement(fecha, "ANYO").text = str(self.ine_year)

        month_end_date=datetime.datetime(self.ine_year,self.ine_month,1) + datetime.timedelta(days=calendar.monthrange(self.ine_year,self.ine_month)[1] - 1)
        ET.SubElement(cabezera,"DIAS_ABIERTO_MES_REFERENCIA").text = str(month_end_date.day)

        ET.SubElement(cabezera,"RAZON_SOCIAL").text = compan.name
        ET.SubElement(cabezera,"NOMBRE_ESTABLECIMIENTO").text = compan.property_name
        ET.SubElement(cabezera,"CIF_NIF").text = compan.vat
        ET.SubElement(cabezera,"NUMERO_REGISTRO").text = compan.tourism
        ET.SubElement(cabezera,"DIRECCION").text = compan.street
        ET.SubElement(cabezera,"CODIGO_POSTAL").text = compan.zip
        ET.SubElement(cabezera,"LOCALIDAD").text = compan.city
        ET.SubElement(cabezera,"MUNICIPIO").text = compan.city
        ET.SubElement(cabezera,"PROVINCIA").text = compan.state_id.display_name
        ET.SubElement(cabezera,"TELEFONO_1").text = compan.phone
        ET.SubElement(cabezera,"TIPO").text = compan.category_id.name
        ET.SubElement(cabezera,"CATEGORIA").text = compan.vat
        ET.SubElement(cabezera,"HABITACIONES").text = str(compan.rooms)
        ET.SubElement(cabezera,"PLAZAS_DISPONIBLES_SIN_SUPLETORIAS").text = str(compan.seats)
        ET.SubElement(cabezera,"URL").text = compan.website

        alojamiento = ET.SubElement(encuesta, "ALOJAMIENTO")
        #Bucle de RESIDENCIA

        habitaciones = ET.SubElement(encuesta, "HABITACIONES")
        #Bucle de HABITACIONES_MOVIMIENTO

        personal = ET.SubElement(encuesta, "PERSONAL_OCUPADO")
        ET.SubElement(personal,"PERSONAL_NO_REMUNERADO").text = '0'
        ET.SubElement(personal,"PERSONAL_REMUNERADO_FIJO").text = str(compan.permanentstaff)
        ET.SubElement(personal,"PERSONAL_REMUNERADO_EVENTUAL").text = str(compan.eventualstaff)

        tree = ET.ElementTree(encuesta)

        xmlstr = '<?xml version="1.0" encoding="ISO-8859-1"?>'
        xmlstr += ET.tostring(encuesta)            
        file=base64.encodestring( xmlstr )
        return self.write({
             'txt_filename': 'INE_'+str(self.ine_month)+'_'+str(self.ine_year) +'.'+ 'xml',
             'txt_binary': base64.encodestring(xmlstr)
             })