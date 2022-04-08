from typing import Optional, Sequence
from tiro_fhir.elements import ContactPoint, Element


class ContactDetail(Element):
    name: Optional[str]
    telecom: Sequence[ContactPoint]
