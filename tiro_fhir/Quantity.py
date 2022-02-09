
from typing import Literal, Optional
from pydantic import BaseModel, HttpUrl

class Quantity(BaseModel):
    value: float
    comparator: Optional[Literal["<", "<=", ">=", ">"]]
    unit: str
    system: HttpUrl
    code: str
