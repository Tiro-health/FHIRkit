try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore
from pydantic import Field


from fhirkit.Resource import DomainResource


class CarePlan(DomainResource):
    resourceType: Literal["CarePlan"] = Field("CarePlan", const=True)
