from typing import Literal
from pydantic import Field


from fhirkit.Resource import DomainResource


class Condition(DomainResource):
    resourceType: Literal["Condition"] = Field("Condition", const=True)
