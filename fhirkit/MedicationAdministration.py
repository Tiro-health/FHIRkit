from typing import Literal
from pydantic import Field


from fhirkit.Resource import DomainResource


class MedicationAdministration(DomainResource):
    resourceType: Literal["MedicationAdministration"] = Field(
        "MedicationAdministration", const=True
    )
