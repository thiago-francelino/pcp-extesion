{
    'name': 'PCP Extension',
    'version': '14.0.1.0.1',
    'summary': "",
    'description': "",
    'category': '',
    'author': 'Thiago Francelino Santos',
    'contributors': [
        'Mila',
        'Gustavo Lourenço'
    ],
    'depends': ['mrp','hr','stock'],
    'company': 'SUPERGLASS',
    'data': [
        'security\ir.model.access.csv',
        'views\pcp_extension_view.xml',
        'views\inherit_mrp_bom_view.xml',
        'views\inherit_workorder_view.xml',
        'views\inherit_mo_view.xml',
        'views\inherit_mrp_workcenter_view.xml',
        # 'views\inherit_product_category.xml',
        'wizards\material_occurrence_view.xml',
        'views\production_request_view.xml',
        'views\cutting_plan_view.xml',
        'views\production_request_view.xml',
    ],
    'license': 'LGPL-3',
}
