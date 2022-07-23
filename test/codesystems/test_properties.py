import pytest_check as check
from fhirkit import CodeSystem


def test_codesystem_property():
    semantic_axes = CodeSystem.parse_file(
        "./test/codesystems/CodeSystem-semantic-axes.json"
    )
    for code in semantic_axes.concept:
        check.is_not_none(code.eq)
