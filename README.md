# FHIRkit

Handle FHIR resources in a more efficient, and pythonic way


## Why FHIRKit
FHIRKit is a wrapper around [Pydantic](https://github.com/samuelcolvin/pydantic) that will help you parse FHIR JSON data. It comes with some utility functions to display resources 👀 and validate codes in those resources ✅.

__The goals of this package in a nutshell:__
- Parse [`application/fhir+json`](https://build.fhir.org/json.html) content using predefined Pydantic models. These models automatically handle [choice data type](https://www.hl7.org/fhir/formats.html#choice)s (ex. `value[x]`) for you by creating an [alias](https://pydantic-docs.helpmanual.io/usage/model_config/#alias-precedence).
- Perform operation on `code`, `coding`, `CodeableConcept` elements and `ValueSets` resources in a *pythonic* way.
  
    After implementing calls to terminology servers over and over again 😥, we realized that Python-developers want code like this:
    ```python
    target_code = SCTCoding(code="298364001")
    vs = target_code.descendants() # create a valueset by retrieving all descendants of a SNOMED-CT code
    obs = Observation.parse_file("my_observation.json")
     
    assert obs.code in vs, f"Observation has an invalid code={obs.code}, please provide a {target_code}"
    # 
    # AssertionError
    # Observation has an invalid code="55406008 | Hyperalgesia |", please provide a "298364001 | Finding of head region |"
    ```
    🎉 Calls to terminology servers are handled for you and boilerplate code is reduced to simple Python operations.
    
- Make FHIR Resources and FHIR Elements readable when printing them in the command-line or displaying them in a Jupyter Notebook. FHIRkit has some handy defaults for `__str__ `, `__repr__` and `__repr_html__` that take care of your development and debug experience. No huge nested dicts in your terminal or notebook.

- Turn a bunch of FHIR resources with the same type in a [FHIR DataFrame](https://github.com/Tiro-health/fhir-dataframes) *(still under development)*
