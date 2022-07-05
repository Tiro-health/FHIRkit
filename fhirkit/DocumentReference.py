from typing import Literal
from pydantic import Field


from fhirkit.Resource import DomainResource


class DocumentReference(DomainResource):
    resourceType: Literal["DocumentReference"] = Field("DocumentReference", const=True)
