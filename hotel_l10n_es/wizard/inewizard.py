# -*- coding: utf-8 -*-

from openerp import models, fields, api
import base64  
import datetime

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
    if month = 0:
        month = 12
    return month

class Wizard(models.TransientModel):
    _name = 'ine.wizard'

    download_date = fields.Date('Date to generate the file',required=True)
    download_num = fields.Char('Correlative number',required=True,size=3,help='Number provided by the police')
    txt_filename = fields.Char()
    txt_binary = fields.Binary()
    ine_month = fields.Selection([(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
                          (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), 
                          (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December'), ], 
                          string='Month', default=get_month())
    ine_year = fields.Selection(get_years(), default=get_year(), string='Year')


    @api.one
    def generate_file(self):
        content = 'Hola mundo'
      
        return self.write({
            'txt_filename': 'compaine' +'.'+ self.download_num,
            'txt_binary': base64.encodestring(content)
            })      