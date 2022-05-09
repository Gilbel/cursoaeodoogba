from odoo import models, api, fields, _, Command

class CreateTicket(models.TransientModel):
    _name ='create.ticket'
    
    @api.model
    def _get_default_tags(self):
        if self.env.context.get('active_model') == 'helpdesk.tickets.tags':
            return [Command.set(self.env.context.get('active_ids'))]
      
    
    name = fields.Char()
    tag_ids = fields.Many2many(
        comodel_name='helpdesk.ticket.tags',
        string = 'Tags',
        default= _get_default_tags)
    
    def get_ticket_values(self):
        return{
            'name': self.name,
            'tags_ids': [Command.set(self.tag_ids.ids)] 
            
        }
        
    
    def create_ticket(self):
        
        self.ensure_one()
        
        ticket_values = self.get_ticket_values()
        
        new_ticket = self.env['helpdesk.ticket'].create(ticket_values)
        action=self.env["ir.actions.actions"]._for_xml_id("helpdesk_gilberto.helpdesk_ticket_action_all")
        action['views']= [(self.env.ref('helpdesk_gilberto.view_helpdesk_ticket_form').id, 'form')]
        action['res_id'] = new_ticket.id
        return action
        