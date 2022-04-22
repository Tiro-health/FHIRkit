#%%
import pandas as pd
from fhirkit.snomed.terminology import SCTCoding
from fhirkit.ValueSet import ValueSet

# %%
data = {
    "a": [SCTCoding("84501003 | cytokinetherapie |"), SCTCoding("385757394| test |")]
}
df = pd.DataFrame(data)
# %%
vs_therapeutic_procedures = ValueSet.parse_file(
    "./test/valuesets/therapeutic-procedure.json"
)

# %%
df.isin(vs_therapeutic_procedures)
# %%

vs_therapeutic_procedures.append(SCTCoding("385757394| test |"))
# %%
SCTCoding("385757394| test |") in vs_therapeutic_procedures
# %%
