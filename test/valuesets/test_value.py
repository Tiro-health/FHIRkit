from tiro_fhir.Parameter import MultiValueType

def test_value_alias():

    param = MultiValueType(value=True)
    assert param.valueBoolean