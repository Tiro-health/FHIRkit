from typing import Literal
from pydantic import Field


from fhirkit.Resource import DomainResource


class Medication(DomainResource):
    resourceType: Literal["Medication"] = Field("Medication", const=True)
