from __future__ import annotations
from typing import (
    Any,
    Sequence,
)

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore

from pydantic import Field
from fhirkit import r5
from fhirkit.utils.deprecated import deprecated


class CodeLookupError(KeyError):
    pass


@deprecated(reason="Use r5.CodeSystem instead")
class CSConceptDesignation(r5.CodeSystemConceptDesignation):
    pass


class CSConceptProperty(r5.CodeSystemConceptProperty):
    @property
    def value(
        self,
    ) -> (
        r5.code
        | r5.Coding
        | r5.string
        | r5.integer
        | r5.boolean
        | r5.dateTime
        | r5.decimal
    ):
        for prop in self.__fields__.keys():
            if prop.startswith("value"):
                v = getattr(self, prop)
                if v is not None:
                    return v
        raise RuntimeError("No value found in CSConceptProperty")

    def __str__(self) -> str:
        return str(self.code) + ": " + str(self.value)


class CSConcept(r5.CodeSystemConcept):
    property: Sequence[CSConceptProperty] = []
    concept: Sequence[CSConcept] = []

    def __getattribute__(self, __name: str) -> Any:
        try:
            return super().__getattribute__(__name)
        except AttributeError:
            for param in self.property:
                if param.code == __name:
                    return param.value
            raise

    def __str__(self) -> str:
        return (
            f"#{self.code} '{self.display}'"
            + "\nproperties: \n"
            + "\n".join(" " + str(p) for p in self.property if p.value is not None)
        )


class CSConceptLookup(CSConcept):
    name: str


class CodeSystem(r5.CodeSystem):
    resourceType: Literal["CodeSystem"] = Field("CodeSystem", const=True)


CodeSystem.update_forward_refs()
