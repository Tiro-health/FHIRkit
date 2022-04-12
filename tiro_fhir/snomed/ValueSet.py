from typing import List, Literal, Optional, Tuple, Union
from pydantic import HttpUrl, PrivateAttr, root_validator
from tiro_fhir.ValueSet import VSCompose, VSExpansion, VSFilter, VSInclude, ValueSet
from tiro_fhir.elements import CodeableConcept, Coding
from tiro_fhir.snomed.consts import SCT_URI
from tiro_fhir.snomed.terminology import SCTFHIRTerminologyServer


class SCTDescendantsFilter(VSFilter):
    property: Literal["concept"]
    op: Literal["is-a"]
    value: str


class SCTECLFilter(VSFilter):
    property: Literal["constraint"]
    op: Literal["="]
    value: str


class SCTImplicitInclude(VSInclude):
    concept: List = []
    valueSetList = []
    filter: Tuple[Union[SCTDescendantsFilter, SCTECLFilter]]


class SCTImplicitCompose(VSCompose):
    include: Tuple[SCTImplicitInclude]


class SCTImplicitValueSet(ValueSet):
    _fhir_server: SCTFHIRTerminologyServer = PrivateAttr(
        SCTFHIRTerminologyServer.default_server()
    )
    url: Optional[Union[HttpUrl, str]]
    compose: Optional[SCTImplicitCompose]

    @root_validator
    def check_either_url_or_compose(cls, values):
        url, compose = values.get("url"), values.get("compose")
        if url is None and compose is None:
            raise ValueError(
                "Either a 'url' or a 'compose' section should be specified to have a valid ValueSet."
            )
        return values

    def ensure_fhir_server(self):
        if self._fhir_server is None:
            raise RuntimeWarning(
                "Can't expand an implicit SNOMED-CT without a FHIR server."
            )
        return True

    def equivalent_url(self):
        if self.url:
            return self.url
        else:
            assert (
                self.compose is not None
            ), "If no url is specified at least a compose section should be available"
            inclusion = self.compose.include[0]
            if inclusion.filter[0].property == "constraint":
                url = inclusion.version or inclusion.system or SCT_URI
                url += "?fhir_vs=ecl/" + inclusion.filter[0].value
            elif inclusion.filter[0].property == "constraint":
                url = inclusion.version or inclusion.system or SCT_URI
                url += "?fhir_vs=isa/" + inclusion.filter[0].value
            else:
                raise RuntimeError("Unexepected case in if-else statement.")
            return url

    def expand(self):
        self.ensure_fhir_server()
        url = self.equivalent_url()
        self.extend(self._fhir_server.valueset_expand(url), extend_compose=False)

    def validate_code(self, code: Union[Coding, CodeableConcept]):
        self.ensure_fhir_server()
        url = self.equivalent_url()
        assert isinstance(
            code, (Coding, CodeableConcept)
        ), "code should be a Coding or CodeableConcept in order to be able to validate it against a ValueSet"
        if isinstance(code, Coding):
            response = self._fhir_server.valueset_validate_code(url, coding=code)
        else:
            response = self._fhir_server.valueset_validate_code(
                url, codeableConcept=code
            )
        return response.result
