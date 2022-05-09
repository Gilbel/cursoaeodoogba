{
  'name' : 'Helpdesk Gilberto',
  'summary' : 'Manage helpdesk tickets',
  'version' : '15.0.1.0.0',
  'author' : 'Gilberto',
  'depends' : ['base'],
  'license' : 'AGPL-3',
  'data' : [
    
    'security/helpdesk_security.xml',
    'security/ir.model.access.csv',
    'views/helpdesk_ticket_tags_views.xml',
    'views/helpdesk_ticket_views.xml',
    'views/helpdesk_ticket_action_views.xml',
    'data/tag_cron.xml',
    'wizard/create_ticket_views.xml']
 
} 