from datetime import datetime
from pydantic import constr


Id = constr(regex=r"[A-Za-z0-9\-\.]{1,64}")
Code = constr(regex=r"[^\s]+(\s[^\s]+)*")
Instant = constr(
    regex=r"([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])T([01][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)(\.[0-9]+)?(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))"
)
XHTML = constr()
dateTime = datetime
