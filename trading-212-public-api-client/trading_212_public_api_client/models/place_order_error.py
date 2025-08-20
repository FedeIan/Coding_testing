from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.place_order_error_code import PlaceOrderErrorCode
from ..types import UNSET, Unset

T = TypeVar("T", bound="PlaceOrderError")


@_attrs_define
class PlaceOrderError:
    """
    Attributes:
        clarification (Union[Unset, str]):
        code (Union[Unset, PlaceOrderErrorCode]):
    """

    clarification: Union[Unset, str] = UNSET
    code: Union[Unset, PlaceOrderErrorCode] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        clarification = self.clarification

        code: Union[Unset, str] = UNSET
        if not isinstance(self.code, Unset):
            code = self.code.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if clarification is not UNSET:
            field_dict["clarification"] = clarification
        if code is not UNSET:
            field_dict["code"] = code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        clarification = d.pop("clarification", UNSET)

        _code = d.pop("code", UNSET)
        code: Union[Unset, PlaceOrderErrorCode]
        if isinstance(_code, Unset):
            code = UNSET
        else:
            code = PlaceOrderErrorCode(_code)

        place_order_error = cls(
            clarification=clarification,
            code=code,
        )

        place_order_error.additional_properties = d
        return place_order_error

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
