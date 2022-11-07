try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore
from pydantic import Field, validator
from typing import Optional, Sequence, Union, List
from fhirkit.choice_type import deterimine_choice_type, ChoiceType
from fhirkit.primitive_datatypes import dateTime, date
from fhirkit.Resource import DomainResource
from fhirkit.elements import (
    CodeableConcept,
    HumanName,
    Identifier,
    Reference,
    Address,
    AdministrativeGender,
)
from fhirkit.metadata_types import ContactDetail, ContactPoint


class Patient(DomainResource):
    resourceType: Literal["Patient"] = Field("Patient", const=True)
    identifier: Sequence[Identifier] = Field([], repr=True)
    active: Optional[bool] = None
    name: Optional[Sequence[HumanName]] = Field([], repr=True)
    telecom: Optional[Sequence[ContactPoint]] = Field([], repr=True)
    gender: Optional[AdministrativeGender] = Field(None, repr=True)
    birthDate: Optional[date] = Field(None, repr=True)
    deceasedBoolean: Optional[bool] = Field(None, exclude=True)
    deceasedDateTime: Optional[dateTime] = Field(None, exclude=True)
    deceased: Union[bool, dateTime, None] = ChoiceType(None)
    address: Optional[Sequence[Address]] = Field([], repr=True)
    maritalStatus: Optional[CodeableConcept] = Field(None, repr=True)
    multipleBirthBoolean: Optional[bool] = Field(None, exclude=True)
    multipleBirthInteger: Optional[int] = Field(None, exclude=True)
    multipleBirth: Optional[Union[bool, int]] = ChoiceType(None)
    contact: Optional[Sequence[ContactDetail]] = []
    generalPractitioner: Optional[Sequence[Reference]] = Field([], repr=True)
    managingOrganization: Optional[Reference] = Field(None, repr=True)

    @validator("deceased", pre=True, always=True, allow_reuse=True)
    def validate_deceased(cls, v, values, field):
        return deterimine_choice_type(cls, v, values, field)

    @validator("multipleBirth", pre=True, always=True, allow_reuse=True)
    def validate_multipleBirth(cls, v, values, field):
        return deterimine_choice_type(cls, v, values, field)
