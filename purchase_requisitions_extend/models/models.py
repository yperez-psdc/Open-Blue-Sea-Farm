# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError

class MaterialPurchaseRequisition(models.Model):
    _inherit = "material.purchase.requisition"
    

    def _get_default_employee_id(self):
        logged_in_user = self.env.user
        logged_in_employee = self.env['hr.employee'].sudo().search([('user_id', '=', logged_in_user.id)], limit=1)
        if logged_in_employee:
            return logged_in_employee.id


    @api.onchange('requisition_responsible_id')
    def _get_default_approver(self):
        user_ids = self.env['res.users'].search([])
        user_eligible = []
        for user in user_ids:
            if user.has_group('bi_material_purchase_requisitions.group_requisition_department_manager'):
                user_eligible.append(user.id)
        return {'domain':{'requisition_responsible_id':[('id','in',user_eligible)]}}
    

    @api.onchange('employee_id')
    def get_department(self):
        self.department_id = self.employee_id.department_id.id

    employee_id = fields.Many2one('hr.employee',string="Employee",required=True,default=_get_default_employee_id)
    department_id = fields.Many2one('hr.department',string="Department",required=True)
    requisition_responsible_id  = fields.Many2one('res.users',string="Requisition Responsible")

class PurchaseOrder(models.Model):      
    _inherit = 'purchase.order'   

    def calculate_validation_purchasing_user(self):
        if self:
            for rec in self:
                if rec.validation_purchasing_user ==True:
                    rec.compute_validation_purchasing_user = True
                elif rec.validation_level_required in ['one', 'two', 'three','four', 'five', False] :
                    rec.compute_validation_purchasing_user =True
                elif rec.state in ["draft","sent","to_approve"]:
                    rec.compute_validation_purchasing_user =False

    def calculate_validation_purchasing_manager(self):
        if self:
            for rec in self:
                if rec.validation_purchasing_manager ==True:
                    rec.compute_validation_purchasing_manager = True
                elif rec.validation_level_required in ['no', 'one', False]:
                    rec.compute_validation_purchasing_manager =True
                elif rec.state in ["draft","sent","to_approve"]: 
                    rec.compute_validation_purchasing_manager = False


    def calculate_validation_department_manager(self):
        if self:
            for rec in self:
                if rec.validation_department_manager ==True:
                    rec.compute_validation_department_manager = True
                elif rec.validation_level_required in ['no', 'one', False]:
                    rec.compute_validation_department_manager =True
                elif rec.state in ["draft","sent","to_approve"]:
                    rec.compute_validation_department_manager =False


    def calculate_validation_director(self):
        if self:
            for rec in self:
                if rec.validation_director ==True:
                    rec.compute_validation_director = True
                elif rec.validation_level_required in ['no', 'one', 'two', False]:
                    rec.compute_validation_director =True
                elif rec.state in ["draft","sent","to_approve"]:
                    rec.compute_validation_director =False

    def calculate_validation_cfo_or_coo(self):
        if self:
            for rec in self:
                if rec.validation_cfo_or_coo ==True:
                    rec.compute_validation_cfo_or_coo = True
                elif rec.validation_level_required in ['no', 'one', 'two', 'three', False]:
                    rec.compute_validation_cfo_or_coo =True
                elif rec.state in ["draft","sent","to_approve"]:
                    rec.compute_validation_cfo_or_coo =False


    def calculate_validation_ceo(self):
        if self:
            for rec in self:
                if rec.validation_ceo ==True:
                    rec.compute_validation_ceo = True
                elif rec.validation_level_required in ['no', 'one', 'two', 'three', 'four', False]:
                    rec.compute_validation_ceo =True
                elif rec.state in ["draft","sent","to_approve"]:
                    rec.compute_validation_ceo =False


    compute_validation_purchasing_user = fields.Boolean(string="Purchasing User", compute='calculate_validation_purchasing_user')
    compute_validation_purchasing_manager = fields.Boolean(string="Purchasing Manager", compute='calculate_validation_purchasing_manager')
    compute_validation_department_manager = fields.Boolean(string="Department Manager", compute='calculate_validation_department_manager')
    compute_validation_director = fields.Boolean(string="Director", compute='calculate_validation_director')
    compute_validation_cfo_or_coo = fields.Boolean(string="CFO or COO", compute='calculate_validation_cfo_or_coo')
    compute_validation_ceo = fields.Boolean(string="CEO", compute='calculate_validation_ceo')


    validation_purchasing_user = fields.Boolean(string="Purchasing User", default=False)
    validation_purchasing_manager = fields.Boolean(string="Purchasing Manager", default=False)
    validation_department_manager = fields.Boolean(string="Department Manager", default=False)
    validation_director = fields.Boolean(string="Director", default=False)
    validation_cfo_or_coo = fields.Boolean(string="CFO or COO", default=False)
    validation_ceo = fields.Boolean(string="CEO", default=False)

    def _compute_validation_level_required(self):
        for rec in self:
            if rec.amount_total <= 300:
                rec.validation_level_required = 'no'
            elif rec.amount_total > 300 and rec.amount_total <=5000:
                rec.validation_level_required = 'two'
            elif rec.amount_total > 5000 and rec.amount_total <= 10000:
                rec.validation_level_required = 'three'
            elif rec.amount_total > 10000 and rec.amount_total <=100000:
                rec.validation_level_required = 'four'
            elif rec.amount_total > 100000:
                rec.validation_level_required = 'five'


    validation_level_required = fields.Selection([
        ('no', 'No'),
        ('one', 'one'),
        ('two', 'two'),
        ('three', 'three'),
        ('four', 'four'),
        ('five', 'five'),
        ],string = "Validation Level Required", compute='_compute_validation_level_required')


    def button_confirm(self):
        for rec in self:
            if rec.validation_level_required == 'no':
                if rec.validation_purchasing_user ==True:
                    super(PurchaseOrder, self).button_confirm()
                else:
                    if rec.validation_purchasing_user ==False:
                        raise ValidationError(_("Purchasing User Approval Required"))

            elif rec.validation_level_required == 'two':
                if rec.validation_purchasing_manager ==True and rec.validation_department_manager==True:
                    super(PurchaseOrder, self).button_confirm()
                else:
                    if rec.validation_purchasing_manager==False:
                        raise ValidationError(_("Purchasing Manager Approval Required"))
                    elif rec.validation_department_manager==False:
                        raise ValidationError(_("Department Manager Approval Required"))
                        
            elif rec.validation_level_required == 'three':
                if rec.validation_purchasing_manager ==True and rec.validation_department_manager==True and rec.validation_director==True :
                    super(PurchaseOrder, self).button_confirm()
                else:
                    if rec.validation_purchasing_manager==False:
                        raise ValidationError(_("Purchasing Manager Approval Required"))
                    elif rec.validation_department_manager==False:
                        raise ValidationError(_("Department Manager Approval Required"))
                    elif rec.validation_director==False:
                        raise ValidationError(_("Director Approval Required"))
            elif rec.validation_level_required == 'four':
                if rec.validation_purchasing_manager ==True and rec.validation_department_manager==True and rec.validation_director==True and rec.validation_cfo_or_coo==True:
                    super(PurchaseOrder, self).button_confirm()
                else:
                    if rec.validation_purchasing_manager==False:
                        raise ValidationError(_("Purchasing Manager Approval Required"))
                    elif rec.validation_department_manager==False:
                        raise ValidationError(_("Department Manager Approval Required"))
                    elif rec.validation_director==False:
                        raise ValidationError(_("Director Approval Required"))
                    elif rec.validation_cfo_or_coo==False:
                        raise ValidationError(_("CFO/COO Approval Required"))
                        
            elif rec.validation_level_required == 'five':
                if rec.validation_purchasing_manager ==True and rec.validation_department_manager==True and rec.validation_director==True and rec.validation_cfo_or_coo==True and rec.validation_ceo==True:
                    super(PurchaseOrder, self).button_confirm()
                else:
                    if rec.validation_purchasing_manager==False:
                        raise ValidationError(_("Purchasing Manager Approval Required"))
                    elif rec.validation_department_manager==False:
                        raise ValidationError(_("Department Manager Approval Required"))
                    elif rec.validation_director==False:
                        raise ValidationError(_("Director Approval Required"))
                    elif rec.validation_cfo_or_coo==False:
                        raise ValidationError(_("CFO/COO Approval Required"))
                    elif rec.validation_ceo==False:
                        raise ValidationError(_("CEO Approval Required"))

    def button_validation_purchasing_user(self):
        self.validation_purchasing_user = True

    def button_validation_purchasing_manager(self):
        self.validation_purchasing_manager = True

    def button_validation_department_manager(self):
        self.validation_department_manager = True

    def button_validation_director(self):
        self.validation_director = True

    def button_validation_cfo_or_coo(self):
        self.validation_cfo_or_coo = True

    def button_validation_ceo(self):
        self.validation_ceo = True