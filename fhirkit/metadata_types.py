from typing import Optional, Sequence
from fhirkit.elements import ContactPoint, Element


class ContactDetail(Element):
    name: Optional[str]
    telecom: Sequence[ContactPoint] = []
