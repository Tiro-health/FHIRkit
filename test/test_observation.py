from fhirkit import Observation
import pytest_check as check
import json

from fhirkit.elements.elements import Quantity


def test_parse_observation():
    obs = Observation.parse_file("./test/observation.json")
    obs_dict = obs.dict()
    check.is_in("value", obs_dict)
    check.is_instance(obs.value, Quantity)
    check.is_not_in("valueQuantity", obs_dict)
    reconstructed = json.loads(obs.json())
    check.is_in("valueQuantity", reconstructed)
