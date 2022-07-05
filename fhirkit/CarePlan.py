from typing import Literal
from pydantic import Field


from fhirkit.Resource import DomainResource


class CarePlan(DomainResource):
    resourceType: Literal["CarePlan"] = Field("CarePlan", const=True)
