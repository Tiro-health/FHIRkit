from __future__ import annotations
from datetime import datetime, date, time
from pathlib import Path
import re

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

from typing import Optional, Union, no_type_check
from pydantic import ConstrainedStr, AnyUrl, Field


class Id(ConstrainedStr):
    regex = re.compile(r"[A-Za-z0-9\-\.]{1,64}")


class Code(ConstrainedStr):
    regex = re.compile(r"[^\s]+(\s[^\s]+)*")


class Instant(ConstrainedStr):
    regex = re.compile(
        r"([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])T([01][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)(\.[0-9]+)?(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))"
    )


class XHTML(ConstrainedStr):
    pass


class dateTime(datetime):
    pass


class URN(ConstrainedStr):
    # TODO extract nid and nss
    regex = re.compile(r"urn:\S*")


class UUID(ConstrainedStr):
    regex = re.compile(
        r"urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    )


class URI(ConstrainedStr):
    regex = re.compile(r"\S*")


class AbsoluteURL(AnyUrl):
    pass


class RelativeURL(ConstrainedStr):
    regex = re.compile(
        r"(Account|ActivityDefinition|AdministrableProductDefinition|AdverseEvent|AllergyIntolerance|Appointment|AppointmentResponse|AuditEvent|Basic|Binary|BiologicallyDerivedProduct|BodyStructure|Bundle|CapabilityStatement|CarePlan|CareTeam|CatalogEntry|ChargeItem|ChargeItemDefinition|Citation|Claim|ClaimResponse|ClinicalImpression|ClinicalUseDefinition|CodeSystem|Communication|CommunicationRequest|CompartmentDefinition|Composition|ConceptMap|Condition|Consent|Contract|Coverage|CoverageEligibilityRequest|CoverageEligibilityResponse|DetectedIssue|Device|DeviceDefinition|DeviceMetric|DeviceRequest|DeviceUseStatement|DiagnosticReport|DocumentManifest|DocumentReference|Encounter|Endpoint|EnrollmentRequest|EnrollmentResponse|EpisodeOfCare|EventDefinition|Evidence|EvidenceReport|EvidenceVariable|ExampleScenario|ExplanationOfBenefit|FamilyMemberHistory|Flag|Goal|GraphDefinition|Group|GuidanceResponse|HealthcareService|ImagingStudy|Immunization|ImmunizationEvaluation|ImmunizationRecommendation|ImplementationGuide|Ingredient|InsurancePlan|Invoice|Library|Linkage|List|Location|ManufacturedItemDefinition|Measure|MeasureReport|Media|Medication|MedicationAdministration|MedicationDispense|MedicationKnowledge|MedicationRequest|MedicationStatement|MedicinalProductDefinition|MessageDefinition|MessageHeader|MolecularSequence|NamingSystem|NutritionOrder|NutritionProduct|Observation|ObservationDefinition|OperationDefinition|OperationOutcome|Organization|OrganizationAffiliation|PackagedProductDefinition|Patient|PaymentNotice|PaymentReconciliation|Person|PlanDefinition|Practitioner|PractitionerRole|Procedure|Provenance|Questionnaire|QuestionnaireResponse|RegulatedAuthorization|RelatedPerson|RequestGroup|ResearchDefinition|ResearchElementDefinition|ResearchStudy|ResearchSubject|RiskAssessment|Schedule|SearchParameter|ServiceRequest|Slot|Specimen|SpecimenDefinition|StructureDefinition|StructureMap|Subscription|SubscriptionStatus|SubscriptionTopic|Substance|SubstanceDefinition|SupplyDelivery|SupplyRequest|Task|TerminologyCapabilities|TestReport|TestScript|ValueSet|VerificationResult|VisionPrescription)\/[A-Za-z0-9\-\.]{1,64}(\/_history\/[A-Za-z0-9\-\.]{1,64})?"
    )

    @no_type_check
    def __new__(cls, url: ConstrainedStr, **kwargs) -> object:
        return str.__new__(cls, url)

    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate
        yield cls.validate_relative_path

    def __init__(
        self,
        url: ConstrainedStr,
        *,
        resourceType: str,
        resourceId: str,
        version: Optional[str] = None,
    ) -> None:
        ConstrainedStr.__init__(url)
        self.resourceType = resourceType
        self.resourceId = resourceId
        self.version = version

    @classmethod
    def validate_relative_path(cls, v: ConstrainedStr):
        resourceType, *other = v.split("/")
        if len(other) == 1:
            resourceId = other[0]
            version = None
        else:
            resourceId, _, version = other
        return cls(v, resourceType=resourceType, resourceId=resourceId, version=version)


literal = Annotated[Union[AbsoluteURL, RelativeURL, URN], Field()]


class CanonicalURL(AnyUrl):
    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate
        yield cls.validate_version

    def __init__(
        self,
        url: str,
        *,
        scheme: str,
        user: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        tld: Optional[str] = None,
        host_type: str = "domain",
        port: Optional[str] = None,
        path: Optional[str] = None,
        query: Optional[str] = None,
        fragment: Optional[str] = None,
        version: Optional[str] = None,
    ) -> None:
        self.version = version
        super().__init__(
            url,
            scheme=scheme,
            user=user,
            password=password,
            host=host,
            tld=tld,
            host_type=host_type,
            port=port,
            path=path,
            query=query,
            fragment=fragment,
        )

    @classmethod
    def validate_version(cls, v: CanonicalURL):
        # version suffixes are always part of a path
        if v.path is None:
            return v
        # extract the version suffix
        parts = v.path.split("|")
        if len(parts) > 1:
            v.path = parts[0]
            v.version = parts[1]
        return v

    @property
    def uri(self):
        kwargs = dict()
        kwargs["scheme"] = self.scheme
        kwargs["user"] = self.user
        kwargs["password"] = self.password
        if self.host is not None:
            kwargs["host"] = self.host

        kwargs["port"] = self.port
        kwargs["path"] = self.path
        kwargs["query"] = self.query
        kwargs["fragment"] = self.fragment
        return self.build(**kwargs)


class CanonicalURN(URN):
    version = None

    @property
    def uri(self):
        return str(self)

    # TODO extract version


canonical = Annotated[
    Union[CanonicalURL, CanonicalURN],
    Field(
        description="""A reference to a Canonical Resources (resources with `url` element) based on the canonical URL.
    They are absolute URLs or fragment identifiers with optionally a `|` version suffix.

    If no version is specified, the server takes the last version
    Fragments refer to contained resources. More info about the use of fragments: https://www.hl7.org/fhir/references.html#canonical-fragments
    """
    ),
]


class decimal(float):
    pass
