from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MetabaseDashboard(models.Model):
    _name = 'metabase.jwt.dashboard'
    _description = 'Metabase JWT Dashboard'
    _rec_name = 'name'
    _order = 'name'

    config_id = fields.Many2one(
        'metabase.jwt.config',
        string='Configuration',
        required=True,
        ondelete='cascade',
    )
    name = fields.Char(string='Dashboard Name', required=True)
    metabase_id = fields.Integer(
        string='Metabase Dashboard ID',
        required=True,
        help='The numeric ID of the dashboard in Metabase (visible in the URL).',
    )
    enable_download = fields.Boolean(
        string='Allow Downloads',
        default=True,
    )
    enable_title = fields.Boolean(
        string='Show Title',
        default=True,
    )

    # Menu integration fields
    menu_ids = fields.One2many(
        'metabase.jwt.dashboard.menu',
        'dashboard_id',
        string='Menus',
    )

    def _get_embed_url(self):
        """Generate a fresh JWT embed URL for this dashboard."""
        self.ensure_one()
        config = self.config_id
        token = config._generate_token('dashboard', self.metabase_id)
        base = config.metabase_url.rstrip('/')
        params = []
        if self.enable_title:
            params.append('titled=true')
        if self.enable_download:
            params.append('with-downloads=true')
        params.append('bordered=true')
        fragment = '&'.join(params)
        return '%s/embed/dashboard/%s#%s' % (base, token, fragment)

    def action_open_dashboard(self):
        """Open dashboard in a new browser tab."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': self._get_embed_url(),
            'target': 'new',
        }

    def action_open_embedded(self):
        """Open dashboard embedded in Odoo via client action."""
        self.ensure_one()
        return {
            'type': 'ir.actions.client',
            'tag': 'metabase_jwt_dashboard_view',
            'name': self.name,
            'params': {
                'dashboard_db_id': self.id,
                'dashboard_name': self.name,
            },
        }


class MetabaseDashboardMenu(models.Model):
    _name = 'metabase.jwt.dashboard.menu'
    _description = 'Metabase JWT Dashboard Menu'
    _rec_name = 'name'

    dashboard_id = fields.Many2one(
        'metabase.jwt.dashboard',
        string='Dashboard',
        required=True,
        ondelete='cascade',
    )
    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    parent_menu_id = fields.Many2one(
        'ir.ui.menu',
        string='Parent Menu',
    )
    group_ids = fields.Many2many(
        'res.groups',
        string='Access Groups',
    )
    menu_id = fields.Many2one(
        'ir.ui.menu',
        string='Generated Menu',
        readonly=True,
        copy=False,
    )
    action_id = fields.Many2one(
        'ir.actions.client',
        string='Generated Action',
        readonly=True,
        copy=False,
    )

    def _create_or_update_action(self):
        self.ensure_one()
        vals = {
            'name': self.name,
            'tag': 'metabase_jwt_dashboard_view',
            'params': {
                'dashboard_db_id': self.dashboard_id.id,
                'dashboard_name': self.dashboard_id.name,
            },
        }
        if self.action_id:
            self.action_id.write(vals)
            return self.action_id
        else:
            action = self.env['ir.actions.client'].create(vals)
            self.action_id = action
            return action

    def _create_or_update_menu(self, action):
        self.ensure_one()
        vals = {
            'name': self.name,
            'sequence': self.sequence,
            'parent_id': self.parent_menu_id.id if self.parent_menu_id else False,
            'action': 'ir.actions.client,%d' % action.id,
            'groups_id': [(6, 0, self.group_ids.ids)],
        }
        if self.menu_id:
            self.menu_id.write(vals)
        else:
            menu = self.env['ir.ui.menu'].create(vals)
            self.menu_id = menu

    def action_generate_menu(self):
        for rec in self:
            action = rec._create_or_update_action()
            rec._create_or_update_menu(action)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Menus generated'),
                'message': _('Menu items have been created/updated successfully.'),
                'type': 'success',
                'sticky': False,
            },
        }

    def _cleanup_generated(self):
        menus = self.mapped('menu_id')
        actions = self.mapped('action_id')
        if menus:
            menus.unlink()
        if actions:
            actions.unlink()

    def unlink(self):
        self._cleanup_generated()
        return super().unlink()

    def write(self, vals):
        trigger_fields = {'name', 'parent_menu_id', 'group_ids', 'sequence', 'dashboard_id'}
        if trigger_fields & set(vals.keys()):
            self._cleanup_generated()
        return super().write(vals)

    def action_remove_menu(self):
        self._cleanup_generated()
