from typing import List, Set, Union
from pydantic import HttpUrl

class ExpansionError(Exception):
    pass

class AbstractFHIRServer:
    def __init__(self, baseUrl:Union[str, HttpUrl]) -> None:
        self.baseUrl = HttpUrl(baseUrl)

    def expand_value_set(self, *args, **kwargs):
        raise NotImplementedError()

        
