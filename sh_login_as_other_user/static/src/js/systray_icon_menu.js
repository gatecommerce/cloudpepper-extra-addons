/* @odoo-module */

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { onWillStart,Component,onMounted } from "@odoo/owl";
import { session } from '@web/session';
import { _t } from "@web/core/l10n/translation";

class UserLoginMenu extends Component {
    setup() {
      super.setup();
      this.orm = useService('orm')
      this.action = useService("action");
      onWillStart(async () => {
        this.allow_user_show_icon =  await this.orm.call("res.users", 'check_login_enabled', [{ user_id: session.uid }], {});
      })
    }

    _onLoginUserClick(ev) {
        ev.preventDefault();
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t("Login AS"),
            views: [
                [false, 'form']
            ],
            res_model: 'login.other.wizard',
            target: 'new',
        })
    }
  }

  UserLoginMenu.template = "mail.systray.UserLoginMenu";
  const systrayItem = {
    Component: UserLoginMenu,
};

registry.category("systray").add("UserLoginMenu", systrayItem, { sequence: 10 });

