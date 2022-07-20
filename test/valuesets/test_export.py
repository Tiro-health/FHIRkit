from datetime import datetime
from fhirkit import Observation, SCTConcept
from fhirkit.primitive_datatypes import dateTime
import pytest_check as check


def test_to_record():
    obs = Observation(
        code=SCTConcept("372278000 |Gleason score|"),
        value=SCTConcept("18430005 |Gleason grade score 4|"),
        effective=datetime(2018, 4, 28),
        component=(
            dict(
                code=SCTConcept("384994009 |Primary Gleason pattern|"),
                value=SCTConcept("369771005 |Gleason Pattern 2|"),
            ),
            dict(
                code=SCTConcept("384995005 |Secondary Gleason pattern|"),
                value=SCTConcept("369771005 |Gleason Pattern 2|"),
            ),
        ),
    )
    record = obs.record()
    check.is_in(("code",), record)
    check.is_in(("value",), record)
    check.is_in(("component", 0, "code"), record)
    check.is_in(("component", 1, "value"), record)


def test_from_choice_type_to_choice_type():
    obs = Observation.parse_obj(
        {
            "code": SCTConcept("372278000 |Gleason score|"),
            "valueCodeableConcept": SCTConcept("18430005 |Gleason grade score 4|"),
            "effectiveDateTime": datetime(2018, 4, 28),
            "component": [
                {
                    "code": SCTConcept("384994009 |Primary Gleason pattern|"),
                    "valueCodeableConcept": SCTConcept("369771005 |Gleason Pattern 2|"),
                },
                {
                    "code": SCTConcept("384995005 |Secondary Gleason pattern|"),
                    "valueCodeableConcept": SCTConcept("369771005 |Gleason Pattern 2|"),
                },
            ],
        }
    )
    record = obs.dict(by_alias=True)
    check.is_in("code", record)
    check.is_not_in("effective", record)
    check.is_in("effectiveDateTime", record)
    check.is_not_in("value", record)
    check.is_in("valueCodeableConcept", record)
    check.is_in("component", record)
    check.equal(len(record["component"]), 2)
    check.is_in("valueCodeableConcept", record["component"][0])
    check.is_not_in("value", record["component"][0])
    check.is_in("valueCodeableConcept", record["component"][1])
    check.is_not_in("value", record["component"][1])


def test_from_choice_type_to_python_type():
    obs = Observation.parse_obj(
        {
            "code": SCTConcept("372278000 |Gleason score|"),
            "valueCodeableConcept": SCTConcept("18430005 |Gleason grade score 4|"),
            "effectiveDateTime": datetime(2018, 4, 28),
            "component": [
                {
                    "code": SCTConcept("384994009 |Primary Gleason pattern|"),
                    "valueCodeableConcept": SCTConcept("369771005 |Gleason Pattern 2|"),
                },
                {
                    "code": SCTConcept("384995005 |Secondary Gleason pattern|"),
                    "valueCodeableConcept": SCTConcept("369771005 |Gleason Pattern 2|"),
                },
            ],
        }
    )
    record = obs.dict()
    check.is_in("code", record)
    check.is_in("effective", record)
    check.is_not_in("effectiveDateTime", record)
    check.is_in("value", record)
    check.is_not_in("valueCodeableConcept", record)
    check.is_in("component", record)
    check.equal(len(record["component"]), 2)
    check.is_not_in("valueCodeableConcept", record["component"][0])
    check.is_in("value", record["component"][0])
    check.is_not_in("valueCodeableConcept", record["component"][1])
    check.is_in("value", record["component"][1])


def test_from_python_type_to_python_type():
    obs = Observation.parse_obj(
        {
            "code": SCTConcept("372278000 |Gleason score|").dict(),
            "value": SCTConcept("18430005 |Gleason grade score 4|").dict(),
            "effective": datetime(2018, 4, 28),
            "component": [
                {
                    "code": SCTConcept("384994009 |Primary Gleason pattern|").dict(),
                    "value": SCTConcept("369771005 |Gleason Pattern 2|").dict(),
                },
                {
                    "code": SCTConcept("384995005 |Secondary Gleason pattern|").dict(),
                    "value": SCTConcept("369771005 |Gleason Pattern 2|").dict(),
                },
            ],
        }
    )
    record = obs.dict()
    check.is_in("code", record)
    check.is_in("effective", record)
    check.is_not_in("effectiveDateTime", record)
    check.is_in("value", record)
    check.is_not_in("valueCodeableConcept", record)
    check.is_in("component", record)
    check.equal(len(record["component"]), 2)
    check.is_not_in("valueCodeableConcept", record["component"][0])
    check.is_in("value", record["component"][0])
    check.is_not_in("valueCodeableConcept", record["component"][1])
    check.is_in("value", record["component"][1])


def test_from_python_type_to_choice_type():
    obs = Observation.parse_obj(
        {
            "code": SCTConcept("372278000 |Gleason score|").dict(),
            "value": SCTConcept("18430005 |Gleason grade score 4|").dict(),
            "effective": datetime(2018, 4, 28),
            "component": [
                {
                    "code": SCTConcept("384994009 |Primary Gleason pattern|").dict(),
                    "value": SCTConcept("369771005 |Gleason Pattern 2|").dict(),
                },
                {
                    "code": SCTConcept("384995005 |Secondary Gleason pattern|").dict(),
                    "value": SCTConcept("369771005 |Gleason Pattern 2|").dict(),
                },
            ],
        }
    )
    record = obs.dict(by_alias=True)
    check.is_in("code", record)
    check.is_not_in("effective", record)
    check.is_in("effectiveDateTime", record)
    check.is_not_in("value", record)
    check.is_in("valueCodeableConcept", record)
    check.is_in("component", record)
    check.equal(len(record["component"]), 2)
    check.is_in("valueCodeableConcept", record["component"][0])
    check.is_not_in("value", record["component"][0])
    check.is_in("valueCodeableConcept", record["component"][1])
    check.is_not_in("value", record["component"][1])
