from datetime import datetime
from re import U
from tiro_fhir import CodeableConcept, Coding
from tiro_fhir import SCTCoding, SCTFHIRTerminologyServer
from tiro_fhir import SimpleValueSet, ValueSet
from tiro_fhir import Observation
from tiro_fhir.snomed.elements import SCTConcept


def test_valueset_iterator():
    vs_therapeutic_procedures = ValueSet.parse_file(
        "./test/valuesets/therapeutic-procedure.json"
    )

    codes = [c for c in vs_therapeutic_procedures]
    assert len(codes) == vs_therapeutic_procedures.expansion.total
    assert len(codes) == len(vs_therapeutic_procedures)


def test_valueset_contains():
    vs_therapeutic_procedures = ValueSet.parse_file(
        "./test/valuesets/therapeutic-procedure.json"
    )

    cytokinetherapie = SCTCoding("84501003 | cytokinetherapie |")

    assert cytokinetherapie in vs_therapeutic_procedures


def test_descendant_of():
    radical_prostatectomy = SCTCoding("26294005 |Radical prostatectomy (procedure)|")
    vs_rad_prod = radical_prostatectomy.descendants()

    ralp = SCTCoding(
        "708919000 |Laparoscopic radical prostatectomy using robotic assistance (procedure)|"
    )
    assert ralp in vs_rad_prod


def test_append_to_valueset():
    vs_therapeutic_procedures = ValueSet.parse_file(
        "./test/valuesets/therapeutic-procedure.json"
    )
    coding = Coding(code="this-is-a-test", system="http://example.com")

    vs_therapeutic_procedures.append(coding)

    assert coding in vs_therapeutic_procedures


def test_simple_valuesets():
    vs = SimpleValueSet(
        SCTCoding("6142004 |influenza (aandoening)|"),
        SCTCoding("442438000 |influenza A (aandoening)|"),
        SCTCoding("24662006 |influenza B (aandoening)|"),
    )
    assert SCTCoding("6142004 |influenza (aandoening)|") in vs
    assert SCTCoding("442438000 |influenza A (aandoening)|") in vs
    assert SCTCoding("24662006 |influenza B (aandoening)|") in vs
    assert len(vs) == 3


def test_simple_valuesets_contains():
    vs = SimpleValueSet(
        SCTCoding("6142004 |influenza (aandoening)|"),
        SCTCoding("442438000 |influenza A (aandoening)|"),
        SCTCoding("24662006 |influenza B (aandoening)|"),
    )
    cc = CodeableConcept(
        text="griep",
        coding=[
            SCTCoding("6142004 |influenza (aandoening)|"),
            SCTCoding("24662006 |influenza B (aandoening)|"),
        ],
    )

    assert cc in vs


def test_simple_valuesets_contains_2():
    vs = SimpleValueSet(
        SCTCoding("24662006 |influenza B (aandoening)|"),
    )
    cc = CodeableConcept(
        text="griep",
        coding=[
            SCTCoding("442438000 |influenza A (aandoening)|"),
            SCTCoding("24662006 |influenza B (aandoening)|"),
        ],
    )

    assert cc in vs


def test_equality_codeable_concepts_and_coding():

    cc = CodeableConcept(
        text="griep",
        coding=[
            SCTCoding("6142004 |influenza (aandoening)|"),
            SCTCoding("24662006 |influenza B (aandoening)|"),
        ],
    )
    c = SCTCoding("24662006 |influenza B (aandoening)|")

    assert cc == c

    assert not c == cc


def test_equality_codeable_concepts():
    cc1 = CodeableConcept(
        text="griep",
        coding=[
            SCTCoding("6142004 |influenza (aandoening)|"),
            SCTCoding("24662006 |influenza B (aandoening)|"),
        ],
    )

    cc2 = CodeableConcept(
        text="griep",
        coding=[
            SCTCoding("6142004 |influenza (aandoening)|"),
            SCTCoding("442438000 |influenza A (aandoening)|"),
        ],
    )

    assert cc1 == cc2


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
    record = obs.to_record()
    assert "code" in record
    assert "value" in record
    assert ("component", 0, "code") in record
    assert ("component", 1, "value") in record
