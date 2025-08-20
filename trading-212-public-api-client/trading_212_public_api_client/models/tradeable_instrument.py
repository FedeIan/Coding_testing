import datetime
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.tradeable_instrument_type import TradeableInstrumentType
from ..types import UNSET, Unset

T = TypeVar("T", bound="TradeableInstrument")


@_attrs_define
class TradeableInstrument:
    """
    Attributes:
        added_on (Union[Unset, datetime.datetime]): On the platform since
        currency_code (Union[Unset, str]): ISO 4217 Example: USD.
        isin (Union[Unset, str]):
        max_open_quantity (Union[Unset, float]):
        min_trade_quantity (Union[Unset, float]): A single order must be equal to or exceed this value
        name (Union[Unset, str]):
        short_name (Union[Unset, str]):
        ticker (Union[Unset, str]): Unique identifier Example: AAPL_US_EQ.
        type_ (Union[Unset, TradeableInstrumentType]):  Example: ETF.
        working_schedule_id (Union[Unset, int]): Get items in the /exchanges endpoint
    """

    added_on: Union[Unset, datetime.datetime] = UNSET
    currency_code: Union[Unset, str] = UNSET
    isin: Union[Unset, str] = UNSET
    max_open_quantity: Union[Unset, float] = UNSET
    min_trade_quantity: Union[Unset, float] = UNSET
    name: Union[Unset, str] = UNSET
    short_name: Union[Unset, str] = UNSET
    ticker: Union[Unset, str] = UNSET
    type_: Union[Unset, TradeableInstrumentType] = UNSET
    working_schedule_id: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        added_on: Union[Unset, str] = UNSET
        if not isinstance(self.added_on, Unset):
            added_on = self.added_on.isoformat()

        currency_code = self.currency_code

        isin = self.isin

        max_open_quantity = self.max_open_quantity

        min_trade_quantity = self.min_trade_quantity

        name = self.name

        short_name = self.short_name

        ticker = self.ticker

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        working_schedule_id = self.working_schedule_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if added_on is not UNSET:
            field_dict["addedOn"] = added_on
        if currency_code is not UNSET:
            field_dict["currencyCode"] = currency_code
        if isin is not UNSET:
            field_dict["isin"] = isin
        if max_open_quantity is not UNSET:
            field_dict["maxOpenQuantity"] = max_open_quantity
        if min_trade_quantity is not UNSET:
            field_dict["minTradeQuantity"] = min_trade_quantity
        if name is not UNSET:
            field_dict["name"] = name
        if short_name is not UNSET:
            field_dict["shortName"] = short_name
        if ticker is not UNSET:
            field_dict["ticker"] = ticker
        if type_ is not UNSET:
            field_dict["type"] = type_
        if working_schedule_id is not UNSET:
            field_dict["workingScheduleId"] = working_schedule_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        _added_on = d.pop("addedOn", UNSET)
        added_on: Union[Unset, datetime.datetime]
        if isinstance(_added_on, Unset):
            added_on = UNSET
        else:
            added_on = isoparse(_added_on)

        currency_code = d.pop("currencyCode", UNSET)

        isin = d.pop("isin", UNSET)

        max_open_quantity = d.pop("maxOpenQuantity", UNSET)

        min_trade_quantity = d.pop("minTradeQuantity", UNSET)

        name = d.pop("name", UNSET)

        short_name = d.pop("shortName", UNSET)

        ticker = d.pop("ticker", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, TradeableInstrumentType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = TradeableInstrumentType(_type_)

        working_schedule_id = d.pop("workingScheduleId", UNSET)

        tradeable_instrument = cls(
            added_on=added_on,
            currency_code=currency_code,
            isin=isin,
            max_open_quantity=max_open_quantity,
            min_trade_quantity=min_trade_quantity,
            name=name,
            short_name=short_name,
            ticker=ticker,
            type_=type_,
            working_schedule_id=working_schedule_id,
        )

        tradeable_instrument.additional_properties = d
        return tradeable_instrument

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
