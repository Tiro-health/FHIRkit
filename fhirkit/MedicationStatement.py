from typing import Literal
from pydantic import Field


from fhirkit.Resource import DomainResource


class MedicationStatement(DomainResource):
    resourceType: Literal["MedicationStatement"] = Field(
        "MedicationStatement", const=True
    )
