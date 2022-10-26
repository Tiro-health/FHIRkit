from typing import List, Optional, Sequence


try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore

from pydantic import Field, ConstrainedFloat, Field
from fhirkit.primitive_datatypes import URI, Instant
from fhirkit.elements import BackboneElement, Identifier, Signature
from fhirkit.Resource import Resource, ResourceWithMultiIdentifier

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


class BundleSearchScore(ConstrainedFloat):
    ge = 0
    le = 1


class BundleSearch(BackboneElement):
    mode: Optional[BundleSearchMode]
    score: BundleSearchScore


class BundleLink(BackboneElement):
    relation: str
    url: URI


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
    identifier: Optional[Identifier] = None
    type: BundleType
    timestamp: Optional[Instant] = None
    link: Sequence[BundleLink] = []
    entry: List[BundleEntry]
    signature: Optional[Signature] = None
