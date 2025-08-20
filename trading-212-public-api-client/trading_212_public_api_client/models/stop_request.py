from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.stop_request_time_validity import StopRequestTimeValidity
from ..types import UNSET, Unset

T = TypeVar("T", bound="StopRequest")


@_attrs_define
class StopRequest:
    """
    Attributes:
        quantity (Union[Unset, float]):  Example: 0.1.
        stop_price (Union[Unset, float]):  Example: 100.23.
        ticker (Union[Unset, str]):  Example: AAPL_US_EQ.
        time_validity (Union[Unset, StopRequestTimeValidity]): Expiration Example: DAY.
    """

    quantity: Union[Unset, float] = UNSET
    stop_price: Union[Unset, float] = UNSET
    ticker: Union[Unset, str] = UNSET
    time_validity: Union[Unset, StopRequestTimeValidity] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        quantity = self.quantity

        stop_price = self.stop_price

        ticker = self.ticker

        time_validity: Union[Unset, str] = UNSET
        if not isinstance(self.time_validity, Unset):
            time_validity = self.time_validity.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if quantity is not UNSET:
            field_dict["quantity"] = quantity
        if stop_price is not UNSET:
            field_dict["stopPrice"] = stop_price
        if ticker is not UNSET:
            field_dict["ticker"] = ticker
        if time_validity is not UNSET:
            field_dict["timeValidity"] = time_validity

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        quantity = d.pop("quantity", UNSET)

        stop_price = d.pop("stopPrice", UNSET)

        ticker = d.pop("ticker", UNSET)

        _time_validity = d.pop("timeValidity", UNSET)
        time_validity: Union[Unset, StopRequestTimeValidity]
        if isinstance(_time_validity, Unset):
            time_validity = UNSET
        else:
            time_validity = StopRequestTimeValidity(_time_validity)

        stop_request = cls(
            quantity=quantity,
            stop_price=stop_price,
            ticker=ticker,
            time_validity=time_validity,
        )

        stop_request.additional_properties = d
        return stop_request

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
