from typing import Literal
from pydantic import Field


from fhirkit.Resource import DomainResource


class AllergyIntolerance(DomainResource):
    resourceType: Literal["AllergyIntolerance"] = Field(
        "AllergyIntolerance", const=True
    )
