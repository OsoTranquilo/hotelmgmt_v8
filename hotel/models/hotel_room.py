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
#import json
from openerp import models, fields, api, _


class HotelRoom(models.Model):
    _name = 'hotel.room'
    _description = 'Hotel Room'

#     @api.multi
#     @api.depends('categ_id')
#     def _compute_price_virtual_room_domain(self):
#         for rec in self:
#             rec.price_virtual_room_domain = json.dumps(
#                 ['|', ('room_ids.id', '=', rec.id), ('room_type_ids.cat_id.id', '=', rec.categ_id.id)]
#             )

    product_id = fields.Many2one('product.product', 'Product_id',
                                 required=True, delegate=True,
                                 ondelete='cascade')
    floor_id = fields.Many2one('hotel.floor', 'Ubication',
                               help='At which floor the room is located.')
    max_adult = fields.Integer('Max Adult')
    max_child = fields.Integer('Max Child')
    room_amenities = fields.Many2many('hotel.room.amenities', 'temp_tab',
                                      'room_amenities', 'rcateg_id',
                                      string='Room Amenities',
                                      help='List of room amenities. ')
    capacity = fields.Integer('Capacity')
    shared_room = fields.Boolean('Shared Room')
    to_be_cleaned = fields.Boolean('To be Cleaned')
    virtual_rooms = fields.Many2many('hotel.virtual.room', string='Virtual Rooms')
    sale_price_type = fields.Selection([
        ('fixed', 'Fixed Price'),
        ('vroom', 'Virtual Room'),
    ], 'Price Type', default='fixed', required=True)
    price_virtual_room = fields.Many2one('hotel.virtual.room', 'Price Virtual Room',
                                         help='Price will be based on selected Virtual Room')
#     price_virtual_room_domain = fields.Char(
#         compute=_compute_price_virtual_room_domain,
#         readonly=True,
#         store=False,
#     )

    @api.onchange('categ_id')
    def price_virtual_room_domain(self):
        return {
            'domain': {
                'price_virtual_room': ['|', ('room_ids.id', '=', self._origin.id), ('room_type_ids.cat_id.id', '=', self.categ_id.id)]
            }
        }
