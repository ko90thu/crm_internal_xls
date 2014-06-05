from openerp.osv import orm
from openerp.addons.report_xls.utils import rowcol_to_cell, _render
from openerp.tools.translate import _

class res_partner(orm.Model):
	_inherit = 'res.partner'
	
	def _report_xls_fields(self,cr,uid,context=None):		
		return [
			'name','street','mobile',
		]
	 # Change/Add Template entries
	def _report_xls_template(self, cr, uid, context=None):
		"""
		Template updates, e.g.

		my_change = {
			'move':{
				'header': [1, 20, 'text', _('My Move Title')],
				'lines': [1, 0, 'text', _render("line.move_id.name or ''")],
				'totals': [1, 0, 'text', None]},
		}
		return my_change
		"""
		return {}
