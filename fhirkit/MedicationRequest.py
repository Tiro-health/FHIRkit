from typing import Literal
from pydantic import Field


from fhirkit.Resource import DomainResource


class MedicationRequest(DomainResource):
    resourceType: Literal["MedicationRequest"] = Field("MedicationRequest", const=True)
