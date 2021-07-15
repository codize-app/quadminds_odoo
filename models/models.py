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

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def create_qm_order(self):
        if self.partner_id.comment:
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

        payload = [
            {
                "timeWindow": [],
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
