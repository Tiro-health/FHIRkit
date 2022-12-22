import logging
from pathlib import Path
import resource
from typing import (
    Callable,
    Generator,
    Generic,
    List,
    Optional,
    Sequence,
    TypeVar,
    Union,
)
from uuid import uuid5, uuid4

from pydantic import HttpUrl, ValidationError, parse_file_as, parse_obj_as
from fhirkit.elements.elements import CodeableConcept, Coding, Reference, Identifier
from fhirkit.primitive_datatypes import (
    URI,
    AbsoluteURL,
    Code,
    RelativeURL,
    URN,
    canonical,
    literal,
)
from fhirkit.Bundle import Bundle
from fhirkit.Server import AbstractFHIRServer, ResourceNotFoundError
from fhirkit.TerminologyServer import AbstractFHIRTerminologyServer
from fhirkit.Resource import Resource, ResourceWithMultiIdentifier
from fhirkit.parse import AnyPatientResource, parse_json_as_resource
from tqdm import tqdm

LOGGER = logging.getLogger(__name__)
R = TypeVar("R", bound=Resource)


def traverse(
    path: Path, filter_expr: Optional[Callable[[Path], bool]] = None
) -> Generator[Path, None, None]:
    for childPath in path.iterdir():
        if childPath.is_dir():
            if filter_expr:
                yield from [
                    path
                    for path in traverse(childPath, filter_expr)
                    if filter_expr(path)
                ]
            else:
                yield from traverse(childPath)
        else:
            if filter_expr is None or filter_expr(childPath):
                yield childPath


class SimpleFHIRStore(Generic[R], AbstractFHIRTerminologyServer, AbstractFHIRServer):
    """Simple FHIR Server holds a list of resources in memory. It can be initialised based on bulk export directory."""

    def __init__(
        self,
        resources: Sequence[R] = [],
        base_url: Optional[Union[str, HttpUrl]] = None,
    ) -> None:
        self._resources = list(resources)
        super().__init__(base_url)

    def iter(self):
        """Dummy method because we can't expect all child classes to be iterable."""
        yield from self._resources

    def __iter__(self):
        return self.iter()

    def __len__(self):
        return len(self._resources)

    def get_resource_by_canonical(self, reference: Union[canonical, str]) -> "Resource":
        reference = parse_obj_as(canonical, reference)
        version = reference.version
        uri = reference.uri
        for r in self._resources:
            # skip resources that don't have url field or url doesn't match

            # AVR 20221025 hasattr and getattr is not a good practice, we should use structural typing with
            # a CanonicalResource as defined in https://build.fhir.org/canonicalresource.html and
            # use runtime typechecking with a CanonicaResource protocol
            if not hasattr(r, "url") or getattr(r, "url") != uri:
                continue

            if version is not None:

                # skip resources that don't have a version field or the version doesn't match
                if not hasattr(r, "version") or getattr(r, "version") != version:
                    continue

            return r

        raise ResourceNotFoundError(f"Couldn't resolve canonical reference {reference}")

    def get_resource_by_id(
        self, resourceId: str, resourceType: Optional[str] = None
    ) -> "Resource":
        for r in self._resources:
            if r.resourceType == resourceType and r.id == resourceId:
                return r
        raise ResourceNotFoundError(
            f"Couldn't find a {resourceType} resource with id={resourceId}"
        )

    def get_resource_by_literal(
        self, reference: Union[literal, str], resourceType: Optional[str] = None
    ) -> "Resource":
        reference = parse_obj_as(literal, reference)
        if isinstance(reference, AbsoluteURL):
            if self.base_url is not None:
                if reference.host != self.base_url.host:
                    reference_str = reference.build(
                        scheme=reference.scheme,
                        host=reference.host or "",
                    )
                    raise ResourceNotFoundError(
                        f"Can't resolve a resource with different base url. Expected {self.base_url} but received {reference_str}"
                    )
                    return

        if isinstance(reference, RelativeURL):
            return self.get_resource_by_id(
                reference.resourceId, resourceType=reference.resourceType
            )

        if isinstance(reference, URN):
            return self.get_resource_by_id(reference, resourceType=resourceType)

        raise ResourceNotFoundError(
            f"Couldn't resolve resource given literal uri: {reference}"
        )

    def get_resource_by_identifier(
        self, resourceType: str, identifier: "Identifier"
    ) -> "Resource":
        for r in self._resources:
            if r.resourceType != resourceType:
                continue

            if isinstance(r, ResourceWithMultiIdentifier):
                for r_identifier in r.identifier:
                    if r_identifier == identifier and r.resourceType == resourceType:
                        return r

        raise ResourceNotFoundError(
            f"Couldn't resolver {resourceType} resource with identifier={identifier}"
        )

    def __getitem__(self, key):
        return self.get_resource_by_literal(key)

    def filter(self, expr: Callable[[R], bool]):
        return SimpleFHIRStore(
            [r for r in self.iter() if expr(r)], base_url=self.base_url
        )

    def create_reference(
        self, resource: R, auto_save_in_store: bool = True
    ) -> Reference:
        if auto_save_in_store and resource.id is None:
            self.put_resource(resource)
        assert resource.id is not None, "Resource is not known in this store."
        return Reference(reference=f"{resource.resourceType}/{resource.id}")

    def put_resource(self, resource: R):
        ## TODO charlotte
        ## if resource with matching resource.id exists override
        ## if resource with matching reource.identifier exists raise Error
        literal_id = uuid4().urn
        resource.id = literal_id
        self._resources.append(resource)

    def valueset_expand(self, *args, **kwargs):
        return super().valueset_expand(*args, **kwargs)

    def valueset_validate_code(
        self,
        url: URI,
        code: Optional[Code] = None,
        display: Optional[str] = None,
        system: Optional[URI] = None,
        coding: Optional[Coding] = None,
        codeableConcept: Optional[CodeableConcept] = None,
    ) -> bool:
        return super().valueset_validate_code(
            url, code, display, system, coding, codeableConcept
        )

    def _repr_html_(self):
        return (
            """
        <div>
            <style scoped>
                .dataframe tbody tr th:only-of-type {
                    vertical-align: middle;
                }

                .dataframe tbody tr th {
                    vertical-align: top;
                }

                .dataframe thead th {
                    text-align: right;
                }
            </style>
            <table border="1" class="dataframe">
                <thead>
                    <tr style="text-align: right;">
                    <th></th>
                    <th>resourceType</th>
                    <th>id</th>
                    </tr>
                </thead>
            <tbody>
            """
            + "".join(
                [
                    f"<tr><th>{i}</th><td>{r.resourceType}</td><td>{r.id}</td></tr>"
                    for i, r in enumerate(self._resources[:10])
                ]
            )
            + "<tr><th>...</th><td>...</td><td>...</td></tr>"
            if len(self) > 10
            else ""
            + """
                </tbody>
                </table>
                <p>%d resources</p>
                </div>
                """
            % len(self)
        )

    @classmethod
    def bulk_import(cls, path: Path):
        """Load resources from a directory containing NDJSON files with FHIR resources as if they are exported from the FHIR Bulk export API."""
        resources = []
        if isinstance(path, str):
            path = Path(path)
        target_paths = list(traverse(path, lambda p: p.suffix == ".ndjson"))
        for fpath in tqdm(target_paths):
            for i, line in tqdm(
                enumerate(open(fpath, "r")), desc=str(path), leave=True
            ):
                try:
                    resources.append(parse_json_as_resource(line))
                except ValidationError:
                    LOGGER.warning(
                        "Couldn't parse line %d from '%s'",
                        i,
                        str(fpath.absolute()),
                        exc_info=True,
                    )
        return cls(resources)

    @classmethod
    def load_bundles(cls, path: Path, fail_when_invalid: bool = False):
        """Load resources from a directory containing JSON files with FHIR Bundle resources per Patients."""
        resources: List[R] = []
        if isinstance(path, str):
            path = Path(path)
        target_paths = list(traverse(path, lambda p: p.suffix == ".json"))
        for fpath in tqdm(target_paths):
            bundle: Bundle = parse_file_as(Bundle, fpath)
            for i, entry in tqdm(enumerate(bundle.entry), desc=str(fpath), leave=True):
                if entry.resource is None:
                    LOGGER.warning(
                        "Entry %d in Bundle with path %s has no resoruce.",
                        i,
                        str(fpath.absolute()),
                    )
                    continue
                try:
                    resources.append(
                        parse_obj_as(AnyPatientResource, entry.resource.dict())
                    )
                except ValidationError:
                    LOGGER.warning(
                        "Couldn't load entry %d (fullURL='%s') from '%s'",
                        i,
                        entry.fullUrl,
                        str(fpath.absolute()),
                        exc_info=True,
                    )
                    if fail_when_invalid:
                        raise StopIteration("Invalid resource.")
        return cls(resources)
