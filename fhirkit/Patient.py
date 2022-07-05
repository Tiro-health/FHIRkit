from typing import Literal
from pydantic import Field


from fhirkit.Resource import DomainResource


class Patient(DomainResource):
    resourceType: Literal["Patient"] = Field("Patient", const=True)
