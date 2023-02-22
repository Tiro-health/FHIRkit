from fhirkit.elements import Meta
from fhirkit.primitive_datatypes import URI
from pydantic import parse_obj_as

source="ANONIEM_id 1602 CAS.xlsx#R0"
parse_obj_as(URI, source)
meta=Meta(source=source)
#print(Meta())
#meta=Meta(source=source)
#print(meta)RI
    
