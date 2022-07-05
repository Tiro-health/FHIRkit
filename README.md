# FHIRkit

[![PyPI version](https://badge.fury.io/py/FHIRkit.svg)](https://badge.fury.io/py/FHIRkit)

Handle FHIR resources in a more efficient, and pythonic way

## Why FHIRKit

FHIRKit is a wrapper around [Pydantic](https://github.com/samuelcolvin/pydantic) that will help you parse FHIR JSON data. It comes with some utility functions to display resources 👀 and validate codes in those resources ✅.

After implementing calls to terminology servers over and over again 😥, we realized that Python developpers and data scientists want code like this:

```python
target_code = SCTCoding(code="298364001")
vs = target_code.descendants() # create a valueset by retrieving all descendants of a SNOMED-CT code
obs = Observation.parse_file("my_observation.json")
assert obs.code in vs, f"Observation has an invalid code={obs.code}, please provide a {target_code}"
#
# AssertionError
# Observation has an invalid code="55406008 | Hyperalgesia |", please provide a "298364001 | Finding of head region |"
```

Calls to terminology servers are handled for you and boilerplate code is reduced to simple Python operations 🎉.

**The goals of this package in a nutshell:**

- Parse FHIR/JSON(https://build.fhir.org/json.html) resources using predefined Pydantic models. These models automatically handle all inconveniences like [choice data types](https://www.hl7.org/fhir/formats.html#choice)s and datetime parsing for you.

- Perform validations and lookups for `code`, `coding`, `CodeableConcept` elements and expand `ValueSets` resources in a _pythonic_ way.

- Make FHIR Resources and FHIR Elements readable when printing them in the command-line or displaying them in a Jupyter Notebook. FHIRkit has some handy defaults for `__str__ `, `__repr__` and `__repr_html__` that take care of your development and debug experience. No huge nested dicts in your terminal or notebook.

- Turn a bunch of FHIR resources with the same type in a [FHIR DataFrame](https://github.com/Tiro-health/fhir-dataframes) _(still under development)_
