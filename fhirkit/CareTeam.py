from typing import Literal
from pydantic import Field


from fhirkit.Resource import DomainResource


class CareTeam(DomainResource):
    resourceType: Literal["CareTeam"] = Field("CareTeam", const=True)
