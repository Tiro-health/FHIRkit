from datetime import (
    datetime,
    time,
    date,
)
import re
from pydantic import ConstrainedStr


class Id(ConstrainedStr):
    regex = re.compile("[A-Za-z0-9\-\.]{1,64}")


class Code(ConstrainedStr):
    regex = re.compile("[^\s]+(\s[^\s]+)*")


class Instant(ConstrainedStr):
    regex = re.compile(
        "([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])T([01][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)(\.[0-9]+)?(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))"
    )


class XHTML(ConstrainedStr):
    pass


class dateTime(datetime):
    pass


class URI(ConstrainedStr):
    regex = re.compile("\S*")


class canonical(ConstrainedStr):
    regex = re.compile("|S*")


class decimal(float):
    pass
