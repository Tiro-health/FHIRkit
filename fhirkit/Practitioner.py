try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
from pydantic import Field
from typing import Optional, Sequence
from fhirkit.Resource import DomainResource
from fhirkit.elements import dateTime, HumanName, Identifier, PatientGender, ContactDetail, ContactPoint, Address


class Practitioner(DomainResource):
    identifier: Optional[Identifier] = Field(None, repr=True)
    active: Optional[bool] = Field(None, exclude=True)
    name: Optional[HumanName] = Field(None, repr=True)
    telecom: Sequence[ContactPoint] = []
    address: Optional[Address] = Field(None, exclude=True) 
    gender: PatientGender = Field("unknown", repr=True)    
    birthDate: Optional[dateTime] = Field(None, repr=True)
    #Custom fields
    hospital: Optional[str] = Field(None, repr=True)
