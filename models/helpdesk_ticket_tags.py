from odoo import fields,models,api,Command


class HelpdeskTicketTags(models.Model):
  _name = "helpdesk.ticket.tags"
  _description = "Helpdesk Ticket Tags"
  
  
  @api.model
  def _get_default_tickets(self):
      if self.env.context.get('active_model') == 'helpdesk.tickets':
        return [Command.set(self.env.context.get('active_ids'))]
      return False
  
  name = fields.Char (required=True)
  description = fields.Text()
  
  ticket_ids = fields.Many2many(
    comodel_name='helpdesk.ticket',
    relation='helpdesk_ticket_tag_rel',
    column1='tag_id',
    column2='ticket_id',
    string='Tickets',
    default=_get_default_tickets)
 
  @api.model
  def clean_unused_tags(self):
    unused_tags= self.search([('ticket_ids', '=', False)])
    unused_tags.unlink()
    