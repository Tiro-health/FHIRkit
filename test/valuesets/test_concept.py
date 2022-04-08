from tiro_fhir import CodeableConcept
from tiro_fhir import SCTCoding


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
