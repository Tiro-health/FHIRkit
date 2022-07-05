from fhirkit import Observation


def test_parse_observation():
    Observation.parse_file("./test/observation.json")
