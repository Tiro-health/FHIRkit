from typing import Literal
from pydantic import Field


from fhirkit.Resource import DomainResource


class Organization(DomainResource):
    resourceType: Literal["Organization"] = Field("Organization", const=True)
