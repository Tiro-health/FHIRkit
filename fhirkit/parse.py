from typing import Union


try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

from pydantic import Field, parse_obj_as
from fhirkit import (
    Observation,
    Procedure,
    Condition,
    Immunization,
    DiagnosticReport,
    DocumentReference,
    MedicationAdministration,
    Medication,
    MedicationRequest,
    Encounter,
    CarePlan,
    CareTeam,
    Practitioner,
    Provenance,
    Organization,
    AllergyIntolerance,
    Location,
    PractitionerRole,
    ImagingStudy,
    Patient,
    Device,
    MedicationStatement,
    SupplyDelivery,
)

AnyPatientResource = Annotated[
    Union[
        Observation,
        Procedure,
        Condition,
        Immunization,
        DiagnosticReport,
        DocumentReference,
        MedicationRequest,
        Encounter,
        CarePlan,
        CareTeam,
        Practitioner,
        Organization,
        AllergyIntolerance,
        Location,
        ImagingStudy,
        PractitionerRole,
        Patient,
        MedicationStatement,
        MedicationAdministration,
        Medication,
        Device,
        Provenance,
        SupplyDelivery,
    ],
    Field(discriminator="resourceType"),
]


def parse_json_as_resource(json: str):
    return parse_obj_as(AnyPatientResource, json)
