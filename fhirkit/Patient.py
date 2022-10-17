try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore
from pydantic import Field, validator
from typing import Optional, Sequence, Union
from fhirkit.choice_type.validators import deterimine_choice_type
from fhirkit.primitive_datatypes import dateTime, date
from fhirkit.Resource import DomainResource
from fhirkit.elements import (
    CodeableConcept,
    HumanName,
    Identifier,
    Reference,
    ContactDetail,
    ContactPoint,
    Address,
)

PatientGender = Literal["male", "female", "other", "unknown"]


class Patient(DomainResource):
    resourceType: Literal["Patient"] = Field("Patient", const=True)
    identifier: Sequence[Identifier] = Field([], repr=True)
    active: Optional[bool] = None
    name: Sequence[HumanName] = Field([], repr=True)
    telecom: Sequence[ContactPoint] = Field([], repr=True)
    gender: PatientGender = Field("unknown", repr=True)
    birthDate: Optional[date] = Field(None, repr=True)
    deceased: Union[bool, dateTime, None] = Field(None, repr=True)
    deceasedBoolean: Optional[bool] = Field(None, exclude=True)
    deceasedDateTime: Optional[dateTime] = Field(None, exclude=True)
    address: Sequence[Address] = Field([], repr=True)
    maritalStatus: Optional[CodeableConcept] = Field(None, exclude=True)
    multipleBirthBoolean: Optional[bool] = Field(None, exclude=True)
    multipleBirthInteger: Optional[int] = Field(None, exclude=True)
    contact: Sequence[ContactDetail] = []
    generalPractitioner: Optional[Reference] = None
    managingOrganization: Optional[Reference] = None
    # Custom fields
    age: Optional[int] = Field(None, exclude=True)

    @validator("deceased", pre=True, always=True, allow_reuse=True)
    def validate_value(cls, v, values, field):
        return deterimine_choice_type(
            cls,
            v,
            values,
            field,
        )
