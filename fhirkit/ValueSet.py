from datetime import date, datetime

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal # type: ignore
from typing import Iterable, List, Optional, Sequence, Union
from pydantic import Field
from fhirkit.BaseModel import BaseModel
from fhirkit.primitive_datatypes import URI, dateTime
from fhirkit.elements import (
    BackboneElement,
    CodeableConcept,
    Coding,
    Narrative,
    UsageContext,
)
from fhirkit.Resource import CanonicalResource


class VSDesignation(BaseModel):
    language: Optional[str]
    use: Optional[Coding]
    value: str


class VSConcept(BaseModel):
    code: str
    display: Optional[str]
    designation: List[VSDesignation] = Field(default=[])


class VSFilter(BackboneElement):
    property: str
    op: Literal[
        "=",
        "is-a",
        "descendent-of",
        "is-not-a",
        "regex",
        "in",
        "not-in",
        "generalizes",
        "child-of",
        "descendent-leaf",
        "exists",
    ]
    value: str


class VSInclude(BackboneElement):
    system: Optional[URI] = None
    version: Optional[str] = None
    concept: Sequence[VSConcept] = Field(default=[])
    filter: Sequence[VSFilter] = Field(default=[])
    valueSet: Sequence[URI] = Field(default=[])


class VSCompose(BaseModel):
    include: Sequence[VSInclude] = []
    exclude: Sequence[VSInclude] = []
    property: Sequence[str] = []
    lockedDate: Optional[date]
    inactive: Optional[bool]


class VSCodingWithDesignation(Coding):
    designation: List[VSDesignation] = Field(default=[])


class VSExpansion(BaseModel):
    offset: Optional[int] = None
    total: Optional[int] = None
    contains: List[VSCodingWithDesignation] = []
    identifier: Optional[URI] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class ValueSet(CanonicalResource):
    resourceType: Literal["ValueSet"] = Field("ValueSet", const=True)
    url: Optional[URI]
    name: Optional[str]
    compose: Optional[VSCompose]
    expansion: Optional[VSExpansion]
    useContext: Sequence[UsageContext] = Field([], repr=True)

    @property
    def has_expanded(self):
        return self.expansion is not None

    def expand(self):
        """Override this method to implement expansion logic.
        This method should fill ValueSet.expansion.contains with concepts.

        Implementing this method enables you to iterate over the ValueSet in a for-loop.
        ```python
        class MyCustomValueSet(ValueSet)

            def expand(self):
                # some expansion logic

        vs_example = MyCustomValueSet()
        for coding in vs:
            print(coding)
        "
        """
        raise NotImplementedError()

    def validate_code(self, code: Union[Coding, CodeableConcept]):
        raise NotImplementedError()

    def init_expansion(self):
        self.expansion = VSExpansion()


class SimpleValueSet(ValueSet):
    status: Literal["active"] = Field("active", const=True)
    expansion: VSExpansion

    def __init__(self, *args: VSCodingWithDesignation, **kwargs):
        if len(args) > 0:

            assert "expansion" not in kwargs, "When passing an iterable with concepts, `expansion` should be None."
            super().__init__(
                expansion=VSExpansion.parse_obj({"contains":[c.dict() for c in args], "total":len(args)}),
                text=Narrative(
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
                            for c in args
                        ]
                    )
                    + """
                        </tbody>
                    </table>
                </div>""",
                ),
                **kwargs,
            )
        else:
            super().__init__(**kwargs)

    def append(
        self,
        code: VSCodingWithDesignation,
    ):

        assert self.expansion is not None, "`self.expansion` is None after initialisation with `self.init_expansion`"
        self.expansion.contains.append(code)

    def extend(
        self,
        codes: Iterable[VSCodingWithDesignation],
    ):
        assert self.expansion is not None, "`self.expansion` is None after initialisation with `self.init_expansion`"
        self.expansion.contains.extend(codes)

    def validate_code(self, code: Union[Coding, CodeableConcept]):
        if isinstance(code, CodeableConcept):
            return any(self.validate_code(c) for c in code.coding)
        elif isinstance(code, Coding):
            return any(c == code for c in self)
        else:
            return False


ValueSet.update_forward_refs()
