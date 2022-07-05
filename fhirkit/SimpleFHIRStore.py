import logging
from pathlib import Path
from typing import Callable, Generator, Generic, Optional, Sequence, TypeVar, Union

from pydantic import HttpUrl, ValidationError, parse_file_as, parse_obj_as
from fhirkit.Bundle import Bundle
from fhirkit.Server import AbstractFHIRServer, ResourceNoteFoundError
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


class SimpleFHIRStore(Generic[R], AbstractFHIRServer):
    """Simple FHIR Server holds a list of resources in memory. It can be initialised based on bulk export directory."""

    def __init__(
        self, resources: Sequence[R], base_url: Optional[Union[str, HttpUrl]] = None
    ) -> None:
        self._resources = resources
        super().__init__()

    def __iter__(self):
        yield from self._resources

    def __len__(self):
        return len(self._resources)

    def filter(self, expr: Callable[[R], bool]):
        return self.__class__([r for r in self if expr(r)], base_url=self.base_url)

    def get_resource(
        self,
        resourceType: str,
        *,
        id: Optional[str] = None,
        url: Optional[Union[str, HttpUrl]] = None,
    ):
        if url is None and self.base_url is not None:
            if id is None:
                raise RuntimeError(
                    "At least resource.id or resource.url must be given to be able to identify the requested resource"
                )
            url = self.base_url + "/"
            url += resourceType + "/" + id
        assert self._resources is not None
        for r in self._resources:
            if (r.resourceType == resourceType or resourceType is None) and r.id == id:
                return r
        t = resourceType or "Resource"
        raise ResourceNoteFoundError(f"{t} with id={id} not found.")

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
