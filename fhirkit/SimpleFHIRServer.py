from typing import Generic, Optional, Sequence, TypeVar, Union

from pydantic import HttpUrl
from fhirkit.Server import AbstractFHIRServer, ResourceNoteFoundError
from fhirkit.Resource import Resource

R = TypeVar("R", bound=Resource)


class SimpleFHIRServer(Generic[R], AbstractFHIRServer):
    def __init__(self, resources: Sequence[R], base_url: Union[str, HttpUrl]) -> None:
        self._resources = resources
        super().__init__(base_url)

    def get_resource(
        self,
        resourceType: str,
        *,
        id: Optional[str] = None,
        url: Optional[Union[str, HttpUrl]] = None,
    ):
        if url is None:
            if id is None:
                raise RuntimeError(
                    "At least resource.id or resource.url must be given to be able to identify the requested resource"
                )
            url = self.base_url + "/" + resourceType + "/" + id
        assert self._resources is not None
        for r in self._resources:
            if (r.resourceType == resourceType or resourceType is None) and (
                r.url == url or r.id == id
            ):
                return r
        t = resourceType or "Resource"
        raise ResourceNoteFoundError(f"{t} with url={url} not found.")
