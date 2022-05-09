from requests_toolbelt import user_agent
from odoo import fields, models, api, _, Command
from odoo import exceptions

from datetime import datetime


class HelpdeskTicket(models.Model):
  _name = "helpdesk.ticket"
  _description = "Helpdesk Ticket"
  _order ='sequence'
  
  @api.model
  def _get_default_user(self):
        return self.env.user
  
  
  
  name = fields.Char(required=True)
  description = fields.Text()
  date = fields.Date(help = "Date when the ticket was created")
  date_start= fields.Datetime()
  
  time = fields.Float(string='time')
  limit_date = fields.Date(help = "Date when the ticket will be closed")
  assigned = fields.Boolean(
    help = "Ticket asigned to someone", 
    compute='_compute_assigned', 
    search='_search_assigned',
    inverse='_set_assigned')
  actions_todo = fields.Html()
  user_id = fields.Many2one(comodel_name = 'res.users', string= 'Assigned to', default=_get_default_user)
  user_email= fields.Char(
    string='User Email',
    related='user_id.partner_id.email') 
  ticket_company= fields.Boolean(string='Ticket_company')
  partner_id = fields.Many2one(comodel_name = 'res.partner', string= 'Partner')
  partner_email= fields.Char(
    string='Partner Email',
    related='partner_id.email') 
  sequence = fields.Integer('Sequence') 
  action_ids = fields.One2many(comodel_name = 'helpdesk.ticket.action',inverse_name='ticket_id', string= 'Actions Done')
  tag_name= fields.Char(string='Tag Name')
  tags_ids = fields.Many2many(
    comodel_name='helpdesk.ticket.tags',
    relation='helpdesk_ticket_tag_rel',
    column1='ticket_id',
    column2='tag_id',
    string='Tags')
  color= fields.Integer('Color Indez', default=0)
  
 
  state = fields.Selection (
    [('nuevo','Nuevo'),
     ('asignado','Asignado'),
     ('en_proceso', 'En proceso'),
     ('pendiente', 'Pendiente'),
     ('resuelto', 'Resuelto'),
     ('cancelado','Cancelado')],
     string='State', default='nuevo')  
  
  def to_asignado(self):
     self.ensure_one()
     self.state ='asignado'  
  
  def to_en_proceso(self):
     self.write({'state' : 'en_proceso'}) 
    
  def to_pendiente(self):
      for record in self:
        record.state = 'pendiente'
  
  def review_actions(self):
      self.ensure_one()
      #import pdb; pdb.set_trace()
      self.action_ids.review()
  
  @api.model   
  def get_amount_ticket(self):
      return self.search_count ([('user_id','=', self.env.user.id)])
    
  @api.depends('user_id')
  def _compute_assigned(self):
    for record in self:
      record.assigned = record.user_id or False
      
  def _search_assigned(self, operator, value):
    if operator not in ['=', '!='] or not isinstance(value, bool):
      raise UserError(_('Operation not supported'))
    
    if (operator == '=' and value) or (operator == '!=' and not value):
      new_operator = '!='
    else:
      new_operator = '='
          
    return[('user_id',new_operator, False)]
  
  def _set_assigned(self):
        for record in self:
          if not record.assigned:
            record.user_id=False
          else:
            record.user_id=self.env.user
  
  def create_and_link_tag(self):
    self.ensure_one()
    
    #creo el ticket y lo asigno
    #self.env['helpdesk.ticket.tags'].create({'name': self.tag_name})  
    #self.write({4,tag.id,0})
    #self.write({'tags_ids' : [Command.link(tag.id)]})
    
    #creo el ticket desde la escritura del tags_ids
    #self.write({'tags_ids':[(0,0,{'name': self.tag_name})],
    #   'tag_name':False})
    self.write({'tags_ids':[Command.create({'name': self.tag_name})],
        'tag_name':False})
  
  @api.constrains('time')
  def _check_time(self):
      if self.filtered (lambda t: t.time<0):
       raise ValidationError(_('The time must be greather than 0.'))
  
  @api.onchange('date_start')
  def _onchange_date_start(self):
    if self.date_start:
      self.limit_date = self.date_start + datetime.timedelta (days=1)
    else:
          self.limit_date = False
  
  