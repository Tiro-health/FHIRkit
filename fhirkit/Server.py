import abc
from typing import Optional, Tuple, Union
from pydantic.error_wrappers import ValidationError
from pydantic import HttpUrl, parse_obj_as
from abc import ABC


class ExpansionError(Exception):
    pass


class ResourceNoteFoundError(Exception):
    pass


class AbstractFHIRServer(ABC):
    def __init__(self, base_url: Optional[Union[str, HttpUrl]] = None) -> None:
        self._base_url = (
            parse_obj_as(HttpUrl, base_url) if base_url is not None else None
        )

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
            if len(key.split("/")) > 1:
                resourceType, id = key.split("/")
            else:
                resourceType = None
                id = key
        elif isinstance(key, tuple):
            resourceType, id = key
        else:
            raise TypeError(f"Received a key(={key}) of type {type(key)}")
        return self.get_resource(resourceType, id=id)
