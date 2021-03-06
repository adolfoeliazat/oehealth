# -*- encoding: utf-8 -*-
################################################################################
#                                                                              #
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol                  #
#                                                                              #
# This program is free software: you can redistribute it and/or modify         #
# it under the terms of the GNU Affero General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or            #
# (at your option) any later version.                                          #
#                                                                              #
# This program is distributed in the hope that it will be useful,              #
# but WITHOUT ANY WARRANTY; without even the implied warranty of               #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
# GNU Affero General Public License for more details.                          #
#                                                                              #
# You should have received a copy of the GNU Affero General Public License     #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.        #
################################################################################

from osv import fields, osv

class oehealth_medicament_catalog(osv.osv):
    _description = 'Health Medicament Catalogs'
    _name = 'oehealth.medicament.catalog'
    
    def _compute_create_uid(self, cr, uid, ids, field_name, arg, context={}):
        result = {}
        for r in self.browse(cr, uid, ids, context=context):
            perms = self.perm_read(cr, uid, ids)
            create_uid = perms[0].get('create_uid', 'n/a')
            result[r.id] = create_uid
        return result

    def _compute_create_date(self, cr, uid, ids, field_name, arg, context={}):
        result = {}
        for r in self.browse(cr, uid, ids, context=context):
            perms = self.perm_read(cr, uid, ids)
            create_date = perms[0].get('create_date', 'n/a')
            result[r.id] = create_date
        return result

    def _compute_write_uid(self, cr, uid, ids, field_name, arg, context={}):
        result = {}
        for r in self.browse(cr, uid, ids, context=context):
            perms = self.perm_read(cr, uid, ids)
            write_uid = perms[0].get('write_uid', 'n/a')
            result[r.id] = write_uid
        return result

    def _compute_write_date(self, cr, uid, ids, field_name, arg, context={}):
        result = {}
        for r in self.browse(cr, uid, ids, context=context):
            perms = self.perm_read(cr, uid, ids)
            write_date = perms[0].get('write_date', 'n/a')
            result[r.id] = write_date
        return result

    _columns = {
        'name': fields.char('Medicament Catalog Name', required=True, size=64, translate=True),
        'alias' : fields.char('Alias', size=64, help='Common name that the Medicament Catalog is referred'),
        'catalog_code': fields.char(size=64, string='Medicament Catalog Code', required=False),
        'active': fields.boolean('Active', help="The active field allows you to hide the medicament catalog without removing it."),
        'catalog_info': fields.text(string='Info'),
        'date_catalog_inclusion' : fields.date('Catalog Inclusion Date'),
        'date_catalog_activation' : fields.date('Catalog Activation Date'),
        'date_catalog_inactivation' : fields.date('Catalog Inactivation Date'),
        'catalog_category': fields.many2one('oehealth.medicament.catalog.category',
                                            'Category',select=True),
        'catalog_tag_ids': fields.many2many('oehealth.tag', 
                                            'oehealth_medicament_catalog_tag_rel', 
                                            'catalog_id', 
                                            'tag_id', 
                                            'Tags'),
        'catalog_status': fields.selection([('U', 'Undefined'),
                                            ('A', 'Activated'),
                                            ('I', 'Inactivated'),
                                            ], string='Medicament Catalog Status',
                                               select=True, sort=False, required=False, translate=True),
        'catalog_annotation_ids': fields.one2many('oehealth.annotation',
                                                  'medicament_catalog_id',
                                                  'Annotations'),
        'state': fields.selection([('new','New'),
                                   ('revised','Revised'),
                                   ('waiting','Waiting'),
                                   ('okay','Okay')], 'Stage', readonly=True),
        'create_uid': fields.function(_compute_create_uid, method=True, type='char', string='Create User',),
        'create_date': fields.function(_compute_create_date, method=True, type='datetime', string='Create Date',),
        'write_uid': fields.function(_compute_write_uid, method=True, type='char', string='Write User',),
        'write_date': fields.function(_compute_write_date, method=True, type='datetime', string='Write Date',),
    }

    _sql_constraints = [('catalog_code_uniq', 'unique(catalog_code)', u'Duplicated Catalog Code!')]
    
    _defaults = {
        'catalog_code': '/',
        'active': 1,
        'catalog_status': 'U',
        'state': 'new',
    }
    
    _order = 'name'

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if not 'catalog_code' in vals or vals['catalog_code'] == '/':
            val = self.pool.get('ir.sequence').get(cr, uid, 'oehealth.medicament_catalog.code')
            code = map(int, str(val))
            code_len = len(code)
            while len(code) < 14:
                code.insert(0, 0)
            while len(code) < 16:
                n = sum([(len(code) + 1 - i) * v for i, v in enumerate(code)]) % 11
                if n > 1:
                    f = 11 - n
                else:
                    f = 0
                code.append(f)
            code_str = "%s.%s.%s.%s.%s-%s" % (str(code[0]) + str(code[1]),
                                              str(code[2]) + str(code[3]) + str(code[4]),
                                              str(code[5]) + str(code[6]) + str(code[7]),
                                              str(code[8]) + str(code[9]) + str(code[10]),
                                              str(code[11]) + str(code[12]) + str(code[13]),
                                              str(code[14]) + str(code[15]))
            if code_len <= 3:
                vals['catalog_code'] = code_str[18 - code_len:21]
            elif code_len > 3 and code_len <= 6:
                vals['catalog_code'] = code_str[17 - code_len:21]
            elif code_len > 6 and code_len <= 9:
                vals['catalog_code'] = code_str[16 - code_len:21]
            elif code_len > 9 and code_len <= 12:
                vals['catalog_code'] = code_str[15 - code_len:21]
            elif code_len > 12 and code_len <= 14:
                vals['catalog_code'] = code_str[14 - code_len:21]
        return super(oehealth_medicament_catalog, self).create(cr, uid, vals, context)

    # def write(self, cr, uid, ids, vals, context=None):
    #     if context is None:
    #         context = {}
    #     catalogs_without_code = self.search(cr, uid, [('catalog_code', 'in', [False, '/']),('id', 'in', ids)], context=context)
    #     direct_write_ids = set(ids) - set(catalogs_without_code)
    #     super(oehealth_medicament_catalog, self).write(cr, uid, list(direct_write_ids), vals, context)
    #     for group_id in catalogs_without_code:
    #         val = self.pool.get('ir.sequence').get(cr, uid, 'oehealth.medicament_catalog.code')
    #         code = map(int, str(val))
    #         code_len = len(code)
    #         while len(code) < 14:
    #             code.insert(0, 0)
    #         while len(code) < 16:
    #             n = sum([(len(code) + 1 - i) * v for i, v in enumerate(code)]) % 11
    #             if n > 1:
    #                 f = 11 - n
    #             else:
    #                 f = 0
    #             code.append(f)
    #         code_str = "%s.%s.%s.%s.%s-%s" % (str(code[0]) + str(code[1]),
    #                                           str(code[2]) + str(code[3]) + str(code[4]),
    #                                           str(code[5]) + str(code[6]) + str(code[7]),
    #                                           str(code[8]) + str(code[9]) + str(code[10]),
    #                                           str(code[11]) + str(code[12]) + str(code[13]),
    #                                           str(code[14]) + str(code[15]))
    #         if code_len <= 3:
    #             vals['catalog_code'] = code_str[18 - code_len:21]
    #         elif code_len > 3 and code_len <= 6:
    #             vals['catalog_code'] = code_str[17 - code_len:21]
    #         elif code_len > 6 and code_len <= 9:
    #             vals['catalog_code'] = code_str[16 - code_len:21]
    #         elif code_len > 9 and code_len <= 12:
    #             vals['catalog_code'] = code_str[15 - code_len:21]
    #         elif code_len > 12 and code_len <= 14:
    #             vals['catalog_code'] = code_str[14 - code_len:21]
    #         super(oehealth_medicament_catalog, self).write(cr, uid, group_id, vals, context)
    #     return True

    def oehealth_medicament_catalog_new(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'new'})
         return True

    def oehealth_medicament_catalog_revised(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'revised'})
         return True

    def oehealth_medicament_catalog_waiting(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'waiting'})
         return True

    def oehealth_medicament_catalog_okay(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'okay'})
         return True

oehealth_medicament_catalog()

