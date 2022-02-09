from __future__ import annotations
import logging
from time import time
from typing import List, Literal, Optional, Tuple, Union
import requests
from pydantic import Field, HttpUrl, parse_obj_as
from tiro_fhir.Server import AbstractFHIRServer 
from tiro_fhir.ValueSet import (
    VSCompose,
    VSExpansion,
    VSFilter,
    VSInclude,
    ValueSet,
)
from tiro_fhir.CodeSystem import Coding

class SCTDescendantsFilter(VSFilter):
    property: Literal["concept"]
    op: Literal["is-a"]
    value: str
class SCTImplicitInclude(VSInclude):
    concept:List = []
    valueSetList = []
    filter: Tuple[SCTDescendantsFilter]

class SCTImplicitCompose(VSCompose):
    include: Tuple[SCTImplicitInclude]

class SCTImplicitValueSet(ValueSet):
    url: HttpUrl
    compose: SCTImplicitCompose

    def expand(self):
        if self.fhir_server:
            expansion = VSExpansion(contains=[])
            for code in self.fhir_server.expand_value_set(self):
                expansion.contains.append(code)
            self.expansion = expansion
        else:
            raise RuntimeWarning(
                "Can't expand an implicit SNOMED-CT without a FHIR server."
            )

class SCTDescendantsFilter(VSFilter):
    property: Literal["concept"]
    op: Literal["is-a"]
    value: str


class SCTCoding(Coding):
    system: HttpUrl = Field(default="http://snomed.info/sct")

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], str):
            code, display, *_ = (x.strip() for x in args[0].split("|")) # break string in pieces
            super().__init__(code=code, display=display)
        else:
            super().__init__(*args, **kwargs) # business as usual, Pydantic takes over

    def descendants(self, fhir_server:Optional[AbstractFHIRServer] = None) -> ValueSet:
        return SCTImplicitValueSet(
            url=f"{self.system}?fhir_vs=isa/{self.code}",
            compose=SCTImplicitCompose(
                include=[
                    SCTImplicitInclude(
                        system=self.system,
                        filter=[SCTDescendantsFilter(property="concept", op="is-a", value=self.code)],
                    )
                ]
            ),
            fhir_server=fhir_server
        )


class SCTFHIRTerminologyServer(AbstractFHIRServer):
    def __init__(self, baseUrl: Union[str, HttpUrl]) -> None:
        self.baseUrl = parse_obj_as(HttpUrl,baseUrl)

    def expand_value_set(self, implicit_vs: SCTImplicitValueSet, **kwargs):
        assert (
            implicit_vs.url is not None
        ), f"Can't expand an implicit ValueSet without URL. Received {implicit_vs}"
        path = "ValueSet/$expand"
        page_size = 200
        offset = 0
 
        query = "url={url}&count={count}&offset={offset}".format(url=implicit_vs.url, count=page_size, offset=offset)
        more_results_available = True
        oper_outcome_count = 0

        while more_results_available:
            req_url = f"{self.baseUrl}/{path}?{query}"
            headersList = {
                "Accept": "application/json",
            }
            payload = ""
            try:

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

                    yield from parse_obj_as(List[Coding], response["expansion"]["contains"])
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
