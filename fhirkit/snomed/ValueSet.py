from typing import List, Optional, Tuple, Union

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
from pydantic import HttpUrl, PrivateAttr, parse_obj_as, root_validator
from fhirkit.ValueSet import VSCompose, VSExpansion, VSFilter, VSInclude, ValueSet
from fhirkit.elements import CodeableConcept, Coding, Narrative
from fhirkit.snomed.consts import SCT_URI
from fhirkit.snomed.terminology import (
    SCTFHIRTerminologyServer,
    get_default_terminology_server,
)


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
        default_factory=get_default_terminology_server
    )
    status: Literal["draft", "active", "retired", "unknown"] = "active"
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
            filter_rule = inclusion.filter[0]
            if filter_rule.property == "constraint" and filter_rule.op == "=":
                url = inclusion.version or inclusion.system or SCT_URI
                url += "?fhir_vs=ecl/" + inclusion.filter[0].value
            elif filter_rule.property == "concept" and filter_rule.op == "is-a":
                url = inclusion.version or inclusion.system or SCT_URI
                url += "?fhir_vs=isa/" + inclusion.filter[0].value
            else:
                raise RuntimeError(
                    f"Unexepected filter {inclusion.filter[0].json()} in inclusion criterium: {inclusion.json()}"
                )
            return url

    def expand(self, **kwargs):
        self.ensure_fhir_server()
        url = self.equivalent_url()
        self.init_expansion()
        for expanded_vs in self._fhir_server.valueset_expand(url, **kwargs):
            self.extend(expanded_vs.expansion.contains, extend_compose=False)

        self.build_narrative()

    def build_narrative(self):
        self.text = Narrative(
            status="generated",
            div="""
                <div>
                    <style scoped>
                        .dataframe tbody tr th:only-of-type {
                            vertical-align: middle;
                        }

                        .dataframe tbody tr th {
                            vertical-align: top;
                        }

                        .dataframe thead th {
                            text-align: right;
                        }
                    </style>
                    <table border="1" class="dataframe">
                        <thead>
                            <tr style="text-align: right;">
                            <th>code</th>
                            <th>display</th>
                            <th>system</th>
                            <th>version</th>
                            </tr>
                        </thead>
                        <tbody>"""
            + "".join(
                [
                    f"<tr><th>{c.code}</th><td>{c.display}</td><td>{c.system}</td><td>{c.version}</td></tr>"
                    for c in self
                ]
            )
            + """
                        </tbody>
                    </table>
                </div>
            """,
        )

    def validate_code(self, code: Union[Coding, CodeableConcept]):
        self.ensure_fhir_server()
        url = self.equivalent_url()
        assert isinstance(
            code, (Coding, CodeableConcept)
        ), "code should be a Coding or CodeableConcept in order to be able to validate it against a ValueSet"
        if self.has_expanded:
            for member_code in self:
                if code == member_code:
                    return True
            return False
        if isinstance(code, Coding):
            response = self._fhir_server.valueset_validate_code(url, coding=code)
        else:
            response = self._fhir_server.valueset_validate_code(
                url, codeableConcept=code
            )
        return response.result
