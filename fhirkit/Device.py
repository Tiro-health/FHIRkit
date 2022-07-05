try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
from pydantic import Field


from fhirkit.Resource import DomainResource


class Device(DomainResource):
    resourceType: Literal["Device"] = Field("Device", const=True)
