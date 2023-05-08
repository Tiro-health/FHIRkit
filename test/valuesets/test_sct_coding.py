from fhirkit import SCTCoding


def test_descendants_rarp():
    radical_prostatectomy = SCTCoding("26294005 |Radical prostatectomy (procedure)|")
    vs_rad_prod = radical_prostatectomy.descendants()

    ralp = SCTCoding(
        "708919000 |Laparoscopic radical prostatectomy using robotic assistance (procedure)|"
    )
    assert vs_rad_prod.validate(ralp)


def test_descendants_influenza():
    influenza = SCTCoding(code="6142004")
    influenza_b = SCTCoding(code="24662006")
    influenza_a = SCTCoding(code="442438000")

    vs_influenza = influenza.descendants()

    assert (
        influenza_a in vs_influenza
    ), "Influenza A must be part of the Influenza descendants."
    assert (
        influenza_b in vs_influenza
    ), "Influenza B must be part of the Influenza descendants."
