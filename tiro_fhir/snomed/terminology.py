from __future__ import annotations
import logging
from time import time
from typing import List, Optional, Union
import requests
from pydantic import HttpUrl, parse_obj_as
from tiro_fhir.Parameter import Parameter
from tiro_fhir.Server import AbstractFHIRServer
from tiro_fhir.data_types import Code
from tiro_fhir.snomed.ValueSet import SCTImplicitValueSet
from tiro_fhir.elements import AbstractCoding, CodeableConcept, Coding


class SCTFHIRTerminologyServer(AbstractFHIRServer):
    def __init__(self, baseUrl: Union[str, HttpUrl]) -> None:
        self.baseUrl = parse_obj_as(HttpUrl, baseUrl)

    def expand_value_set(self, implicit_vs: SCTImplicitValueSet, **kwargs):
        assert (
            implicit_vs.url is not None
        ), f"Can't expand an implicit ValueSet without URL. Received {implicit_vs}"
        path = "ValueSet/$expand"
        page_size = 200
        offset = 0

        query = "url={url}&count={count}&offset={offset}".format(
            url=implicit_vs.url, count=page_size, offset=offset
        )
        more_results_available = True
        oper_outcome_count = 0

        while more_results_available:
            req_url = f"{self.baseUrl}/{path}?{query}"
            headersList = {
                "Accept": "application/json",
            }
            payload = ""
            try:

                # TODO parse this as FHIR Resource!
                raw_response = requests.request(
                    "GET", req_url, data=payload, headers=headersList
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
                        **response["issue"][0].values(),
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

    def validate_code_in_valueset(
        self,
        implicit_vs: Union[SCTImplicitValueSet, HttpUrl],
        code: Optional[Code] = None,
        display: Optional[str] = None,
        system: Optional[HttpUrl] = None,
        coding: Optional[AbstractCoding] = None,
        codeableConcept: Optional[CodeableConcept] = None,
    ) -> bool:
        if isinstance(implicit_vs, SCTImplicitValueSet):
            assert (
                implicit_vs.url is not None
            ), f"Can't expand an implicit ValueSet without URL. Received {implicit_vs}"
            implicit_vs = implicit_vs.url

        assert (
            code or coding or codeableConcept
        ), "At least a code, coding or codeableConcept must be given to validate."

        path = "ValueSet/$validate-code"

        parameters = [dict(name="url", valueUri=str(implicit_vs))]

        if code:
            parameters.append(dict(name="code", valueCode=code))
            if system:
                parameters.append(dict(name="system", valueUri=str(system)))
            if display:
                parameters.append(dict(name="display", valueString=display))
        if coding:
            parameters.append(dict(name="coding", valueCoding=coding))
        if codeableConcept:
            parameters.append(
                dict(name="codeableConcept", valueCodeableConcpet=codeableConcept)
            )

        req_url = f"{self.baseUrl}/{path}"
        headersList = {
            "Accept": "application/json",
        }
        payload = Parameter(parameter=parameters).dict()
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
            response = Parameter.parse_obj(raw_response.json())
        except:
            raise RuntimeWarning(
                "Failed when calling {endpoint} on {baseurl}".format(
                    endpoint=path, baseurl=self.baseUrl
                )
            )

        return response.result
