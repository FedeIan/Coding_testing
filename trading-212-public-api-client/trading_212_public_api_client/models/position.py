import datetime
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.position_frontend import PositionFrontend
from ..types import UNSET, Unset

T = TypeVar("T", bound="Position")


@_attrs_define
class Position:
    """
    Attributes:
        average_price (Union[Unset, float]):
        current_price (Union[Unset, float]):
        frontend (Union[Unset, PositionFrontend]): Origin
        fx_ppl (Union[Unset, float]): Forex movement impact, only applies to positions with instrument currency that
            differs from the accounts'
        initial_fill_date (Union[Unset, datetime.datetime]):
        max_buy (Union[Unset, float]): Additional quantity that can be bought
        max_sell (Union[Unset, float]): Quantity that can be sold
        pie_quantity (Union[Unset, float]): Invested in pies
        ppl (Union[Unset, float]):
        quantity (Union[Unset, float]):
        ticker (Union[Unset, str]): Unique instrument identifier Example: AAPL_US_EQ.
    """

    average_price: Union[Unset, float] = UNSET
    current_price: Union[Unset, float] = UNSET
    frontend: Union[Unset, PositionFrontend] = UNSET
    fx_ppl: Union[Unset, float] = UNSET
    initial_fill_date: Union[Unset, datetime.datetime] = UNSET
    max_buy: Union[Unset, float] = UNSET
    max_sell: Union[Unset, float] = UNSET
    pie_quantity: Union[Unset, float] = UNSET
    ppl: Union[Unset, float] = UNSET
    quantity: Union[Unset, float] = UNSET
    ticker: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        average_price = self.average_price

        current_price = self.current_price

        frontend: Union[Unset, str] = UNSET
        if not isinstance(self.frontend, Unset):
            frontend = self.frontend.value

        fx_ppl = self.fx_ppl

        initial_fill_date: Union[Unset, str] = UNSET
        if not isinstance(self.initial_fill_date, Unset):
            initial_fill_date = self.initial_fill_date.isoformat()

        max_buy = self.max_buy

        max_sell = self.max_sell

        pie_quantity = self.pie_quantity

        ppl = self.ppl

        quantity = self.quantity

        ticker = self.ticker

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if average_price is not UNSET:
            field_dict["averagePrice"] = average_price
        if current_price is not UNSET:
            field_dict["currentPrice"] = current_price
        if frontend is not UNSET:
            field_dict["frontend"] = frontend
        if fx_ppl is not UNSET:
            field_dict["fxPpl"] = fx_ppl
        if initial_fill_date is not UNSET:
            field_dict["initialFillDate"] = initial_fill_date
        if max_buy is not UNSET:
            field_dict["maxBuy"] = max_buy
        if max_sell is not UNSET:
            field_dict["maxSell"] = max_sell
        if pie_quantity is not UNSET:
            field_dict["pieQuantity"] = pie_quantity
        if ppl is not UNSET:
            field_dict["ppl"] = ppl
        if quantity is not UNSET:
            field_dict["quantity"] = quantity
        if ticker is not UNSET:
            field_dict["ticker"] = ticker

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        average_price = d.pop("averagePrice", UNSET)

        current_price = d.pop("currentPrice", UNSET)

        _frontend = d.pop("frontend", UNSET)
        frontend: Union[Unset, PositionFrontend]
        if isinstance(_frontend, Unset):
            frontend = UNSET
        else:
            frontend = PositionFrontend(_frontend)

        fx_ppl = d.pop("fxPpl", UNSET)

        _initial_fill_date = d.pop("initialFillDate", UNSET)
        initial_fill_date: Union[Unset, datetime.datetime]
        if isinstance(_initial_fill_date, Unset):
            initial_fill_date = UNSET
        else:
            initial_fill_date = isoparse(_initial_fill_date)

        max_buy = d.pop("maxBuy", UNSET)

        max_sell = d.pop("maxSell", UNSET)

        pie_quantity = d.pop("pieQuantity", UNSET)

        ppl = d.pop("ppl", UNSET)

        quantity = d.pop("quantity", UNSET)

        ticker = d.pop("ticker", UNSET)

        position = cls(
            average_price=average_price,
            current_price=current_price,
            frontend=frontend,
            fx_ppl=fx_ppl,
            initial_fill_date=initial_fill_date,
            max_buy=max_buy,
            max_sell=max_sell,
            pie_quantity=pie_quantity,
            ppl=ppl,
            quantity=quantity,
            ticker=ticker,
        )

        position.additional_properties = d
        return position

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
