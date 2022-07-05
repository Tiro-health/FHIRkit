from typing import Literal
from pydantic import Field


from fhirkit.Resource import DomainResource


class Encounter(DomainResource):
    resourceType: Literal["Encounter"] = Field("Encounter", const=True)
