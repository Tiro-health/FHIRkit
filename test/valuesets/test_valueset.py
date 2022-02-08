from tiro_fhir.CodeSystem import Coding
from tiro_fhir.SCT import SCTCoding, SCTFHIRTerminologyServer
from tiro_fhir.ValueSet import ValueSet

def test_valueset_iterator():
    vs_therapeutic_procedures = ValueSet.parse_file("./test/valuesets/therapeutic-procedure.json")

    codes = [c for c in vs_therapeutic_procedures]
    assert len(codes) == vs_therapeutic_procedures.expansion.total 
    assert len(codes) == len(vs_therapeutic_procedures)

def test_valueset_contains():
    vs_therapeutic_procedures = ValueSet.parse_file("./test/valuesets/therapeutic-procedure.json")

    cytokinetherapie = SCTCoding("84501003 | cytokinetherapie |")

    assert cytokinetherapie in vs_therapeutic_procedures

def test_descendant_of():
    radical_prostatectomy = SCTCoding("26294005 |Radical prostatectomy (procedure)|")
    vs_rad_prod = radical_prostatectomy.descendants(fhir_server=SCTFHIRTerminologyServer("https://snowstorm-aovarw23xa-uc.a.run.app/fhir"))

    ralp = SCTCoding("708919000 |Laparoscopic radical prostatectomy using robotic assistance (procedure)|")
    assert ralp in vs_rad_prod

def test_append_to_valueset():
    vs_therapeutic_procedures = ValueSet.parse_file("./test/valuesets/therapeutic-procedure.json")
    coding = Coding(code="this-is-a-test", system="http://example.com")
    
    vs_therapeutic_procedures.append(coding)

    assert coding in vs_therapeutic_procedures