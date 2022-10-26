from importlib.resources import Resource
from typing import List, Union
import typing


try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore

from pydantic import Field, parse_obj_as
from fhirkit.Resource import RESOURCE_MODELS

AnyPatientResource = Annotated[
    Union[tuple(RESOURCE_MODELS)],
    Field(discriminator="resourceType"),
]


def parse_json_as_resource(json: str):
    return parse_obj_as(AnyPatientResource, json)
