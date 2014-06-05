try:
    from . import crm_internal
    from . import report
except ImportError:
    import logging
    logging.getLogger('openerp.module').warning('report_xls not available in addons path.')
