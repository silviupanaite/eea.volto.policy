""" Controlpanel get service """

from plone.restapi.services.controlpanels.get import (
    ControlpanelsGet as PloneControlpanelsGet
)
from eea.volto.policy.restapi.services.controlpanel.utils import (
    has_controlpanel_permission
)


class ControlpanelsGet(PloneControlpanelsGet):
    """ Controlpanel get service """

    def reply(self):
        """ Reply """
        if self.params:
            return self.reply_panel()
        return super().reply()

    def reply_panel(self):
        """ Reply panel """
        name = self.params[0]
        panel = self.panel_by_name(name)

        if not has_controlpanel_permission(self.context, self.request, panel):
            return None

        return super().reply_panel()
