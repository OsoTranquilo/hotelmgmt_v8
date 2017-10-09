# -*- coding: utf-8 -*-

from openerp import models, fields, api
import base64  
import datetime
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


    # @api.one
    # def generate_file(self):
    #     content = 'Hola mundo'
      
    #     return self.write({
    #         'txt_filename': 'compaine' +'.'+ 'txt',
    #         'txt_binary': base64.encodestring(content)
    #         }) 



    @api.one
    def generate_file(self):
    #def generate_file(self, cr, uid, ids, context=None):
        encuesta = ET.Element("ENCUESTA")
        cabezera = ET.SubElement(encuesta, "CABEZERA")

        ET.SubElement(cabezera, "field1", name="blah").text = "some value1"
        ET.SubElement(cabezera, "field2", name="asdfasd").text = "some vlaue2"

        tree = ET.ElementTree(encuesta)

        xmlstr = '<?xml version="1.0" encoding="ISO-8859-1"?>'
        xmlstr += ET.tostring(encuesta)            
        file=base64.encodestring( xmlstr )
        return self.write({
             'txt_filename': 'ine_'+str(get_year())+'_'+str(get_month()) +'.'+ 'xml',
             'txt_binary': base64.encodestring(xmlstr)
             })           



        #tree.write(get_year()+"filename.xml") 

           