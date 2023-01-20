from pydantic import Field, HttpUrl
from fhirkit.elements import Coding

class TiroCoding(Coding):
    system: HttpUrl = Field(default="http://tiro.health/fhir/CodeSystem/auto-generated")

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], str):
            code, display, *_ = (
                x.strip() for x in args[0].split("|")
            )  # break string in pieces
            super().__init__(code=code, display=display, **kwargs)
        else:
            super().__init__(*args, **kwargs)  # business as usual, Pydantic takes over
