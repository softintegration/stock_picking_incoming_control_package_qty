# -*- coding: utf-8 -*- 

from odoo import models,fields,api,_
from odoo.tools.float_utils import float_compare
from odoo.exceptions import ValidationError


class StockMove(models.Model):
    _inherit = "stock.move"

    managed_by_package = fields.Boolean(string='Managed by package',related='product_id.managed_by_package')
    packages_qty = fields.Integer(string='Qty global of packages',states={'done': [('readonly', True)]},copy=False)
    global_qty_done = fields.Float(string='Global received Qty',states={'done': [('readonly', True)]},copy=False,
                                   digits='Product Unit of Measure',)

    def write(self, vals):
        res = super(StockMove, self).write(vals)
        self._check_global_qty_move_line_ids()
        return res

    @api.constrains('picking_type_id','packages_qty','product_global_qty','move_line_ids',
                    #'picking_type_id.show_operations'
                    )
    def _check_global_qty_move_line_ids(self):
        for each in self:
            if each.picking_type_id.code != 'incoming':
                continue
            if not each.picking_type_id.show_operations and each.managed_by_package and each.move_line_ids:
                if each.packages_qty != len(each.move_line_ids.mapped("result_package_id")):
                    raise ValidationError(_("The qty global of packages must be equal to the number of packages entered on the lines!"))
                if float_compare(each.global_qty_done, sum(each.move_line_ids.mapped("qty_done")), precision_rounding=each.product_uom.rounding) != 0:
                    raise ValidationError(_("The global received Qty received must be equal to the sum of the quantities entered on the lines"))







