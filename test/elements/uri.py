from re import T
from pydantic import parse_obj_as
from pytest_check import check
from fhirkit.primitive_datatypes import (
    URI,
    AbsoluteURL,
    CanonicalURL,
    canonical,
    literal,
)


def test_uuid_is_valid_literal_uri():
    test_uri = "urn:uuid:c757873d-ec9a-4326-a141-556f43239520"
    uuid = parse_obj_as(literal, test_uri)


def test_oid_is_valid_literal_uri():
    test_uri = "urn:oid:2.16.840.1.113883.4.873"
    oid = parse_obj_as(literal, test_uri)


def test_relative_path_is_valid_literal_uri():
    test_uri = "Patient/example"
    url = parse_obj_as(literal, test_uri)
    assert url.resourceType == "Patient"
    assert url.resourceId == "example"


def test_canonical_url():
    test_uri = "http://hl7.org/fhir/ValueSet/account-balance-term|0.1#test"
    url = parse_obj_as(canonical, test_uri)
    assert isinstance(
        url, CanonicalURL
    ), "Expected instance AbsoluteURL but recieved %s" % type(url)
    assert url.fragment == "test"

def test_parse_uri():
    source="ANONIEM_id 1602 CAS.xlsx#R0"
    check.is_instance(source, URI)
    

