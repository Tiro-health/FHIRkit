from typing import TYPE_CHECKING, Any, Dict, Type
from pydantic.fields import ModelField

if TYPE_CHECKING:
    from fhirkit.BaseModel import BaseModel

TYPE_NAME_ALIAS = {
    "str": "string",
    "datetime": "dateTime",
    "float": "decimal",
    "int": "integer",
    "bool": "Boolean",
}


def get_matching_type(value: Any, field: ModelField):
    for type_class in field.type_.__args__:
        if isinstance(value, type_class):
            return type_class
    raise TypeError(f"{value} doesn't match any of the specified types ", field.type_)


def deterimine_choice_type(
    cls: Type["BaseModel"], v: Any, values: Dict[str, Any], field: ModelField
):
    """Automatically assign the value from one of the choice type alias fields to current field."""
    if v is not None:
        return v

    non_null_values = list(
        filter(
            lambda t: t[0].startswith(field.name) and t[1] is not None,
            values.items(),
        )
    )
    if len(non_null_values) == 0:
        return
    elif len(non_null_values) > 1:
        raise ValueError(
            f"{cls.__class__.__name__}.{field.name}[x] can only have one value."
        )
    v = non_null_values[0][1]
    return v
