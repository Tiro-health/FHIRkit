import abc
from typing import Optional, Tuple, Union
from pydantic.error_wrappers import ValidationError
from fhirkit.data_types import Code
from fhirkit.elements import CodeableConcept, Coding
from pydantic import HttpUrl, parse_obj_as
from abc import ABC


class ExpansionError(Exception):
    pass


class ResourceNoteFoundError(Exception):
    pass


class AbstractFHIRServer(ABC):
    def __init__(self, baseUrl: Union[str, HttpUrl]) -> None:
        self._base_url = parse_obj_as(HttpUrl, baseUrl)

    @property
    def base_url(self):
        return self._base_url

    @abc.abstractmethod
    def get_resource(
        self,
        type: Optional[str] = None,
        *,
        id: Optional[str] = None,
        url: Optional[str] = None,
    ):
        pass

    def __getitem__(self, key: Union[str, Tuple[str, str], HttpUrl]):
        # TODO implement URL keys
        if isinstance(key, HttpUrl):
            return self.get_resource(None, url=key)
        try:
            url = parse_obj_as(HttpUrl, key)
        except ValidationError:
            pass
        else:
            return self.get_resource(None, url=url)
        if isinstance(key, str):
            resourceType, id = key.split("/")
        elif isinstance(key, tuple):
            resourceType, id = key
        else:
            raise TypeError(f"Received a key(={key}) of type {type(key)}")
        return self.get_resource(resourceType, id=id)


class AbstractFHIRTerminologyServer(AbstractFHIRServer):
    @abc.abstractmethod
    def valueset_expand(self, *args, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def valueset_validate_code(
        self,
        url: HttpUrl,
        code: Optional[Code] = None,
        display: Optional[str] = None,
        system: Optional[HttpUrl] = None,
        coding: Optional[Coding] = None,
        codeableConcept: Optional[CodeableConcept] = None,
    ) -> bool:
        raise NotImplementedError()
