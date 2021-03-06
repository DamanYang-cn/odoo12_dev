# -*- coding: utf-8 -*-

from odoo import api, models, fields, exceptions


class OrdenReparacion(models.Model):
    _name = 'taller.order.reparacion'
    _description = 'Gestión Órdenes Reparación'

    name = fields.Char(string='Name', required=True, help="Introduzca el nombre", size=20, default="Nueva Orden")
    active = fields.Boolean(string='Activo', default='1')
    partner_id = fields.Many2one(comodel_name='res.partner', string="Cliente")
    reparacion_line_ids = fields.One2many(comodel_name='taller.order.reparacion.line',
                                          inverse_name='reparacion_id',
                                          string='Lineas Reparación')
    state = fields.Selection([
        ('draft', 'Nuevo'),
        ('confirm', 'Confirmado'),
        ('done', 'Realizado'),
        ('cancel', 'Cancelado'),
    ], string='Estado', readonly=True, index=True, copy=False,
        default='draft', tracking=True)

    @api.model
    def create(self, vals):
        new_seq_name = self.env['ir.sequence'].next_by_code(
            'order.reparacion') or 'New'
        vals.update(name=new_seq_name)
        res = super(OrdenReparacion, self).create(vals)
        return res

    def confirm(self):
        self.write({'state': 'confirm'})

    def cancel(self):
        self.write({'state': 'cancel'})

    def done(self):
        self.write({'state': 'done'})


class OrderReparacionLine(models.Model):
    _name = 'taller.order.reparacion.line'
    _description = 'Líneas Órden Reparación'

    name = fields.Char(string='Name', required=True, help="Introduzca el nombre",
                       default="Nueva Linea Orden Reparación")
    reparacion_id = fields.Many2one(comodel_name="taller.order.reparacion")
    active = fields.Boolean(string='Activo', default='True')
    vehiculo_id = fields.Many2one(comodel_name='taller.vehiculo', string="Vehiculo")
