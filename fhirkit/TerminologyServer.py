from typing import Optional
import abc
from fhirkit.elements import URI, Code, Coding, CodeableConcept
from fhirkit.Server import AbstractFHIRServer


class AbstractFHIRTerminologyServer:
    @abc.abstractmethod
    def valueset_expand(self, *args, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def valueset_validate_code(
        self,
        url: URI,
        code: Optional[Code] = None,
        display: Optional[str] = None,
        system: Optional[URI] = None,
        coding: Optional[Coding] = None,
        codeableConcept: Optional[CodeableConcept] = None,
    ) -> bool:
        raise NotImplementedError()
