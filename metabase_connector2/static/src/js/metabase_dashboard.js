/** @odoo-module **/

import { Component, useState, onMounted, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

/**
 * MetabaseJwtDashboardView – client action that fetches a fresh JWT embed URL
 * from the server and renders the Metabase dashboard in an interactive iframe.
 */
class MetabaseJwtDashboardView extends Component {
    static template = "metabase_connector2.MetabaseJwtDashboardView";

    setup() {
        this.rpc = useService("rpc");
        this.state = useState({ loading: true, error: false, embedUrl: "" });
        this.iframeRef = useRef("iframe");

        onMounted(async () => {
            await this._fetchEmbedUrl();
            // After URL is set and iframe starts loading
            const iframe = this.iframeRef.el;
            if (iframe) {
                iframe.addEventListener("load", () => {
                    this.state.loading = false;
                });
                iframe.addEventListener("error", () => {
                    this.state.loading = false;
                    this.state.error = true;
                });
            }
        });
    }

    async _fetchEmbedUrl() {
        const dashboardDbId = this.props.action.params?.dashboard_db_id;
        if (!dashboardDbId) {
            this.state.loading = false;
            this.state.error = true;
            return;
        }
        try {
            const result = await this.rpc("/metabase_jwt/embed_url", {
                dashboard_db_id: dashboardDbId,
            });
            if (result.error) {
                this.state.loading = false;
                this.state.error = true;
            } else {
                this.state.embedUrl = result.url;
            }
        } catch (e) {
            this.state.loading = false;
            this.state.error = true;
        }
    }

    get dashboardName() {
        return this.props.action.params?.dashboard_name || "Dashboard";
    }

    openInNewTab() {
        if (this.state.embedUrl) {
            window.open(this.state.embedUrl, "_blank", "noopener,noreferrer");
        }
    }
}

MetabaseJwtDashboardView.props = {
    action: { type: Object },
    actionId: { type: Number, optional: true },
    className: { type: String, optional: true },
    globalState: { type: Object, optional: true },
};

registry.category("actions").add("metabase_jwt_dashboard_view", MetabaseJwtDashboardView);

export { MetabaseJwtDashboardView };
