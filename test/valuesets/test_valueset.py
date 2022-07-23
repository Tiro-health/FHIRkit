import pytest_check as check
from fhirkit import ValueSet, SCTCoding, SimpleValueSet, CodeableConcept


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


def test_valueset_usage_context():
    vs_therapeutic_procedures = ValueSet.parse_file(
        "./test/valuesets/therapeutic-procedure.json"
    )
    check.equal(len(vs_therapeutic_procedures.useContext), 4)
    for usage_context in vs_therapeutic_procedures.useContext:
        check.is_not_none(usage_context.value)


def test_valueset_iterator():
    vs_therapeutic_procedures = ValueSet.parse_file(
        "./test/valuesets/therapeutic-procedure.json"
    )

    codes = [c for c in vs_therapeutic_procedures]
    assert len(codes) == vs_therapeutic_procedures.expansion.total
    assert len(codes) == len(vs_therapeutic_procedures)


def test_valueset_contains():
    vs_therapeutic_procedures = SimpleValueSet.parse_file(
        "./test/valuesets/therapeutic-procedure.json"
    )

    cytokinetherapie = SCTCoding("84501003 | cytokinetherapie |")

    assert cytokinetherapie in vs_therapeutic_procedures


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
