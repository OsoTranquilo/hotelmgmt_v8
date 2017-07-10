# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2017 Solucións Aloxa S.L. <info@aloxa.eu>
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields


class VirtualRoomAvailability(models.Model):
    _name = 'virtual.room.availability'

    virtual_room_id = fields.Many2one('hotel.virtual.room', 'Virtual Room', required=True)
    avail = fields.Integer('Avail', default=-1)
    no_ota = fields.Boolean('No OTA', default=False)
    booked = fields.Boolean('Booked', default=False)
    date = fields.Date('Date', required=True)
