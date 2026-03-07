import json
from odoo import http
from odoo.http import request


class MetabaseJwtController(http.Controller):

    @http.route('/metabase_jwt/embed_url', auth='user', type='json')
    def get_embed_url(self, dashboard_db_id, **kwargs):
        """Generate a fresh JWT embed URL for the given dashboard record.

        Called by the OWL frontend component each time a dashboard is opened,
        ensuring the JWT token is always fresh.
        """
        dashboard = request.env['metabase.jwt.dashboard'].browse(int(dashboard_db_id))
        if not dashboard.exists():
            return {'error': 'Dashboard not found'}
        return {'url': dashboard._get_embed_url()}
