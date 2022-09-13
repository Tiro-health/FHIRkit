import abc
from typing import Optional, Tuple, Union
from pydantic.error_wrappers import ValidationError
from pydantic import HttpUrl, parse_obj_as
from abc import ABC


class ExpansionError(Exception):
    pass


class ResourceNotFoundError(Exception):
    pass


class AbstractFHIRServer(ABC):
    def __init__(self, base_url: Optional[Union[str, HttpUrl]] = None) -> None:
        self._base_url = base_url

    @property
    def base_url(self):
        return self._base_url

    @abc.abstractmethod
    def get_resource(
        self,
        resourceType: Optional[str],
        *,
        id: Optional[str] = None,
        uri: Optional[str] = None,
    ):
        pass

    def __getitem__(self, key: Union[str, Tuple[str, str], HttpUrl]):
        # TODO implement URL keys
        if isinstance(key, HttpUrl):
            return self.get_resource(None, uri=key)
        try:
            uri = parse_obj_as(HttpUrl, key)
        except ValidationError:
            pass
        else:
            return self.get_resource(None, uri=uri)
        if isinstance(key, str):
            if len(key.split("/")) == 2:
                resourceType, id = key.split("/")
            else:
                resourceType = None
                id = key
        elif isinstance(key, tuple):
            resourceType, id = key
        else:
            raise TypeError(f"Received a key(={key}) of type {type(key)}")
        return self.get_resource(resourceType, id=id)
