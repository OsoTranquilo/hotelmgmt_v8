# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-Today Serpent Consulting Services PVT. LTD.
#    (<http://www.serpentcs.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
# ---------------------------------------------------------------------------
from openerp.exceptions import except_orm, UserError, ValidationError
from openerp.tools import misc, DEFAULT_SERVER_DATETIME_FORMAT
from openerp import models, fields, api, _
from openerp import workflow
from decimal import Decimal
import datetime
import urllib2
import time


class VirtualRoom(models.Model):
    _name ='hotel.virtual.room'
    _inherits = {'product.product':'product_id'}
    
    @api.depends('room_ids','room_type_ids')
    def _compute_total_rooms(self):
	for r in self:
		count = 0
		count += len(r.room_ids) #Rooms linked directly
		room_categories	= r.room_type_ids.mapped('cat_id.id') 		 
		count += self.env['hotel.room'].search_count([('categ_id.id','in',room_categories)])#Rooms linked through room type
		r.total_rooms_count = count
    
    @api.constrains('room_ids','room_type_ids')
    def _check_duplicated_rooms(self):
	warning_msg = ""
	for r in self:
		room_categories	= self.room_type_ids.mapped('cat_id.id')
		if self.room_ids & self.env['hotel.room'].search([('categ_id.id','in',room_categories)]):
			room_ids = self.room_ids & self.env['hotel.room'].search([('categ_id.id','in',room_categories)]) 
			rooms_name = ','.join(str(x.name) for x in room_ids)
			warning_msg += 'You can not enter the same room in duplicate (check the room types) %s' % rooms_name
			raise models.ValidationError(warning_msg)

    @api.constrains('max_real_rooms','room_ids','room_type_ids')
    def _check_max_rooms(self):
	warning_msg = ""
	for r in self:
		if self.max_real_rooms > self.total_rooms_count:
			warning_msg += 'The Maxime rooms allowed can not be greate than total rooms count'
			raise models.ValidationError(warning_msg)
    
    virtual_code = fields.Char('Code')
    room_ids = fields.Many2many('hotel.room',string='Rooms')
    room_type_ids = fields.Many2many('hotel.room.type',string='Room Types')
    total_rooms_count = fields.Integer(compute='_compute_total_rooms')
    product_id = fields.Many2one('product.product', 'Product_id',
                                 required=True, delegate=True,
                                 ondelete='cascade')
    service_ids = fields.Many2many('hotel.services',string='Included Services')
    max_real_rooms = fields.Integer('Max Room Allowed')
    product_id = fields.Many2one(
		'product.product',
		ondelete='cascade')
    
    
    
    
    
    

    
