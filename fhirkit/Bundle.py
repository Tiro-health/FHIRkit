from importlib.resources import Resource
from typing import List, Literal, Optional

from pydantic import Field, HttpUrl
from elements import Identifier
from data_types import Instant
from fhirkit.elements import BackboneElement

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


class BundleLink(BackboneElement):
    relation: str
    url: HttpUrl


class BundleSearch(BackboneElement):
    # TODO
    pass


class BundleRequest(BackboneElement):
    method: Literal["GET", "HEAD", "POST", "PUT", "DELETE", "PATCH"]
    url: HttpUrl


class BundleResponse(BackboneElement):
    status: str
    location: Optional[HttpUrl]
    etag: Optional[str]
    lastModified: Optional[Instant]
    outcome: Optional[Resource]


class BundleEntry(BackboneElement):
    fullUrl: Optional[HttpUrl]
    resource: Optional[Resource]
    request: Optional[BundleRequest]
    response: Optional[BundleResponse]


class Bundle(Resource):
    resourceType = Field("Bundle", const=True)
    identifier: Optional[Identifier]
    type: BundleType
    timestamp: Optional[Instant]
    entry: List[BundleEntry]
