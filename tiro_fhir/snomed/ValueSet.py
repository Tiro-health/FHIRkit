from typing import List, Literal, Tuple, Union
from pydantic import HttpUrl
from tiro_fhir.ValueSet import VSCompose, VSExpansion, VSFilter, VSInclude, ValueSet
from tiro_fhir.elements import AbstractCoding, CodeableConcept


class SCTDescendantsFilter(VSFilter):
    property: Literal["concept"]
    op: Literal["is-a"]
    value: str
class SCTImplicitInclude(VSInclude):
    concept:List = []
    valueSetList = []
    filter: Tuple[SCTDescendantsFilter]

class SCTImplicitCompose(VSCompose):
    include: Tuple[SCTImplicitInclude]

class SCTImplicitValueSet(ValueSet):
    url: HttpUrl
    compose: SCTImplicitCompose

    def expand(self):
        if self.fhir_server:
            expansion = VSExpansion(contains=[])
            for code in self.fhir_server.expand_value_set(self):
                expansion.contains.append(code)
            self.expansion = expansion
        else:
            raise RuntimeWarning(
                "Can't expand an implicit SNOMED-CT without a FHIR server."
            )
    def __contains__(self, item: Union[AbstractCoding, CodeableConcept]) -> bool:
        if isinstance(item, CodeableConcept):
            raise NotImplementedError()
        if self.fhir_server:
            return self.fhir_server.validate_code_in_valueset(self, coding=item)
        else:
            raise RuntimeWarning(
                "Can't test valueset membership of SNOMED-CT valuesets without a FHIR server."
            )

class SCTDescendantsFilter(VSFilter):
    property: Literal["concept"]
    op: Literal["is-a"]
    value: str
