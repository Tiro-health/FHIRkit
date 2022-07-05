from typing import Literal
from pydantic import Field


from fhirkit.Resource import DomainResource


class Location(DomainResource):
    resourceType: Literal["Location"] = Field("Location", const=True)
