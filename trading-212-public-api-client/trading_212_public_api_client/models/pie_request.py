import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.pie_request_dividend_cash_action import PieRequestDividendCashAction
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.pie_request_instrument_shares import PieRequestInstrumentShares


T = TypeVar("T", bound="PieRequest")


@_attrs_define
class PieRequest:
    """
    Attributes:
        dividend_cash_action (Union[Unset, PieRequestDividendCashAction]):
        end_date (Union[Unset, datetime.datetime]):
        goal (Union[Unset, float]): Total desired value of the pie in account currency
        icon (Union[Unset, str]):
        instrument_shares (Union[Unset, PieRequestInstrumentShares]):  Example: {'AAPL_US_EQ': 0.5, 'MSFT_US_EQ': 0.5}.
        name (Union[Unset, str]):
    """

    dividend_cash_action: Union[Unset, PieRequestDividendCashAction] = UNSET
    end_date: Union[Unset, datetime.datetime] = UNSET
    goal: Union[Unset, float] = UNSET
    icon: Union[Unset, str] = UNSET
    instrument_shares: Union[Unset, "PieRequestInstrumentShares"] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dividend_cash_action: Union[Unset, str] = UNSET
        if not isinstance(self.dividend_cash_action, Unset):
            dividend_cash_action = self.dividend_cash_action.value

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        goal = self.goal

        icon = self.icon

        instrument_shares: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.instrument_shares, Unset):
            instrument_shares = self.instrument_shares.to_dict()

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if dividend_cash_action is not UNSET:
            field_dict["dividendCashAction"] = dividend_cash_action
        if end_date is not UNSET:
            field_dict["endDate"] = end_date
        if goal is not UNSET:
            field_dict["goal"] = goal
        if icon is not UNSET:
            field_dict["icon"] = icon
        if instrument_shares is not UNSET:
            field_dict["instrumentShares"] = instrument_shares
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.pie_request_instrument_shares import PieRequestInstrumentShares

        d = src_dict.copy()
        _dividend_cash_action = d.pop("dividendCashAction", UNSET)
        dividend_cash_action: Union[Unset, PieRequestDividendCashAction]
        if isinstance(_dividend_cash_action, Unset):
            dividend_cash_action = UNSET
        else:
            dividend_cash_action = PieRequestDividendCashAction(_dividend_cash_action)

        _end_date = d.pop("endDate", UNSET)
        end_date: Union[Unset, datetime.datetime]
        if isinstance(_end_date, Unset):
            end_date = UNSET
        else:
            end_date = isoparse(_end_date)

        goal = d.pop("goal", UNSET)

        icon = d.pop("icon", UNSET)

        _instrument_shares = d.pop("instrumentShares", UNSET)
        instrument_shares: Union[Unset, PieRequestInstrumentShares]
        if isinstance(_instrument_shares, Unset):
            instrument_shares = UNSET
        else:
            instrument_shares = PieRequestInstrumentShares.from_dict(_instrument_shares)

        name = d.pop("name", UNSET)

        pie_request = cls(
            dividend_cash_action=dividend_cash_action,
            end_date=end_date,
            goal=goal,
            icon=icon,
            instrument_shares=instrument_shares,
            name=name,
        )

        pie_request.additional_properties = d
        return pie_request

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
