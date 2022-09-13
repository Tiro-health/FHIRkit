try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
from typing import Optional
from pydantic import Field


from fhirkit.Resource import DomainResource
from .elements.elements import CodeableConcept, Reference


class Encounter(DomainResource):
    resourceType: Literal["Encounter"] = Field("Encounter", const=True)
    subject: Optional[Reference] = None
    reasonCode: Optional[CodeableConcept] = None
    reasonReference: Optional[Reference] = None
