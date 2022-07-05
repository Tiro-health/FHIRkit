try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
from pydantic import Field


from fhirkit.Resource import DomainResource


class Condition(DomainResource):
    resourceType: Literal["Condition"] = Field("Condition", const=True)
