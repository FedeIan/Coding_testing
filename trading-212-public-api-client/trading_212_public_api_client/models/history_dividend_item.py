import datetime
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="HistoryDividendItem")


@_attrs_define
class HistoryDividendItem:
    """
    Attributes:
        amount (Union[Unset, float]): In account currency
        amount_in_euro (Union[Unset, float]):
        gross_amount_per_share (Union[Unset, float]): In instrument currency
        paid_on (Union[Unset, datetime.datetime]):
        quantity (Union[Unset, float]):
        reference (Union[Unset, str]):
        ticker (Union[Unset, str]):
        type_ (Union[Unset, str]):
    """

    amount: Union[Unset, float] = UNSET
    amount_in_euro: Union[Unset, float] = UNSET
    gross_amount_per_share: Union[Unset, float] = UNSET
    paid_on: Union[Unset, datetime.datetime] = UNSET
    quantity: Union[Unset, float] = UNSET
    reference: Union[Unset, str] = UNSET
    ticker: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount = self.amount

        amount_in_euro = self.amount_in_euro

        gross_amount_per_share = self.gross_amount_per_share

        paid_on: Union[Unset, str] = UNSET
        if not isinstance(self.paid_on, Unset):
            paid_on = self.paid_on.isoformat()

        quantity = self.quantity

        reference = self.reference

        ticker = self.ticker

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if amount is not UNSET:
            field_dict["amount"] = amount
        if amount_in_euro is not UNSET:
            field_dict["amountInEuro"] = amount_in_euro
        if gross_amount_per_share is not UNSET:
            field_dict["grossAmountPerShare"] = gross_amount_per_share
        if paid_on is not UNSET:
            field_dict["paidOn"] = paid_on
        if quantity is not UNSET:
            field_dict["quantity"] = quantity
        if reference is not UNSET:
            field_dict["reference"] = reference
        if ticker is not UNSET:
            field_dict["ticker"] = ticker
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        amount = d.pop("amount", UNSET)

        amount_in_euro = d.pop("amountInEuro", UNSET)

        gross_amount_per_share = d.pop("grossAmountPerShare", UNSET)

        _paid_on = d.pop("paidOn", UNSET)
        paid_on: Union[Unset, datetime.datetime]
        if isinstance(_paid_on, Unset):
            paid_on = UNSET
        else:
            paid_on = isoparse(_paid_on)

        quantity = d.pop("quantity", UNSET)

        reference = d.pop("reference", UNSET)

        ticker = d.pop("ticker", UNSET)

        type_ = d.pop("type", UNSET)

        history_dividend_item = cls(
            amount=amount,
            amount_in_euro=amount_in_euro,
            gross_amount_per_share=gross_amount_per_share,
            paid_on=paid_on,
            quantity=quantity,
            reference=reference,
            ticker=ticker,
            type_=type_,
        )

        history_dividend_item.additional_properties = d
        return history_dividend_item

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
