from __future__ import annotations
import logging
from urllib.parse import urlencode

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
from pydantic import Field

from typing import ClassVar, Optional, Union

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

import requests
from pydantic import Field, HttpUrl, ValidationError, parse_obj_as
from fhirkit.Parameter import Parameters
from fhirkit.TerminologyServer import AbstractFHIRTerminologyServer
from fhirkit.ValueSet import VSExpansion, ValueSet
from fhirkit.primitive_datatypes import URI, Code
from fhirkit.elements import CodeableConcept, Coding
from fhirkit.OperationOutcome import OperationOutcome, OperationOutcomeException


class ExpandedValueset(ValueSet):
    status: Literal["active"] = Field("active")
    expansion: VSExpansion


Response = Annotated[
    Union[Parameters, OperationOutcome], Field(discriminator="resourceType")
]
VSExpansionResponse = Annotated[
    Union[ExpandedValueset, OperationOutcome], Field(discriminator="resourceType")
]


class SCTFHIRTerminologyServer(AbstractFHIRTerminologyServer):
    DEFAULT_URL: ClassVar[
        str
    ] = "https://browser.ihtsdotools.org/snowstorm/snomed-ct/fhir"
    DEFAULT_SERVER: ClassVar[Optional[SCTFHIRTerminologyServer]] = None
    RETRY_COUNT: int = 3
    RETRY_PAUSE: int = 10

    def __init__(self, base_url: Optional[Union[str, HttpUrl]] = None) -> None:
        base_url = base_url or self.DEFAULT_URL
        self._base_url = parse_obj_as(HttpUrl, base_url)

    @classmethod
    def default_server(cls):
        if cls.DEFAULT_SERVER is None:
            cls.DEFAULT_SERVER = SCTFHIRTerminologyServer()
        return cls.DEFAULT_SERVER

    def get_terminology_resource(
        self,
        resourceType: Optional[str],
        *,
        id: Optional[str] = None,
        url: Optional[URI] = None,
    ):
        return super().get_terminology_resource(resourceType, id=id, url=url)

    def get_resource(
        self, resourceType: str, *, id: Optional[str] = None, url: Optional[str] = None
    ):
        path = resourceType
        if id:
            path += "/" + id
        req_url = f"{self.base_url}/{path}"
        if url:
            req_url = url
        headers = {"Accept": "application/json", "Content-type": "application/json"}
        try:
            raw_response = requests.get(req_url, headers=headers)

            if raw_response.status_code != 200:
                logging.warn(
                    "Received an error from the snowstorm server (%s) after sending the following request %s",
                    raw_response.text,
                    req_url,
                )
            response = parse_obj_as(Response, raw_response.json())
        except ValidationError:
            raise ConnectionError(
                f"Received a response that doesn't resemble a FHIR-resource. Please check if the server at {self.base_url} is a valid FHIR-server"
            )
        except:
            raise RuntimeWarning(
                "Failed when calling {endpoint} on {base_url}".format(
                    endpoint=path, base_url=self.base_url
                )
            )

        if isinstance(response, OperationOutcome):
            raise OperationOutcomeException(response)

        return response

    def valueset_expand(self, url: Union[str, HttpUrl], **kwargs):
        path = "ValueSet/$expand"
        page_size = 200
        offset = 0

        more_results_available = True

        while more_results_available:
            query = "url={url}&count={count}&offset={offset}".format(
                url=url, count=page_size, offset=offset
            )
            query += "&" + urlencode(kwargs) if kwargs else ""
            req_url = f"{self.base_url}/{path}?{query}"
            headers = {
                "Accept": "application/json",
            }
            payload = ""

            try:

                raw_response = requests.request(
                    "GET", req_url, data=payload, headers=headers
                )

                if raw_response.status_code != 200:
                    logging.warn(
                        "Received an error from the snowstorm server (%s) after sending the following request %s",
                        raw_response.text,
                        req_url,
                    )
                response = parse_obj_as(VSExpansionResponse, raw_response.json())

                if isinstance(response, OperationOutcome):
                    raise OperationOutcomeException(response)

                yield response

                offset = response.expansion.offset + page_size
                remaining = max(response.expansion.total - offset, 0)

            except ValidationError:
                raise ConnectionError(
                    f"Received a response that doesn't resemble a FHIR-server. Please check if the server at {self.base_url} is a valid FHIR-server. \n Response:\n\n {raw_response.json()}"
                )
            except:
                raise
                raise RuntimeWarning(
                    "Failed when calling {endpoint} on {base_url}".format(
                        endpoint=path, base_url=self.base_url
                    )
                )
            else:

                if remaining % (page_size * 10) == 0:
                    logging.debug(
                        f"{remaining} concepts remaining (total: {response.expansion.total} | page size: {page_size})."
                    )
                more_results_available = remaining > 0

    def valueset_validate_code(
        self,
        url: Union[str, HttpUrl],
        code: Optional[Code] = None,
        display: Optional[str] = None,
        system: Optional[HttpUrl] = None,
        coding: Optional[Coding] = None,
        codeableConcept: Optional[CodeableConcept] = None,
    ) -> bool:
        assert (
            code or coding or codeableConcept
        ), "At least a code, coding or codeableConcept must be given to validate."

        path = "ValueSet/$validate-code"

        parameters = [dict(name="url", valueUri=str(url))]

        if code and system:
            parameters.append(dict(name="code", valueCode=code))
            parameters.append(dict(name="system", valueUri=str(system)))
            if display:
                parameters.append(dict(name="display", valueString=display))
        if coding:
            parameters.append(dict(name="coding", valueCoding=coding))
        if codeableConcept:
            parameters.append(
                dict(name="codeableConcept", valueCodeableConcept=codeableConcept)
            )

        req_url = f"{self.base_url}/{path}"
        headersList = {"Accept": "application/json", "Content-type": "application/json"}
        payload = Parameters(parameter=parameters).json(exclude_none=True)
        try:

            raw_response = requests.request(
                "POST", req_url, data=payload, headers=headersList
            )
            if raw_response.status_code != 200:
                logging.warn(
                    "Received an error from the snowstorm server (%s) after sending the following request %s",
                    raw_response.text,
                    req_url,
                )
            response = parse_obj_as(Response, raw_response.json())
        except ValidationError:
            raise ConnectionError(
                f"Received a response that doesn't resemble a FHIR-server. Please check if the server at {self.base_url} is a valid FHIR-server"
            )
        except:
            raise RuntimeWarning(
                "Failed when calling {endpoint} on {base_url}".format(
                    endpoint=path, base_url=self.base_url
                )
            )

        if isinstance(response, OperationOutcome):
            raise OperationOutcomeException(response)

        return response


def get_default_terminology_server():
    return SCTFHIRTerminologyServer.default_server()


DEFAULT_TERMINOLOGY_SERVER = SCTFHIRTerminologyServer()
