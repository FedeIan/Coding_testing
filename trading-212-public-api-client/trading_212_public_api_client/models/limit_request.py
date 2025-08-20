from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.limit_request_time_validity import LimitRequestTimeValidity
from ..types import UNSET, Unset

T = TypeVar("T", bound="LimitRequest")


@_attrs_define
class LimitRequest:
    """
    Attributes:
        limit_price (Union[Unset, float]):  Example: 100.23.
        quantity (Union[Unset, float]):  Example: 0.1.
        ticker (Union[Unset, str]):  Example: AAPL_US_EQ.
        time_validity (Union[Unset, LimitRequestTimeValidity]): Expiration Example: DAY.
    """

    limit_price: Union[Unset, float] = UNSET
    quantity: Union[Unset, float] = UNSET
    ticker: Union[Unset, str] = UNSET
    time_validity: Union[Unset, LimitRequestTimeValidity] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        limit_price = self.limit_price

        quantity = self.quantity

        ticker = self.ticker

        time_validity: Union[Unset, str] = UNSET
        if not isinstance(self.time_validity, Unset):
            time_validity = self.time_validity.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if limit_price is not UNSET:
            field_dict["limitPrice"] = limit_price
        if quantity is not UNSET:
            field_dict["quantity"] = quantity
        if ticker is not UNSET:
            field_dict["ticker"] = ticker
        if time_validity is not UNSET:
            field_dict["timeValidity"] = time_validity

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        limit_price = d.pop("limitPrice", UNSET)

        quantity = d.pop("quantity", UNSET)

        ticker = d.pop("ticker", UNSET)

        _time_validity = d.pop("timeValidity", UNSET)
        time_validity: Union[Unset, LimitRequestTimeValidity]
        if isinstance(_time_validity, Unset):
            time_validity = UNSET
        else:
            time_validity = LimitRequestTimeValidity(_time_validity)

        limit_request = cls(
            limit_price=limit_price,
            quantity=quantity,
            ticker=ticker,
            time_validity=time_validity,
        )

        limit_request.additional_properties = d
        return limit_request

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
