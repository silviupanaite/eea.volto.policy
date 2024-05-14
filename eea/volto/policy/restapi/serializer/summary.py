from plone.restapi.interfaces import IJSONSummarySerializerMetadata
from plone.restapi.serializer.summary import JSONSummarySerializerMetadata
from zope.interface import implementer


@implementer(IJSONSummarySerializerMetadata)
class EEAJSONSummarySerializerMetadata(JSONSummarySerializerMetadata):
    def default_metadata_fields(self):
        return {"@id", "@type", "description", "review_state", "title", "type_title", 'effective'}
