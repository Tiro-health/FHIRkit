from typing import (
    AbstractSet,
    Any,
    Callable,
    Dict,
    Generator,
    Mapping,
    Optional,
    Tuple,
    Union,
    cast,
)
import warnings
import pydantic

from pydantic.utils import ROOT_KEY

from fhirkit.choice_type.validators import TYPE_NAME_ALIAS, get_matching_type

IntStr = Union[int, str]
AbstractSetIntStr = AbstractSet[IntStr]
MappingIntStrAny = Mapping[IntStr, Any]
DictStrAny = Dict[str, Any]


class BaseModel(pydantic.BaseModel):
    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    def _iter(
        self,
        to_dict: bool = False,
        by_alias: bool = False,
        include: Union[AbstractSetIntStr, MappingIntStrAny] = None,
        exclude: Union[AbstractSetIntStr, MappingIntStrAny] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        exclude_empty: bool = True,
    ) -> Generator[Tuple[str, Any], None, None]:
        for k, v in super()._iter(
            to_dict,
            by_alias,
            include,
            exclude,
            exclude_unset,
            exclude_defaults,
            exclude_none,
        ):
            if exclude_empty:
                if v is None:
                    continue
                try:
                    if len(v) == 0:
                        continue
                except TypeError:
                    pass
            if by_alias and k in self.__fields__:
                field = self.__fields__[k]
                if "choice_type" in field.field_info.extra:
                    # notice that 'v' can be a dict when are being called from Model.dict()
                    # this is why we use self.__getattribute to get the original type
                    type_class = get_matching_type(self.__getattribute__(k), field)
                    suffix = TYPE_NAME_ALIAS.get(
                        type_class.__name__, type_class.__name__
                    )
                    suffix = suffix[:1].title() + suffix[1:]
                    k = k + suffix
            yield k, v

    def dict(
        self,
        *,
        include: Union[AbstractSetIntStr, MappingIntStrAny] = None,
        exclude: Union[AbstractSetIntStr, MappingIntStrAny] = None,
        by_alias: bool = False,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        exclude_empty: bool = True,
    ) -> DictStrAny:
        """
        Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

        """
        if skip_defaults is not None:
            warnings.warn(
                f'{self.__class__.__name__}.dict(): "skip_defaults" is deprecated and replaced by "exclude_unset"',
                DeprecationWarning,
            )
            exclude_unset = skip_defaults
        return dict(
            self._iter(
                to_dict=True,
                by_alias=by_alias,
                include=include,
                exclude=exclude,
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                exclude_none=exclude_none,
                exclude_empty=exclude_empty,
            )
        )

    def json(
        self,
        *,
        include: Union[AbstractSetIntStr, MappingIntStrAny] = None,
        exclude: Union[AbstractSetIntStr, MappingIntStrAny] = None,
        by_alias: bool = True,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = True,
        exclude_empty: bool = True,
        encoder: Optional[Callable[[Any], Any]] = None,
        models_as_dict: bool = True,
        **dumps_kwargs: Any,
    ) -> str:
        encoder = cast(Callable[[Any], Any], encoder or self.__json_encoder__)

        # We don't directly call `self.dict()`, which does exactly this with `to_dict=True`
        # because we want to be able to keep raw `BaseModel` instances and not as `dict`.
        # This allows users to write custom JSON encoders for given `BaseModel` classes.
        data = dict(
            self._iter(
                to_dict=models_as_dict,
                by_alias=by_alias,
                include=include,
                exclude=exclude,
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                exclude_none=exclude_none,
                exclude_empty=exclude_empty,
            )
        )
        if self.__custom_root_type__:
            data = data[ROOT_KEY]
        return self.__config__.json_dumps(data, default=encoder, **dumps_kwargs)
