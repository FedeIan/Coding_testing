from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MarketRequest")


@_attrs_define
class MarketRequest:
    """
    Attributes:
        quantity (Union[Unset, float]):  Example: 0.1.
        ticker (Union[Unset, str]):  Example: AAPL_US_EQ.
    """

    quantity: Union[Unset, float] = UNSET
    ticker: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        quantity = self.quantity

        ticker = self.ticker

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if quantity is not UNSET:
            field_dict["quantity"] = quantity
        if ticker is not UNSET:
            field_dict["ticker"] = ticker

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        quantity = d.pop("quantity", UNSET)

        ticker = d.pop("ticker", UNSET)

        market_request = cls(
            quantity=quantity,
            ticker=ticker,
        )

        market_request.additional_properties = d
        return market_request

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
