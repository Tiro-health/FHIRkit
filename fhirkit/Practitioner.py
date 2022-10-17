try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore
from pydantic import Field
from typing import Optional, Sequence
from fhirkit.Resource import DomainResource
from fhirkit.elements import (
    dateTime,
    HumanName,
    Identifier,
    ContactPoint,
    Address,
)


class Practitioner(DomainResource):
    resourceType: Literal["Practitioner"] = Field("Practitioner", const=True)
    identifier: Sequence[Identifier] = Field([], repr=True)
    active: Optional[bool] = Field(None, repr=True)
    name: Sequence[HumanName] = Field([], repr=True)
    telecom: Sequence[ContactPoint] = Field([], repr=True)
    address: Sequence[Address] = Field([], repr=True)
    gender: Optional[Literal["male", "female", "other", "unknown"]] = Field(None, repr=True)
    birthDate: Optional[dateTime] = Field(None, repr=True)
