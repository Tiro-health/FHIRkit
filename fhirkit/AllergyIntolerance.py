try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore
from typing import Sequence
from pydantic import Field


from fhirkit.Resource import DomainResource, ResourceWithMultiIdentifier
from fhirkit.elements.elements import Identifier


class AllergyIntolerance(DomainResource, ResourceWithMultiIdentifier):
    resourceType: Literal["AllergyIntolerance"] = Field(
        "AllergyIntolerance", const=True
    )
    identifier: Sequence[Identifier] = Field([])
