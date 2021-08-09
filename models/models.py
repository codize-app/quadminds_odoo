# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

import requests
import json

import time
from datetime import datetime

class ResCompany(models.Model):
    _inherit = 'res.company'

    qm_apikey = fields.Char(string='QuadMinds API Key', help='QuadMinds API Key')

class ResPartner(models.Model):
    _inherit = 'res.partner'

    qm_code = fields.Char('QM Code')
    qm_hour_from = fields.Selection([
        ('00:00', '00:00'),
        ('01:00', '01:00'),
        ('02:00', '02:00'),
        ('03:00', '03:00'),
        ('04:00', '04:00'),
        ('05:00', '05:00'),
        ('06:00', '06:00'),
        ('07:00', '07:00'),
        ('08:00', '08:00'),
        ('09:00', '09:00'),
        ('10:00', '10:00'),
        ('11:00', '11:00'),
        ('12:00', '12:00'),
        ('13:00', '13:00'),
        ('14:00', '14:00'),
        ('15:00', '15:00'),
        ('16:00', '16:00'),
        ('17:00', '17:00'),
        ('18:00', '18:00'),
        ('19:00', '19:00'),
        ('20:00', '20:00'),
        ('21:00', '21:00'),
        ('22:00', '22:00'),
        ('23:00', '23:00'),
    ], 'Hour From')
    qm_hour_to = fields.Selection([
        ('00:00', '00:00'),
        ('01:00', '01:00'),
        ('02:00', '02:00'),
        ('03:00', '03:00'),
        ('04:00', '04:00'),
        ('05:00', '05:00'),
        ('06:00', '06:00'),
        ('07:00', '07:00'),
        ('08:00', '08:00'),
        ('09:00', '09:00'),
        ('10:00', '10:00'),
        ('11:00', '11:00'),
        ('12:00', '12:00'),
        ('13:00', '13:00'),
        ('14:00', '14:00'),
        ('15:00', '15:00'),
        ('16:00', '16:00'),
        ('17:00', '17:00'),
        ('18:00', '18:00'),
        ('19:00', '19:00'),
        ('20:00', '20:00'),
        ('21:00', '21:00'),
        ('22:00', '22:00'),
        ('23:00', '23:00'),
    ], 'Hour To')

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def create_qm_order(self):
        if self.partner_id.qm_code:
            url = "https://saas.quadminds.com/api/v2/pois/" + self.partner_id.qm_code
            headers = {
                "Accept": "application/json",
                "x-saas-apikey": self.company_id.qm_apikey
            }
            response = requests.request("GET", url, headers=headers)

            if response.status_code == 200:
                self.send_order(response.json()['data']['_id'])
            else:
                raise ValidationError('Error ' + str(response.status_code) + ': ' + response.json()['message'])

        else:
            raise ValidationError('Customer must be Code!')

    def send_order(self, poid):
        url = "https://saas.quadminds.com/api/v2/orders"

        if not self.origin:
            raise ValidationError('Picking needs Origin for QuadMinds identification!')

        timeWindow = []

        if self.partner_id.qm_hour_from and self.partner_id.qm_hour_to:
            timeWindow = [{'from': self.partner_id.qm_hour_from, 'to': self.partner_id.qm_hour_to}]

        payload = [
            {
                "timeWindow": timeWindow,
                "orderItems": [],
                "orderMeasures": [],
                "code": self.origin,
                "date": str(datetime.strptime(str(self.scheduled_date), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')),
                "poiId": poid,
                "operation": "PEDIDO"
            }
        ]
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "x-saas-apikey": self.company_id.qm_apikey
        }

        response = requests.request("POST", url, json=payload, headers=headers)

        if response.status_code == 200:
            raise ValidationError('Order created successfully in QuadMinds')
        else:
            raise ValidationError('Error ' + str(response.status_code) + ': ' + response.json()['message'])
