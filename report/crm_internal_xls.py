import xlwt
import time
from datetime import datetime
from openerp.osv import orm
from openerp.report import report_sxw
from openerp.addons.report_xls.report_xls import report_xls
from openerp.addons.report_xls.utils import rowcol_to_cell, _render
from openerp.tools.translate import translate, _
from openerp import pooler
import logging
_logger = logging.getLogger(__name__)

_ir_translation_name = 'crm_internal.xls'

class res_partner_xls_parser(report_sxw.rml_parse):
	def __init__(self, cr, uid, name, context):
		import pdb;
		pdb.set_trace()
		super(res_partner_xls_parser, self).__init__(cr, uid, name, context=context)
		res_obj = self.pool.get('res.partner')
		self.context = context
		wanted_list = res_obj._report_xls_fields(cr, uid, context)
		template_changes = res_obj._report_xls_template(cr, uid, context)
		self.localcontext.update({
			'datetime': datetime,
			'wanted_list': wanted_list,
			'template_changes': template_changes,
			'_': self._,
		})

	def _(self, src):
		lang = self.context.get('lang', 'en_US')
		return translate(self.cr, _ir_translation_name, 'report', lang, src) or src

class res_partner_xls(report_xls):

	def __init__(self, name, table, rml=False, parser=False, header=True, store=False):
		super(res_partner_xls, self).__init__(name, table, rml, parser, header, store)

		# Cell Styles
		_xs = self.xls_styles
		# header
		rh_cell_format = _xs['bold'] + _xs['fill'] + _xs['borders_all']
		self.rh_cell_style = xlwt.easyxf(rh_cell_format)
		self.rh_cell_style_center = xlwt.easyxf(rh_cell_format + _xs['center'])
		self.rh_cell_style_right = xlwt.easyxf(rh_cell_format + _xs['right'])
		# lines
		aml_cell_format = _xs['borders_all']
		self.aml_cell_style = xlwt.easyxf(aml_cell_format)
		self.aml_cell_style_center = xlwt.easyxf(aml_cell_format + _xs['center'])
		self.aml_cell_style_date = xlwt.easyxf(aml_cell_format + _xs['left'], num_format_str=report_xls.date_format)
		self.aml_cell_style_decimal = xlwt.easyxf(aml_cell_format + _xs['right'], num_format_str=report_xls.decimal_format)
		# totals
		rt_cell_format = _xs['bold'] + _xs['fill'] + _xs['borders_all']
		self.rt_cell_style = xlwt.easyxf(rt_cell_format)
		self.rt_cell_style_right = xlwt.easyxf(rt_cell_format + _xs['right'])
		self.rt_cell_style_decimal = xlwt.easyxf(rt_cell_format + _xs['right'], num_format_str=report_xls.decimal_format)	
		self.col_specs_template = {
            'name': {
                'header': [1, 20, 'text', _render("_('Customer Name')")],
                'lines': [1, 0, 'text', _render("line.name or ''")],
                'totals': [1, 0, 'text', None]},           
            'street': {
                'header': [1, 42, 'text', _render("_('Address')")],
                'lines': [1, 0, 'text', _render("line.street or ''")],
                'totals': [1, 0, 'text', None]},
	    'mobile': {
                'header': [1, 42, 'text', _render("_('Mobile')")],
                'lines': [1, 0, 'text', _render("line.mobile or ''")],
                'totals': [1, 0, 'text', None]},
            
	     
        }
        
	def generate_xls_report(self, _p, _xs, data, objects, wb):		
		wanted_list = _p.wanted_list
		self.col_specs_template.update(_p.template_changes)
		_ = _p._
		import pdb;
		pdb.set_trace()
		
		      
        

		#report_name = objects[0]._description or objects[0]._name
		report_name = _("Customer Lists")
		ws = wb.add_sheet(report_name[:31])
		ws.panes_frozen = True
		ws.remove_splits = True
		ws.portrait = 0  # Landscape
		ws.fit_width_to_pages = 1
		row_pos = 0

		# set print header/footer
		ws.header_str = self.xls_headers['standard']
		ws.footer_str = self.xls_footers['standard']

		# Title
		cell_style = xlwt.easyxf(_xs['xls_title'])
		c_specs = [
			('report_name', 1, 0, 'text', report_name),
		]
		row_data = self.xls_row_template(c_specs, ['report_name'])
		row_pos = self.xls_write_row(ws, row_pos, row_data, row_style=cell_style)
		row_pos += 1

		# Column headers
		c_specs = map(lambda x: self.render(x, self.col_specs_template, 'header', render_space={'_': _p._}), wanted_list)
		row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
		row_pos = self.xls_write_row(ws, row_pos, row_data, row_style=self.rh_cell_style, set_column_size=True)
		ws.set_horz_split_pos(row_pos)

		# res_partner
		for line in objects:			
			c_specs = map(lambda x: self.render(x, self.col_specs_template, 'lines'), wanted_list)
			row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
			row_pos = self.xls_write_row(ws, row_pos, row_data, row_style=self.aml_cell_style)

		# Totals
		aml_cnt = len(objects)		
		c_specs = map(lambda x: self.render(x, self.col_specs_template, 'totals'), wanted_list)
		row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
		row_pos = self.xls_write_row(ws, row_pos, row_data, row_style=self.rt_cell_style_right)

res_partner_xls('report.customer.xls',
    'res.partner',
    parser=res_partner_xls_parser)

