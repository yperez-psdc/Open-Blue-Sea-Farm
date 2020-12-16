# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import logging
class Teamv2(models.Model):
	_name = 'helpdesk.team'
	_inherit = 'helpdesk.team'

	claim_subtypes = fields.Boolean(string ='Claim subtypes')


class Subtypes(models.Model):
	_name = 'helpdesk.ticket'
	_inherit = 'helpdesk.ticket'

	sale_order_products = fields.Many2many('sale.order.line',  relation='help_desk_rel', column1='product_id' )
	# domain="[('order_id','=','sale_order_id')]"

	# @api.onchange('sale_order_id')
	# def _onchange_product(self):
    # 	return ('domain': {'sale_order_products': [('order_id', '=', self.sale_order_id.id)]}

	subtype_selection = fields.Selection([
		('product', 'Product Quality and/or Food Safety'),
		('invoicing', 'Invoicing'),
		('logistics', 'Logistics'),
		('customer', 'Customer Service')
		],
		string='Query subtype'
		)
		#,required=True

	subtype_check = fields.Boolean(string='subtype check', related='team_id.claim_subtypes')

	#	Product Quality and/or Food Safety
	blown_bags = fields.Boolean(string='Blown Bags')
	broken_boxes = fields.Boolean(string='Broken Boxes')
	broken_vacuum_seal = fields.Boolean(string='Broken Vacuum Seal')
	fatty_composition = fields.Boolean(string='Fatty Composition')
	red_flesh = fields.Boolean(string='Red Flesh')
	warm_temperature = fields.Boolean(string='Warm Temperature')
	weight_discrepancy = fields.Boolean(string='Weight Discrepancy')
	volume_error = fields.Boolean(string='Volume error')
	old_product = fields.Boolean(string='Old Product')
	discoloration = fields.Boolean(string='Discoloration')
	food_safety_issues = fields.Boolean(string='Food Safety Issues')


	# 	Invoicing
	delivery_format = fields.Boolean(string='Incorrect Delivery Format')
	delivery_size = fields.Boolean(string='Incorrect Delivery Size')
	price_quote = fields.Boolean(string='Incorrect Price Quote')
	charge_error = fields.Boolean(string='Sample Charge Error')


	#	 Logistics
	log_old_product = fields.Boolean(string='Old Product')
	storage_error = fields.Boolean(string='Storage Facility Error')
	log_error = fields.Boolean(string='Logistics Delivery Error')
	certificate_delay = fields.Boolean(string='Health Certificate Delays')

	#	Customer Service
	cancelled_harvest = fields.Boolean(string='Cancelled Harvest')
	cus_didnt_pick_up = fields.Boolean(string='Customer did not pick up')
	customer_other = fields.Text(string='Other')


