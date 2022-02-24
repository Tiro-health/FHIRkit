from datetime import date, datetime
from typing import Any, ClassVar, Generic, List, Literal, Optional, Sequence, TypeVar, Union
import warnings
from pydantic import BaseModel, Field, HttpUrl, StrictInt, StrictStr, root_validator, StrictBool
from pydantic.generics import GenericModel
from tiro_fhir.Resource import Resource
from tiro_fhir.elements import BackboneElement

TYPE_TO_NAME = {
    str: "String",
    bool: "Boolean",
    int: "Integer",
    float: "Float",
    datetime: "DateTime",
    date: "Date",
    HttpUrl: "Uri"
}

class MultiValueType(BaseModel):
    _polymorphic_fields:ClassVar[Sequence[str]] = ["value",]
    valueBoolean: Optional[StrictBool]
    valueString: Optional[StrictStr]
    valueUri: Optional[HttpUrl]
    valueInteger: Optional[StrictInt]

    @root_validator(pre=True)
    def validate_value(cls, values) -> None:
        for polymorphic_field in cls._polymorphic_fields:
            if polymorphic_field in values:
                value = values[polymorphic_field]
                ext_field_name = polymorphic_field
                if type(value) in TYPE_TO_NAME:
                    ext_field_name += TYPE_TO_NAME[type(value)]
                else:
                    ext_field_name += str(type(value).__name__).capitalize()
                values.update({ext_field_name: value})
        return values

    def __iter__(self, *args, reduce_polymorphic:bool=False, **kwargs): 
        for (key, value) in super().__iter__(*args, **kwargs):
            yielded = False
            if reduce_polymorphic and value:
                for polymophic_field in self._polymorphic_fields:
                    if key.startswith(polymophic_field):
                        yield (polymophic_field, value)
                        yielded = True
                        break
                if not yielded:
                    yield (key, value)

    def dict(self, *, include: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None, exclude: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None, by_alias: bool = False, skip_defaults: bool = None, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, reduce_polymorphic: bool = False):
        """
        Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

        """
        if skip_defaults is not None:
            warnings.warn(
                f'{self.__class__.__name__}.dict(): "skip_defaults" is deprecated and replaced by "exclude_unset"',
                DeprecationWarning,
            )
            exclude_unset = skip_defaults

        return dict(
            self._iter(
                to_dict=True,
                by_alias=by_alias,
                include=include,
                exclude=exclude,
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                exclude_none=exclude_none,
                reduce_polymorphic=reduce_polymorphic
            )
        )
class AbstractParameter(BackboneElement):
    name: str
  

Name = TypeVar("Name")
Value = TypeVar("Value")

class ValueParameter(GenericModel, Generic[Name, Value], AbstractParameter):
    name: Name
    value: Value
    resource: None = Field(None, const=True)

class Parameter(Resource):
    resourceType = Field("Parameter", const=True)
    parameter: List[AbstractParameter]

    def __getattribute__(self, __name: str) -> Any:
        try:
            return super().__getattribute__(__name)
        except AttributeError:
            for param in self.parameter:
                if param.name == __name:
                    return param.value
            raise
