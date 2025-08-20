import datetime
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.history_transaction_item_type import HistoryTransactionItemType
from ..types import UNSET, Unset

T = TypeVar("T", bound="HistoryTransactionItem")


@_attrs_define
class HistoryTransactionItem:
    """
    Attributes:
        amount (Union[Unset, float]): In the account currency
        date_time (Union[Unset, datetime.datetime]):
        reference (Union[Unset, str]): ID
        type_ (Union[Unset, HistoryTransactionItemType]):
    """

    amount: Union[Unset, float] = UNSET
    date_time: Union[Unset, datetime.datetime] = UNSET
    reference: Union[Unset, str] = UNSET
    type_: Union[Unset, HistoryTransactionItemType] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount = self.amount

        date_time: Union[Unset, str] = UNSET
        if not isinstance(self.date_time, Unset):
            date_time = self.date_time.isoformat()

        reference = self.reference

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if amount is not UNSET:
            field_dict["amount"] = amount
        if date_time is not UNSET:
            field_dict["dateTime"] = date_time
        if reference is not UNSET:
            field_dict["reference"] = reference
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        amount = d.pop("amount", UNSET)

        _date_time = d.pop("dateTime", UNSET)
        date_time: Union[Unset, datetime.datetime]
        if isinstance(_date_time, Unset):
            date_time = UNSET
        else:
            date_time = isoparse(_date_time)

        reference = d.pop("reference", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, HistoryTransactionItemType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = HistoryTransactionItemType(_type_)

        history_transaction_item = cls(
            amount=amount,
            date_time=date_time,
            reference=reference,
            type_=type_,
        )

        history_transaction_item.additional_properties = d
        return history_transaction_item

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
