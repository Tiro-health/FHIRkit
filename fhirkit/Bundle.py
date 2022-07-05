from typing import List, Optional

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


from pydantic import confloat, Field, AnyUrl
from fhirkit.data_types import URI, Instant
from fhirkit.elements import BackboneElement, Identifier
from fhirkit.Resource import Resource

BundleType = Literal[
    "document",
    "message",
    "transaction",
    "transaction-response",
    "batch",
    "batch-response",
    "history",
    "searchset",
    "collection",
]

BundleSearchMode = Literal["match", "include", "outcome"]


class BundleLink(BackboneElement):
    relation: str
    url: URI


class BundleSearch(BackboneElement):
    mode: Optional[BundleSearchMode]
    score: confloat(ge=0, le=1)


class BundleRequest(BackboneElement):
    method: Literal["GET", "HEAD", "POST", "PUT", "DELETE", "PATCH"]
    url: URI
    ifNoneMatch: Optional[str]
    ifModifiedSince: Optional[Instant]
    ifMatch: Optional[str]
    ifNoneExist: Optional[str]


class BundleResponse(BackboneElement):
    status: str
    location: Optional[URI]
    etag: Optional[str]
    lastModified: Optional[Instant]
    outcome: Optional[Resource]


class BundleEntry(BackboneElement):
    fullUrl: Optional[URI]
    resource: Optional[Resource]
    request: Optional[BundleRequest]
    response: Optional[BundleResponse]


class Bundle(Resource):
    resourceType = Field("Bundle", const=True)
    identifier: Optional[Identifier]
    type: BundleType
    timestamp: Optional[Instant]
    entry: List[BundleEntry]
