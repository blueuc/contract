# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ContractContractTerminate(models.TransientModel):
    _name = "contract.contract.terminate"
    _description = "Terminate Contract Wizard"

    contract_id = fields.Many2one(
        comodel_name="contract.contract",
        string="Contract",
        required=True,
        ondelete="cascade",
    )
    terminate_reason_id = fields.Many2one(
        comodel_name="contract.terminate.reason",
        string="Termination Reason",
        required=True,
        ondelete="cascade",
    )
    terminate_comment = fields.Text(string="Termination Comment")
    terminate_date = fields.Date(string="Termination Date", required=True)
    terminate_comment_required = fields.Boolean(
        related="terminate_reason_id.terminate_comment_required"
    )
    terminate_with_last_date_invoiced = fields.Boolean(
        string="Terminate lines with last date invoiced",
        help="Terminate the contract lines with the last invoiced date if they cannot "
        "be terminated with the date reported in the wizard.",
    )

    def terminate_contract(self):
        for wizard in self:
            wizard.contract_id._terminate_contract(
                wizard.terminate_reason_id,
                wizard.terminate_comment,
                wizard.terminate_date,
                wizard.terminate_with_last_date_invoiced,
            )
        return True
