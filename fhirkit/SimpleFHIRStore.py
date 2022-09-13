import logging
from pathlib import Path
from typing import Callable, Generator, Generic, Optional, Sequence, TypeVar, Union

from pydantic import HttpUrl, ValidationError, parse_file_as, parse_obj_as
from fhirkit.elements.elements import CodeableConcept, Coding
from fhirkit.primitive_datatypes import URI, Code
from fhirkit.Bundle import Bundle
from fhirkit.Server import AbstractFHIRServer, ResourceNotFoundError
from fhirkit.TerminologyServer import AbstractFHIRTerminologyServer
from fhirkit.Resource import Resource
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
        self, resources: Sequence[R], base_url: Optional[Union[str, HttpUrl]] = None
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

    def filter(self, expr: Callable[[R], bool]):
        return SimpleFHIRStore(
            [r for r in self.iter() if expr(r)], base_url=self.base_url
        )

    def get_resource(
        self,
        resourceType: Optional[str],
        *,
        id: Optional[str] = None,
        url: Optional[str] = None,
    ):
        if url is not None and self.base_url is not None:
            assert url.startswith(self.base_url), (
                "Can't resolve a resource that is not managed by this server (base URL=%s)"
                % self.base_url,
                url,
            )
            *_, resourceType, id = url.split("/")
        if id is not None:
            assert self._resources is not None
            for r in self._resources:
                if (
                    r.resourceType == resourceType or resourceType is None
                ) and r.id == id:
                    return r
        if id is None and url is None:
            raise RuntimeError(
                "At least an id or url must be given to be able to identify the requested resource"
            )
        t = resourceType or "Resource"
        raise ResourceNotFoundError(f"{t} with id={id} not found.")

    def get_terminology_resource(
        self,
        resourceType: Optional[str],
        *,
        id: Optional[str] = None,
        url: Optional[URI] = None,
    ):

        # ValueSets and CodeSystems have a url that identifies them
        assert (
            resourceType in ("ValueSet", "CodeSystem", "ConceptMap")
            or resourceType is None
        ), "ResourceType should be either %s or %s " % (
            "ValueSet",
            "CodeSystem",
            "ConceptMap",
        )
        try:
            for resource in self._resources:
                if (
                    resource.resourceType in ("ValueSet", "CodeSystem", "ConceptMap"),
                    resource.url == url
                    and url is not None
                    and (resourceType is None or resource.resourceType == resourceType),
                ):
                    return resource
            if id is not None:
                return super().get_resource(resourceType, id=id)
        except ResourceNotFoundError:
            raise
        except Exception:
            LOGGER.warning(
                "Unexpected exception while resolving resource.", exc_info=True
            )
            raise ResourceNotFoundError(
                "Could not resolve resource with resourceType=%s, url=%s, id=%s"
                % (resourceType, url, id)
            )

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
        for fpath in traverse(path, lambda p: p.suffix == ".ndjson"):
            for i, line in enumerate(open(fpath, "r")):
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
    def load_bundles(cls, path: Path):
        """Load resources from a directory containing JSON files with FHIR Bundle resources per Patients."""
        resources = []
        if isinstance(path, str):
            path = Path(path)
        for fpath in traverse(path, lambda p: p.suffix == ".json"):
            bundle: Bundle = parse_file_as(Bundle, fpath)
            for i, entry in tqdm(enumerate(bundle.entry), desc=str(fpath)):
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
        return cls(resources)
