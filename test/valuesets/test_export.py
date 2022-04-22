from fhirkit import Observation, SCTConcept
from datetime import datetime


def test_to_record():
    obs = Observation(
        code=SCTConcept("372278000 |Gleason score|"),
        value=SCTConcept("18430005 |Gleason grade score 4|"),
        effective=datetime(2018, 4, 28),
        component=[
            dict(
                code=SCTConcept("384994009 |Primary Gleason pattern|"),
                value=SCTConcept("369771005 |Gleason Pattern 2|"),
            ),
            dict(
                code=SCTConcept("384995005 |Secondary Gleason pattern|"),
                value=SCTConcept("369771005 |Gleason Pattern 2|"),
            ),
        ],
    )
    record = obs.record()
    assert ("code",) in record
    assert ("value",) in record
    assert ("component", 0, "code") in record
    assert ("component", 1, "value") in record


def test_to_dict_from_choice_type():
    obs = Observation(
        code=SCTConcept("372278000 |Gleason score|"),
        valueCodeableConcept=SCTConcept("18430005 |Gleason grade score 4|"),
        effectiveDateTime=datetime(2018, 4, 28),
        component=[
            dict(
                code=SCTConcept("384994009 |Primary Gleason pattern|"),
                valueCodeableConcept=SCTConcept("369771005 |Gleason Pattern 2|"),
            ),
            dict(
                code=SCTConcept("384995005 |Secondary Gleason pattern|"),
                valueCodeableConcept=SCTConcept("369771005 |Gleason Pattern 2|"),
            ),
        ],
    )
    record = obs.dict()
    assert "code" in record
    assert "effective" not in record
    assert "effectiveDateTime" in record
    assert "value" not in record
    assert "valueCodeableConcept" in record
    assert "component" in record
    assert len(record["component"]) == 2
    assert "valueCodeableConcept" in record["component"][0]
    assert "valueCodeableConcept" in record["component"][1]


def test_to_dict_from_poly_type():
    obs = Observation(
        code=SCTConcept("372278000 |Gleason score|"),
        value=SCTConcept("18430005 |Gleason grade score 4|"),
        effective=datetime(2018, 4, 28),
        component=[
            dict(
                code=SCTConcept("384994009 |Primary Gleason pattern|"),
                value=SCTConcept("369771005 |Gleason Pattern 2|"),
            ),
            dict(
                code=SCTConcept("384995005 |Secondary Gleason pattern|"),
                value=SCTConcept("369771005 |Gleason Pattern 2|"),
            ),
        ],
    )
    record = obs.dict()
    assert "code" in record
    assert "effective" not in record
    assert "effectiveDateTime" in record
    assert "value" not in record
    assert "valueCodeableConcept" in record
    assert "component" in record
    assert len(record["component"]) == 2
    assert "valueCodeableConcept" in record["component"][0]
    assert "valueCodeableConcept" in record["component"][1]
