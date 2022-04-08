from tiro_fhir.snomed.ValueSet import SCTImplicitValueSet
from tiro_fhir.snomed.terminology import SCTFHIRTerminologyServer


def test_change_default_url():
    SCTFHIRTerminologyServer.DEFAULT_URL = (
        "https://snowstorm-aovarw23xa-uc.a.run.app/fhir"
    )
    sct_server = SCTFHIRTerminologyServer()
    assert sct_server.baseUrl == "https://snowstorm-aovarw23xa-uc.a.run.app/fhir"


def test_subsumption():
    SCTFHIRTerminologyServer.DEFAULT_URL = (
        "https://snowstorm-aovarw23xa-uc.a.run.app/fhir"
    )
    sct_server = SCTFHIRTerminologyServer()
    system = "http://snomed.info/sct"
    code = "5880005"

    response = sct_server.valueset_validate_code(
        f"{system}?fhir_vs=isa/{code}", code="66456009", system=system
    )
    assert (
        response.result
    ), "66456009 should be a childe of 5880005 | Physical Examination |"


def test_implicit_valueset_expansion():
    vs = SCTImplicitValueSet(url="http://snomed.info/sct?fhir_vs=isa/6142004")
    vs.expand()
    print(list(vs))
