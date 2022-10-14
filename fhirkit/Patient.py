try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
from pydantic import Field
from typing import Optional, Sequence
from fhirkit.primitive_datatypes import dateTime
from fhirkit.Resource import DomainResource
from fhirkit.elements import CodeableConcept, HumanName, Identifier, Reference, ContactDetail, ContactPoint, Address

PatientGender = Literal[
    "male",
    "female",
    "other",
    "unknown"
]

class Patient(DomainResource):
    resourceType: Literal["Patient"] = Field("Patient", const=True)
    identifier: Identifier = Field(None, repr=True)
    active: Optional[bool] = None
    name: Optional[HumanName] = Field(None, repr=True)
    telecom: Sequence[ContactPoint] = []
    gender: PatientGender = Field("unknown", repr=True)
    birthDate: Optional[dateTime]  = Field(None, repr=True)
    deceasedBoolean: Optional[bool] = Field(None, exclude=True)
    deceasedDateTime: Optional[dateTime] = Field(None, exclude=True)
    address: Optional[Address] = Field(None, exclude=True) 
    maritalStatus: Optional[CodeableConcept] = Field(None, exclude=True)  
    multipleBirthBoolean: Optional[bool] = Field(None, exclude=True)
    multipleBirthInteger: Optional[int] = Field(None, exclude=True)
    contact: Sequence[ContactDetail] = []
    generalPractitioner: Optional[Reference] = None
    managingOrganization: Optional[Reference] = None
    #Custom fields
    age:Optional[int] = Field(None, exclude=True)


