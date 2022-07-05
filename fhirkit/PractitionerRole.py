from typing import Literal
from pydantic import Field


from fhirkit.Resource import DomainResource


class PractitionerRole(DomainResource):
    resourceType: Literal["PractitionerRole"] = Field("PractitionerRole", const=True)
