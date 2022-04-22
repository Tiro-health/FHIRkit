from typing import Literal, Optional, Sequence
from pydantic import Field
from fhirkit.Resource import DomainResource
from fhirkit.elements import BackboneElement, CodeableConcept
from fhirkit.data_types import Code


class OperationOutcomeIssue(BackboneElement):
    severity: Literal["fatal", "error", "warning", "information"]
    code: Code  # TODO add logic that can bind this to valueset
    details: Optional[CodeableConcept] = None
    diagnostics: Optional[str] = None
    location: Sequence[str] = []
    expression: Sequence[str] = []

    def __str__(self):
        txt = f"[{self.severity}](issue type={self.code}) "
        if self.diagnostics:
            txt += self.diagnostics
        return txt


class OperationOutcome(DomainResource):
    resourceType = Field("OperationOutcome", const=True)
    issue: Sequence[OperationOutcomeIssue] = []

    def __str__(self) -> str:
        return "OperationOutcome: \n" + "\n\n".join(str(issue) for issue in self.issue)


class OperationOutcomeException(Exception):
    def __init__(self, resource: OperationOutcome) -> None:
        self.resource = resource
        super().__init__(str(resource))
