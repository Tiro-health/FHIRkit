from fhirkit import Observation
from fhirkit import SimpleFHIRStore
from fhirkit.elements.elements import Identifier, Reference


def test_resource_with_reference():
    store = SimpleFHIRStore()

    literal_ref = Reference(reference=f"Patient/123")

    observation = Observation(code={"text": "bloeddruk"}, value="hoog")
    # create reference given resource

    ref = store.create_reference(observation)

    # retrieve resource from reference
    resource = ref.resolve(store)
