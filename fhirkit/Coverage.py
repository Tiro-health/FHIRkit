try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type:ignore
from typing import Sequence
from pydantic import Field
from fhirkit.elements import (
    Identifier,
    Reference
)
from fhirkit.Resource import DomainResource
from fhirkit.elements.elements import Identifier


class Coverage(DomainResource):
    identifier: Sequence[Identifier] = Field(
        None,
        title="Business identifier(s) for this coverage")
    status: Literal["active","cancelled","draft","entered-in-error"] = Field(
        None,
        title="active | cancelled | draft | entered-in-error",
        valueset="https://build.fhir.org/valueset-fm-status.html")
    kind: Literal["insurance","self-pay","other"] = Field(
        None,
        title="insurance | self-pay | other",
        valueset="https://build.fhir.org/valueset-coverage-kind.html")
    beneficiary: Reference = Field(
        None,
        enum_reference_types=["Patient"],
        title="Plan beneficiary")    


