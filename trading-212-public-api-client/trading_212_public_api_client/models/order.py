import datetime
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.order_status import OrderStatus
from ..models.order_strategy import OrderStrategy
from ..models.order_type import OrderType
from ..types import UNSET, Unset

T = TypeVar("T", bound="Order")


@_attrs_define
class Order:
    """
    Attributes:
        creation_time (Union[Unset, datetime.datetime]):
        filled_quantity (Union[Unset, float]): Applicable to quantity orders
        filled_value (Union[Unset, float]): Applicable to value orders
        id (Union[Unset, int]):
        limit_price (Union[Unset, float]): Applicable to LIMIT and STOP_LIMIT orders
        quantity (Union[Unset, float]): Applicable to quantity orders
        status (Union[Unset, OrderStatus]):
        stop_price (Union[Unset, float]): Applicable to STOP and STOP_LIMIT orders
        strategy (Union[Unset, OrderStrategy]):
        ticker (Union[Unset, str]): Unique instrument identifier. Get from the /instruments endpoint Example:
            AAPL_US_EQ.
        type_ (Union[Unset, OrderType]):
        value (Union[Unset, float]): Applicable to value orders
    """

    creation_time: Union[Unset, datetime.datetime] = UNSET
    filled_quantity: Union[Unset, float] = UNSET
    filled_value: Union[Unset, float] = UNSET
    id: Union[Unset, int] = UNSET
    limit_price: Union[Unset, float] = UNSET
    quantity: Union[Unset, float] = UNSET
    status: Union[Unset, OrderStatus] = UNSET
    stop_price: Union[Unset, float] = UNSET
    strategy: Union[Unset, OrderStrategy] = UNSET
    ticker: Union[Unset, str] = UNSET
    type_: Union[Unset, OrderType] = UNSET
    value: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        creation_time: Union[Unset, str] = UNSET
        if not isinstance(self.creation_time, Unset):
            creation_time = self.creation_time.isoformat()

        filled_quantity = self.filled_quantity

        filled_value = self.filled_value

        id = self.id

        limit_price = self.limit_price

        quantity = self.quantity

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        stop_price = self.stop_price

        strategy: Union[Unset, str] = UNSET
        if not isinstance(self.strategy, Unset):
            strategy = self.strategy.value

        ticker = self.ticker

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if creation_time is not UNSET:
            field_dict["creationTime"] = creation_time
        if filled_quantity is not UNSET:
            field_dict["filledQuantity"] = filled_quantity
        if filled_value is not UNSET:
            field_dict["filledValue"] = filled_value
        if id is not UNSET:
            field_dict["id"] = id
        if limit_price is not UNSET:
            field_dict["limitPrice"] = limit_price
        if quantity is not UNSET:
            field_dict["quantity"] = quantity
        if status is not UNSET:
            field_dict["status"] = status
        if stop_price is not UNSET:
            field_dict["stopPrice"] = stop_price
        if strategy is not UNSET:
            field_dict["strategy"] = strategy
        if ticker is not UNSET:
            field_dict["ticker"] = ticker
        if type_ is not UNSET:
            field_dict["type"] = type_
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        _creation_time = d.pop("creationTime", UNSET)
        creation_time: Union[Unset, datetime.datetime]
        if isinstance(_creation_time, Unset):
            creation_time = UNSET
        else:
            creation_time = isoparse(_creation_time)

        filled_quantity = d.pop("filledQuantity", UNSET)

        filled_value = d.pop("filledValue", UNSET)

        id = d.pop("id", UNSET)

        limit_price = d.pop("limitPrice", UNSET)

        quantity = d.pop("quantity", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, OrderStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = OrderStatus(_status)

        stop_price = d.pop("stopPrice", UNSET)

        _strategy = d.pop("strategy", UNSET)
        strategy: Union[Unset, OrderStrategy]
        if isinstance(_strategy, Unset):
            strategy = UNSET
        else:
            strategy = OrderStrategy(_strategy)

        ticker = d.pop("ticker", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, OrderType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = OrderType(_type_)

        value = d.pop("value", UNSET)

        order = cls(
            creation_time=creation_time,
            filled_quantity=filled_quantity,
            filled_value=filled_value,
            id=id,
            limit_price=limit_price,
            quantity=quantity,
            status=status,
            stop_price=stop_price,
            strategy=strategy,
            ticker=ticker,
            type_=type_,
            value=value,
        )

        order.additional_properties = d
        return order

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
