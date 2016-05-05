# -*- encoding: utf-8 -*-

from openerp.osv import osv, fields
import logging

class res_partner(osv.osv):
    _inherit = "res.partner"

    def _validar_nit(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)

        if obj.vat == 'CF' or not obj.vat:
            return True

        partners_id = self.search(cr, uid, [('vat','=',obj.vat),('parent_id','!=',False)])
        if len(partners_id) > 1:
            return False

        if obj.country_id and obj.country_id.id != 91:
            return True

        nit = obj.vat.replace('-','')
        verificador = nit[-1]
        if verificador.upper() == 'K':
            verificador = '10'
        secuencia = nit[:-1]

        total = 0
        i = 2
        for c in secuencia[::-1]:
            total += int(c) * i
            i += 1

        resultante = ( 11 - ( total % 11 ) ) % 11

        if str(resultante) == verificador:
            return True
        else:
            return False

    _constraints = [
        #(_validar_nit, 'El NIT no es correcto', ['vat']),
    ]
