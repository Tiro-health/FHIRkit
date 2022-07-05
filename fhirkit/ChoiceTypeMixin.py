import abc
from typing import (
    AbstractSet,
    Any,
    Callable,
    Dict,
    Mapping,
    Optional,
    Set,
    Tuple,
    Union,
    Generator,
    cast,
)

from pydantic import BaseModel, ValidationError, validator
from pydantic.utils import ValueItems, ROOT_KEY

IntStr = Union[int, str]
AbstractSetIntStr = AbstractSet[IntStr]
MappingIntStrAny = Mapping[IntStr, Any]
DictStrAny = Dict[str, Any]


class AbstractChoiceTypeMixin(abc.ABC, BaseModel):
    @property
    def choice_type_fields(self) -> Set[str]:
        return set()

    @property
    def polymorphic_fields(self) -> Set[str]:
        return set()

    def _iter(
        self,
        to_dict: bool = False,
        by_alias: bool = False,
        include: Union[
            AbstractSet[Union[int, str]], Mapping[Union[int, str], any]
        ] = None,
        exclude: Union[
            AbstractSet[Union[int, str]], Mapping[Union[int, str], any]
        ] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        exclude_choice_type: bool = False,
        exclude_polymorphic: bool = True,
    ) -> Generator[Tuple[str, Any], None, None]:
        if exclude_choice_type:
            exclude = ValueItems.merge(exclude, self.choice_type_fields)
        if exclude_polymorphic:
            exclude = ValueItems.merge(exclude, self.polymorphic_fields)
        return super()._iter(
            to_dict,
            by_alias,
            include,
            exclude,
            exclude_unset,
            exclude_defaults,
            exclude_none,
        )

    def dict(
        self,
        *,
        include: Union[AbstractSetIntStr, MappingIntStrAny] = None,
        exclude: Union[AbstractSetIntStr, MappingIntStrAny] = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        exclude_choice_type: bool = False,
        exclude_polymorphic: bool = True,
    ) -> DictStrAny:
        if exclude_choice_type:
            exclude = ValueItems.merge(exclude, self.choice_type_fields)
        if exclude_polymorphic:
            exclude = ValueItems.merge(exclude, self.polymorphic_fields)
        return dict(
            self._iter(
                to_dict=True,
                by_alias=by_alias,
                include=include,
                exclude=exclude,
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                exclude_none=exclude_none,
            )
        )

    def json(
        self,
        *,
        include: Union[AbstractSetIntStr, MappingIntStrAny] = None,
        exclude: Union[AbstractSetIntStr, MappingIntStrAny] = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        exclude_choice_type: bool = False,
        exclude_polymorphic: bool = True,
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
                exclude_choice_type=exclude_choice_type,
                exclude_polymorphic=exclude_polymorphic,
            )
        )
        if self.__custom_root_type__:
            data = data[ROOT_KEY]
        return self.__config__.json_dumps(data, default=encoder, **dumps_kwargs)


class ChoiceTypeMixinBase(AbstractChoiceTypeMixin):
    pass


def validate_choice_types(
    cls, v, values, choice_types: Set[str], polymorphic_field: str
):
    if v is not None:
        return v

    non_null_values = list(
        filter(
            lambda t: t[0] in choice_types and t[1] is not None,
            values.items(),
        )
    )
    if len(non_null_values) == 0:
        pass
        # candidate_choice_types = [
        # f
        # for f in values.keys()
        # if f.startswith(polymorphic_field) and values[f] is not None
        # ]
        # raise ValueError(
        #    f"{cls.__class__.__name__}.{polymorphic_field}[x] can not be None. Maybe one if these fields is not supported yet: {str(candidate_choice_types)}"
        #    ""
        # )
        return
    elif len(non_null_values) > 1:
        raise ValueError(
            f"{cls.__class__.__name__}.{polymorphic_field}[x] can only have one value."
        )
    return non_null_values[0][1]
