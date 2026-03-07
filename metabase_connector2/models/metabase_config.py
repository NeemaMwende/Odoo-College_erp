import time
import jwt
import requests
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MetabaseConfig(models.Model):
    _name = 'metabase.jwt.config'
    _description = 'Metabase JWT Configuration'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    metabase_url = fields.Char(
        string='Metabase URL',
        required=True,
        help='Base URL of your Metabase instance, e.g. http://localhost:3000',
    )
    secret_key = fields.Char(
        string='Metabase Secret Key',
        required=True,
        help='The METABASE_SECRET_KEY from Metabase Admin > Embedding settings.',
    )
    metabase_api_key = fields.Char(
        string='Metabase API Key',
        help='Optional. Used to fetch dashboard list from Metabase API.',
    )
    token_expiry_minutes = fields.Integer(
        string='Token Expiry (minutes)',
        default=10,
        help='How long the JWT embed token is valid. Default: 10 minutes.',
    )
    dashboard_ids = fields.One2many(
        'metabase.jwt.dashboard',
        'config_id',
        string='Dashboards',
    )

    # ------------------------------------------------------------------ #
    # JWT helpers                                                         #
    # ------------------------------------------------------------------ #

    def _generate_token(self, resource_type, resource_id, params=None):
        """Generate a JWT token for Metabase embedding.

        Args:
            resource_type: 'dashboard' or 'question'
            resource_id: the Metabase numeric ID
            params: dict of locked parameters (optional)
        """
        self.ensure_one()
        payload = {
            'resource': {resource_type: resource_id},
            'params': params or {},
            'exp': round(time.time()) + (self.token_expiry_minutes * 60),
        }
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return token

    def _get_embed_url(self, resource_type, resource_id, params=None):
        """Return the full embed URL for a resource."""
        self.ensure_one()
        token = self._generate_token(resource_type, resource_id, params)
        base = self.metabase_url.rstrip('/')
        return '%s/embed/%s/%s#bordered=true&titled=true' % (
            base, resource_type, token,
        )

    # ------------------------------------------------------------------ #
    # API helpers                                                         #
    # ------------------------------------------------------------------ #

    def _get_headers(self):
        self.ensure_one()
        if not self.metabase_api_key:
            raise UserError(_('API Key is required for this operation.'))
        return {
            'x-api-key': self.metabase_api_key,
            'Content-Type': 'application/json',
        }

    def _metabase_get(self, endpoint):
        self.ensure_one()
        url = self.metabase_url.rstrip('/') + endpoint
        try:
            response = requests.get(url, headers=self._get_headers(), timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            raise UserError(_('Cannot connect to Metabase at %s') % self.metabase_url)
        except requests.exceptions.HTTPError as e:
            raise UserError(_('Metabase API error: %s') % str(e))
        except Exception as e:
            raise UserError(_('Unexpected error: %s') % str(e))

    # ------------------------------------------------------------------ #
    # Actions                                                              #
    # ------------------------------------------------------------------ #

    def action_check_connection(self):
        self.ensure_one()
        data = self._metabase_get('/api/user/current')
        email = data.get('email', '?')
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Connection successful'),
                'message': _('Connected to Metabase as %s') % email,
                'type': 'success',
                'sticky': False,
            },
        }

    def action_fetch_dashboards(self):
        self.ensure_one()
        data = self._metabase_get('/api/dashboard')
        existing = {d.metabase_id: d for d in self.dashboard_ids}
        for item in data:
            metabase_id = item.get('id')
            name = item.get('name', _('Unnamed'))
            if metabase_id in existing:
                existing[metabase_id].write({'name': name})
            else:
                self.env['metabase.jwt.dashboard'].create({
                    'config_id': self.id,
                    'metabase_id': metabase_id,
                    'name': name,
                })
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Dashboards fetched'),
                'message': _('%d dashboards synced from Metabase') % len(data),
                'type': 'success',
                'sticky': False,
            },
        }
