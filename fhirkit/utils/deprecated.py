from typing import Type, TypeVar
import warnings
from pydantic import BaseModel

TModel = TypeVar("TModel", bound=BaseModel)
def deprecated(*, reason: str):
    """This is a decorator which can be used to mark Pydantic models as deprecated."""
    def decorator(cls: Type[TModel]):
        original_init = cls.__init__
        original_doc = cls.__doc__
        def new_init(self, *args, **kwargs):
            warnings.warn("This class is deprecated: " + reason, DeprecationWarning, stacklevel=2)
            original_init(self, *args, **kwargs)
        cls.__init__ = new_init

        cls.__doc__ = "Deprecated: " + reason
        if original_doc is not None:
            cls.__doc__ += "\n\n" + original_doc
        return cls
    return decorator