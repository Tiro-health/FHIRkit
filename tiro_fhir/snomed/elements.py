from typing import Optional
from pydantic import Field, HttpUrl
from tiro_fhir.Server import AbstractFHIRServer
from tiro_fhir.elements import CodeableConcept, Coding 
from tiro_fhir.ValueSet import ValueSet
from .ValueSet import SCTDescendantsFilter, SCTImplicitCompose, SCTImplicitInclude, SCTImplicitValueSet

class SCTCoding(Coding):
    system: HttpUrl = Field(default="http://snomed.info/sct")

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], str):
            code, display, *_ = (x.strip() for x in args[0].split("|")) # break string in pieces
            super().__init__(code=code, display=display,**kwargs)
        else:
            super().__init__(*args, **kwargs) # business as usual, Pydantic takes over

    def descendants(self, fhir_server:Optional[AbstractFHIRServer] = None) -> ValueSet:
        return SCTImplicitValueSet(
            url=f"{self.system}?fhir_vs=isa/{self.code}",
            compose=SCTImplicitCompose(
                include=[
                    SCTImplicitInclude(
                        system=self.system,
                        filter=[SCTDescendantsFilter(property="concept", op="is-a", value=self.code)],
                    )
                ]
            ),
            fhir_server=fhir_server
        )

class SCTConcept(CodeableConcept):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], str):
            sct_coding = SCTCoding(args[0])
            super().__init__(text=sct_coding.display, coding=[sct_coding], **kwargs)
        else:
            super().__init__(*args, **kwargs) # business as usual, Pydantic takes over