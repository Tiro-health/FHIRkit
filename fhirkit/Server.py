from __future__ import annotations
import abc
from typing import TYPE_CHECKING, Optional, Tuple, Union
from pydantic.error_wrappers import ValidationError
from pydantic import HttpUrl, AnyUrl, parse_obj_as
from fhirkit.primitive_datatypes import literal, canonical

if TYPE_CHECKING:
    from .elements import Identifier, Reference
    from .Resource import Resource
from abc import ABC


class ExpansionError(Exception):
    pass


class ResourceNotFoundError(Exception):
    pass


class AbstractFHIRServer(ABC):
    CURRENT_SERVER: Optional[AbstractFHIRServer] = None

    def __init__(self, base_url: Optional[Union[str, HttpUrl]] = None) -> None:
        self._base_url = (
            parse_obj_as(AnyUrl, base_url) if base_url is not None else base_url
        )

    @property
    def base_url(self):
        return self._base_url

    @abc.abstractmethod
    def get_resource_by_canonical(self, reference: Union[canonical, str]) -> "Resource":
        """Resolves a canonical reference into a resource or raises a ResourceNotFound exception.
        More info on canonical references: https://build.fhir.org/references.html#canonical"""
        # check if urn or absolute url
        # check version
        # check fragment
        pass

    @abc.abstractmethod
    def get_resource_by_id(self, resourceId: str, resourceType: Optional[str] = None):
        """Resolves a resourceType and id couple into a resource or raises a ResourceNotFound exception."""

    @abc.abstractmethod
    def get_resource_by_literal(self, reference: literal) -> "Resource":
        """Resolves a literal reference into a resource or raises a ResourceNotFound exception.
        More info on literal references: https://build.fhir.org/references.html#literal"""
        # check if urn
        # check if absolute url
        # check if relative url
        # check if fragment
        pass

    @abc.abstractmethod
    def get_resource_by_identifier(
        self,
        *,
        identifier: "Identifier",
        resourceType: str,
    ) -> "Resource":
        """Resolves an Identifier element into a resource or raises a ResourceNotFound exception."""
        pass

    def get_resource_by_reference(self, reference: "Reference") -> "Resource":
        """Resolves a Reference into a resource or raises a ResourceNotFound exception"""
        try:
            if reference.reference is not None:
                return self.get_resource_by_literal(reference.reference)
        except ResourceNotFoundError:
            pass

        try:
            if reference.identifier is not None and reference.type is not None:
                return self.get_resource_by_identifier(
                    identifier=reference.identifier, resourceType=reference.type
                )
        except ResourceNotFoundError:
            pass
        raise ResourceNotFoundError(f"Could not resolve reference: {reference}")
