try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore
from typing import Iterable, Sequence, Union, List
from pydantic import Field, validator
from fhirkit import r5
from fhirkit.utils.deprecated import deprecated
from fhirkit.elements import (
    CodeableConcept,
    Coding,
)


@deprecated(reason="Use r5.ValueSetComposeIncludeConceptDesignation instead")
class VSDesignation(r5.ValueSetComposeIncludeConceptDesignation):
    """This class is deprecated. Use r5.ValueSetComposeIncludeConceptDesignation instead."""

    pass


@deprecated(reason="Use r5.ValueSetComposeIncludeConcept instead")
class VSConcept(r5.ValueSetComposeIncludeConcept):
    """This class is deprecated. Use r5.ValueSetComposeIncludeConcept instead."""

    pass


ALLOWED_OPERATORS = [
    r5.code("="),
    r5.code("is-a"),
    r5.code("descendent-of"),
    r5.code("is-not-a"),
    r5.code("regex"),
    r5.code("in"),
    r5.code("not-in"),
    r5.code("generalizes"),
    r5.code("child-of"),
    r5.code("descendent-leaf"),
    r5.code("exists"),
]


class VSFilter(r5.ValueSetComposeIncludeFilter):
    """Select concepts by specifying a matching criterion based on the properties (including relationships) defined by the system, or on filters defined by the system. If multiple filters are specified within the include, they SHALL all be true."""

    op: r5.code = Field(default=...)
    "The kind of operation to perform as a part of the filter criteria."

    @validator("op")
    def operator_must_be_allowed(cls, v):
        if v not in ALLOWED_OPERATORS:
            raise ValueError(
                f"Operator {v.operator} is not allowed. Allowed operators are {ALLOWED_OPERATORS}"
            )
        return v


class VSInclude(r5.ValueSetComposeInclude):
    """Include one or more codes from a code system or other value set(s)."""

    filter: Sequence[VSFilter] = Field(default_factory=list)


class VSCompose(r5.ValueSetCompose):
    """A set of criteria that define the contents of the value set by including or excluding codes selected from the specified code system(s) that the value set draws from. This is also known as the Content Logical Definition (CLD)."""

    include: Sequence[VSInclude] = Field(default=...)
    "Include one or more codes from a code system or other value set(s)."
    exclude: Sequence[VSInclude] = Field(default_factory=list)
    "Exclude one or more codes from the value set based on code system filters and/or other value sets."


@deprecated(reason="Use r5.ValueSetExpansionContainsProperty instead")
class VSCodingProperty(r5.ValueSetExpansionContainsProperty):
    """This class is deprecated. Use r5.ValueSetExpansionContainsProperty instead."""

    pass


@deprecated(reason="Use r5.ValueSetExpansionContains instead")
class VSCodingWithDesignation(r5.ValueSetExpansionContains):
    """This class is deprecated. Use r5.ValueSetExpansionContains instead."""


@deprecated(reason="Use r5.ValueSetExpansion instead")
class VSExpansion(r5.ValueSetExpansion):
    """This class is deprecated. Use r5.ValueSetExpansion instead."""


class ValueSet(r5.ValueSet):
    resourceType: Literal["ValueSet"] = Field("ValueSet", const=True)
    compose: VSCompose | None = Field(default=None)
    "A set of criteria that define the contents of the value set by including or excluding codes selected from the specified code system(s) that the value set draws from. This is also known as the Content Logical Definition (CLD)."


class SimpleValueSet(ValueSet):
    status: r5.code = Field("active", const=True)
    expansion: VSExpansion

    def __init__(self, *args: VSCodingWithDesignation, **kwargs):
        if len(args) > 0:
            assert (
                "expansion" not in kwargs
            ), "When passing an iterable with concepts, `expansion` should be None."
            super().__init__(
                expansion=VSExpansion.parse_obj(
                    {"contains": [c.dict() for c in args], "total": len(args)}
                ),
                text=r5.Narrative(
                    status=r5.code("generated"),
                    div=r5.xhtml(
                        """
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
                ),
                **kwargs,
            )
        else:
            super().__init__(**kwargs)

    def append(
        self,
        code: VSCodingWithDesignation,
    ):
        assert (
            self.expansion is not None
        ), "`self.expansion` is None after initialisation with `self.init_expansion`"
        self.expansion.contains = list(self.expansion.contains) + [code]

    def extend(
        self,
        codes: Iterable[VSCodingWithDesignation],
    ):
        assert (
            self.expansion is not None
        ), "`self.expansion` is None after initialisation with `self.init_expansion`"
        self.expansion.contains = list(self.expansion.contains) + list(codes)

    def validate_code(self, code: Union[Coding, CodeableConcept]):
        if isinstance(code, CodeableConcept):
            return any(self.validate_code(c) for c in code.coding)
        elif isinstance(code, Coding):
            return any(c == code for c in self)
        else:
            return False


ValueSet.update_forward_refs()
