from __future__ import annotations
import logging
from time import time
from typing import ClassVar, List, Optional, Union
import requests
from pydantic import HttpUrl, ValidationError, parse_obj_as
from tiro_fhir.Parameter import Parameters
from tiro_fhir.Server import AbstractFHIRTerminologyServer
from tiro_fhir.data_types import Code
from tiro_fhir.elements import CodeableConcept, Coding
from tiro_fhir.OperationOutcome import OperationOutcome, OperationOutcomeException

# DEFAULT_SCT_URL = "https://browser.ihtsdotools.org/snowstorm/snomed-ct/fhir"
DEFAULT_SCT_URL = "https://r4.ontoserver.csiro.au/fhir"
# DEFAULT_SCT_URL = "https://snowstorm-aovarw23xa-uc.a.run.app/fhir"

Response = Union[Parameters, OperationOutcome]


class SCTFHIRTerminologyServer(AbstractFHIRTerminologyServer):
    DEFAULT_URL: ClassVar[str] = "https://r4.ontoserver.csiro.au/fhir"
    DEFAULT_SERVER: ClassVar[Optional[SCTFHIRTerminologyServer]] = None

    def __init__(self, baseUrl: Optional[Union[str, HttpUrl]] = None) -> None:
        baseUrl = baseUrl or self.DEFAULT_URL
        self.baseUrl = parse_obj_as(HttpUrl, baseUrl)

    @classmethod
    def default_server(cls):
        if cls.DEFAULT_SERVER is None:
            cls.DEFAULT_SERVER = SCTFHIRTerminologyServer()
        return cls.DEFAULT_SERVER

    def get_resource(
        self, resourceType: str, *, id: Optional[str] = None, url: Optional[str] = None
    ):
        path = resourceType
        if id:
            path += "/" + id
        req_url = f"{self.baseUrl}/{path}"
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
            response = raw_response.json()
            response = parse_obj_as(Response, raw_response.json())
        except ValidationError:
            raise ConnectionError(
                f"Received a response that doesn't resemble a FHIR-server. Please check if the server at {self.baseUrl} is a valid FHIR-server"
            )
        except:
            raise RuntimeWarning(
                "Failed when calling {endpoint} on {baseurl}".format(
                    endpoint=path, baseurl=self.baseUrl
                )
            )

        if isinstance(response, OperationOutcome):
            raise OperationOutcomeException(response)

        return response

    def valueset_expand(self, url: Union[str, HttpUrl], **kwargs):
        path = "ValueSet/$expand"
        page_size = 200
        offset = 0

        query = "url={url}&count={count}&offset={offset}".format(
            url=url, count=page_size, offset=offset
        )
        more_results_available = True
        oper_outcome_count = 0

        while more_results_available:
            req_url = f"{self.baseUrl}/{path}?{query}"
            headers = {
                "Accept": "application/json",
            }
            payload = ""
            try:

                # TODO parse this as FHIR Resource!
                raw_response = requests.request(
                    "GET", req_url, data=payload, headers=headers
                )
                if raw_response.status_code != 200:
                    logging.warn(
                        "Received an error from the snowstorm server (%s) after sending the following request %s",
                        raw_response.text,
                        req_url,
                    )
                response = raw_response.json()
                assert (
                    "resourceType" in response
                ), "Expected a valid FHIR-resource but received " + str(response)
                resourceType = response["resourceType"]

                # first check if the server responded with a OperationOutcome to report issues
                if response["resourceType"] == "OperationOutcome":
                    raise ResourceWarning(
                        "Snowstorm reported some resource issues.",
                        *response["issue"][0].values(),
                    )

                assert (
                    response["resourceType"] == "ValueSet"
                ), f"Expected 'ValueSet' Resource but received {resourceType}"
                if "expansion" in response and "contains" in response["expansion"]:

                    yield from parse_obj_as(
                        List[Coding], response["expansion"]["contains"]
                    )
                    remaining = max(
                        response["expansion"]["total"]
                        - response["expansion"]["offset"]
                        - page_size,
                        0,
                    )
                else:
                    raise RuntimeError(
                        f"No expansion or empty expansion in response ValueSet for request: {req_url} \n"
                        + str(response)
                    )
            except ResourceWarning:
                if oper_outcome_count >= 3:
                    raise
                logging.info(
                    "Received an OperationOutcome. Waiting 15 seconds for the server to catchup."
                )
                time.sleep(15)
                oper_outcome_count += 1

            except Exception:
                logging.warn(
                    "Something went wrong when resolving a ECL query. Request: %s",
                    req_url,
                )
                raise
            else:

                if remaining % (page_size * 10) == 0:
                    logging.debug(
                        f"{remaining} concepts remaining (total: {response['expansion']['total']} | page size: {page_size})."
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

        req_url = f"{self.baseUrl}/{path}"
        headersList = {"Accept": "application/json", "Content-type": "application/json"}
        payload = Parameters(parameter=parameters).json(exclude_none=True)
        try:

            # TODO parse this as FHIR Resource!
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
                f"Received a response that doesn't resemble a FHIR-server. Please check if the server at {self.baseUrl} is a valid FHIR-server"
            )
        except:
            raise RuntimeWarning(
                "Failed when calling {endpoint} on {baseurl}".format(
                    endpoint=path, baseurl=self.baseUrl
                )
            )

        if isinstance(response, OperationOutcome):
            raise OperationOutcomeException(response)

        return response


DEFAULT_TERMINOLOGY_SERVER = SCTFHIRTerminologyServer()
