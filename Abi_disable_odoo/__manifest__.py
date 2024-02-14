# -*- coding: utf-8 -*-
{
    "name": "Remove odoo.com Bindings.",
    "version": "1.0",
    "author": "Abinfocom",
    "website": "www.abinfocom.com",
    "category": "Extra Tools",
    "license": "LGPL-3",
    "support": " ",
    "summary": " Remove odoo.com Bindings. ",
    "description": """ Remove odoo.com Bindings. """,
    "depends": ["mail", "base"],
    "data": [
        "views/ir_ui_menu.xml",
        "views/inherit_res_company_view.xml",
    ],
    "assets": {
        "web.assets_backend": ["Abi_disable_odoo/static/src/js/user_menu_items.esm.js"],
    },
    "application": True,
    "installable": True,
    "auto_install": False,
}
