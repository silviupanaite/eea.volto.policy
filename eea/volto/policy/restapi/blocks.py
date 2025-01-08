""" block-related utils """

from urllib.parse import urlparse
from plone import api
from plone.restapi.behaviors import IBlocks
from plone.restapi.interfaces import IBlockFieldSerializationTransformer
from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest
from eea.volto.policy.restapi.services.contextnavigation.get import (
    EEANavigationPortletRenderer,
    eea_extract_data,
    IEEANavigationPortlet,
)
try:
    from eea.api.versions.browser.relations import EEAVersionsView
except ImportError:
    EEAVersionsView = None


@implementer(IBlockFieldSerializationTransformer)
@adapter(IBlocks, IBrowserRequest)
class RestrictedBlockSerializationTransformer:
    """Restricted Block serialization"""

    order = 9999
    block_type = None

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, value):
        restrictedBlock = value.get("restrictedBlock", False)
        if not restrictedBlock:
            return value
        if restrictedBlock and api.user.has_permission(
            "EEA: Manage restricted blocks", obj=self.context
        ):
            return value
        return {"@type": "empty"}


@implementer(IBlockFieldSerializationTransformer)
@adapter(IBlocks, IBrowserRequest)
class ContextNavigationBlockSerializationTransformer:
    """ContextNavigation Block serialization"""

    order = 9999
    block_type = "contextNavigation"

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, value):
        if value.get("variation", None) == "report_navigation":

            if (
                "root_node" in value and
                isinstance(value["root_node"], list) and
                len(value["root_node"]) > 0
            ):
                root_nav_item = value["root_node"][0]
                url = urlparse(root_nav_item.get("@id", ""))
                value["root_path"] = url.path if url.scheme else ""

            data = eea_extract_data(IEEANavigationPortlet, value, prefix=None)

            renderer = EEANavigationPortletRenderer(
                self.context, self.request, data
            )
            res = renderer.render()
            is_data_available = res.get(
                "available", True
            )  # or get res[items]?
            value["results"] = is_data_available

        return value


@implementer(IBlockFieldSerializationTransformer)
@adapter(IBlocks, IBrowserRequest)
class AllVersionBlockSerializationTransformer:
    """All versions Block serialization"""

    order = 9999
    block_type = "eea_versions"

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, value):
        if value.get("@type", None) == "eea_versions":
            all_versions = EEAVersionsView(self.context, self.request)
            results = (
                all_versions.newer_versions() or all_versions.older_versions()
            )

            value["results"] = len(results) > 0
        return value


@implementer(IBlockFieldSerializationTransformer)
@adapter(IBlocks, IBrowserRequest)
class LatestVersionBlockSerializationTransformer:
    """Latest versions Block serialization"""

    order = 9999
    block_type = "eea_latest_version"

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, value):
        if value.get("@type", None) == "eea_latest_version":
            all_versions = EEAVersionsView(self.context, self.request)
            results = all_versions.newer_versions()

            value["results"] = len(results) > 0

        return value
