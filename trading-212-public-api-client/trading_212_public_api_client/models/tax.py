import datetime
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.tax_name import TaxName
from ..types import UNSET, Unset

T = TypeVar("T", bound="Tax")


@_attrs_define
class Tax:
    """
    Attributes:
        fill_id (Union[Unset, str]):
        name (Union[Unset, TaxName]):
        quantity (Union[Unset, float]):
        time_charged (Union[Unset, datetime.datetime]):
    """

    fill_id: Union[Unset, str] = UNSET
    name: Union[Unset, TaxName] = UNSET
    quantity: Union[Unset, float] = UNSET
    time_charged: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        fill_id = self.fill_id

        name: Union[Unset, str] = UNSET
        if not isinstance(self.name, Unset):
            name = self.name.value

        quantity = self.quantity

        time_charged: Union[Unset, str] = UNSET
        if not isinstance(self.time_charged, Unset):
            time_charged = self.time_charged.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if fill_id is not UNSET:
            field_dict["fillId"] = fill_id
        if name is not UNSET:
            field_dict["name"] = name
        if quantity is not UNSET:
            field_dict["quantity"] = quantity
        if time_charged is not UNSET:
            field_dict["timeCharged"] = time_charged

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        fill_id = d.pop("fillId", UNSET)

        _name = d.pop("name", UNSET)
        name: Union[Unset, TaxName]
        if isinstance(_name, Unset):
            name = UNSET
        else:
            name = TaxName(_name)

        quantity = d.pop("quantity", UNSET)

        _time_charged = d.pop("timeCharged", UNSET)
        time_charged: Union[Unset, datetime.datetime]
        if isinstance(_time_charged, Unset):
            time_charged = UNSET
        else:
            time_charged = isoparse(_time_charged)

        tax = cls(
            fill_id=fill_id,
            name=name,
            quantity=quantity,
            time_charged=time_charged,
        )

        tax.additional_properties = d
        return tax

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
