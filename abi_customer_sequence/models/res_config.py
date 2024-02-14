from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    is_seq_auto_create = fields.Boolean(
        "Auto Create Customer Sequence",
        default=False,
        config_parameter="abi_customer_sequence.is_seq_auto_create",
        store=True,
    )
