""" Navigation
"""

from urllib.parse import urlparse
from plone.restapi.interfaces import IExpandableElement, IPloneRestapiLayer
from plone.restapi.services.navigation.get import Navigation as BaseNavigation
from plone.restapi.services.navigation.get import (
    NavigationGet as BaseNavigationGet,
)
from zope.component import adapter
from zope.interface import Interface, implementer


@implementer(IExpandableElement)
@adapter(Interface, IPloneRestapiLayer)
class Navigation(BaseNavigation):
    """Navigation adapter"""

    def __call__(self, expand=False):
        if self.request.form.get("expand.navigation.depth", False):
            self.depth = int(self.request.form["expand.navigation.depth"])
        else:
            self.depth = 1

        result = {
            "navigation": {"@id": self.context.absolute_url() + "/@navigation"}
        }
        if not expand:
            return result

        result["navigation"]["items"] = self.build_tree(self.navtree_path)
        return result

    def customize_entry(self, entry, brain):
        """append custom entries"""
        entry["brain"] = brain
        if hasattr(brain, "getRemoteUrl") and brain.getRemoteUrl:
            entry["path"] = urlparse(brain.getRemoteUrl).path
            entry["@id"] = brain.getRemoteUrl

        return entry

    def render_item(self, item, path):
        """build navtree from item helper"""
        sub = self.build_tree(item["path"], first_run=False)

        item.update({"items": sub})

        if "path" in item:
            del item["path"]

        if "brain" in item:
            del item["brain"]

        return item


class NavigationGet(BaseNavigationGet):
    """Navigation get service"""

    def reply(self):
        """reply"""
        navigation = Navigation(self.context, self.request)
        return navigation(expand=True)["navigation"]
