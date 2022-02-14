from typing import Any, Generic, List, Optional, TypeVar
from pydantic import Field
from pydantic.generics import GenericModel
from tiro_fhir.Resource import Resource
from tiro_fhir.elements import BackboneElement


class AbstractParameter(BackboneElement):
    name: str
    value: Optional[Any] = Field(None,alias="valueBoolean")
    resource: Optional[Resource]


Name = TypeVar("Name")
Value = TypeVar("Value")


class ValueParameter(GenericModel, Generic[Name, Value], AbstractParameter):
    name: Name
    value: Value
    resource: None = Field(None, const=True)


class Parameter(Resource):
    parameter: List[AbstractParameter]

    def __getattribute__(self, __name: str) -> Any:
        try:
            return super().__getattribute__(__name)
        except AttributeError:
            for param in self.parameter:
                if param.name == __name:
                    return param.value
            raise
