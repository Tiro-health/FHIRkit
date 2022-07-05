from typing import Literal
from pydantic import Field


from fhirkit.Resource import DomainResource


class Practitioner(DomainResource):
    resourceType: Literal["Practitioner"] = Field("Practitioner", const=True)
