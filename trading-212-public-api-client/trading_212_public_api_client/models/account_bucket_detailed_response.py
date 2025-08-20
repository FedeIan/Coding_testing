import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.account_bucket_detailed_response_dividend_cash_action import (
    AccountBucketDetailedResponseDividendCashAction,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account_bucket_detailed_response_instrument_shares import (
        AccountBucketDetailedResponseInstrumentShares,
    )


T = TypeVar("T", bound="AccountBucketDetailedResponse")


@_attrs_define
class AccountBucketDetailedResponse:
    """
    Attributes:
        creation_date (Union[Unset, datetime.datetime]):
        dividend_cash_action (Union[Unset, AccountBucketDetailedResponseDividendCashAction]):
        end_date (Union[Unset, datetime.datetime]):
        goal (Union[Unset, float]):
        icon (Union[Unset, str]):
        id (Union[Unset, int]):
        initial_investment (Union[Unset, float]):
        instrument_shares (Union[Unset, AccountBucketDetailedResponseInstrumentShares]):
        name (Union[Unset, str]):
        public_url (Union[Unset, str]):
    """

    creation_date: Union[Unset, datetime.datetime] = UNSET
    dividend_cash_action: Union[Unset, AccountBucketDetailedResponseDividendCashAction] = UNSET
    end_date: Union[Unset, datetime.datetime] = UNSET
    goal: Union[Unset, float] = UNSET
    icon: Union[Unset, str] = UNSET
    id: Union[Unset, int] = UNSET
    initial_investment: Union[Unset, float] = UNSET
    instrument_shares: Union[Unset, "AccountBucketDetailedResponseInstrumentShares"] = UNSET
    name: Union[Unset, str] = UNSET
    public_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        creation_date: Union[Unset, str] = UNSET
        if not isinstance(self.creation_date, Unset):
            creation_date = self.creation_date.isoformat()

        dividend_cash_action: Union[Unset, str] = UNSET
        if not isinstance(self.dividend_cash_action, Unset):
            dividend_cash_action = self.dividend_cash_action.value

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        goal = self.goal

        icon = self.icon

        id = self.id

        initial_investment = self.initial_investment

        instrument_shares: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.instrument_shares, Unset):
            instrument_shares = self.instrument_shares.to_dict()

        name = self.name

        public_url = self.public_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if creation_date is not UNSET:
            field_dict["creationDate"] = creation_date
        if dividend_cash_action is not UNSET:
            field_dict["dividendCashAction"] = dividend_cash_action
        if end_date is not UNSET:
            field_dict["endDate"] = end_date
        if goal is not UNSET:
            field_dict["goal"] = goal
        if icon is not UNSET:
            field_dict["icon"] = icon
        if id is not UNSET:
            field_dict["id"] = id
        if initial_investment is not UNSET:
            field_dict["initialInvestment"] = initial_investment
        if instrument_shares is not UNSET:
            field_dict["instrumentShares"] = instrument_shares
        if name is not UNSET:
            field_dict["name"] = name
        if public_url is not UNSET:
            field_dict["publicUrl"] = public_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.account_bucket_detailed_response_instrument_shares import (
            AccountBucketDetailedResponseInstrumentShares,
        )

        d = src_dict.copy()
        _creation_date = d.pop("creationDate", UNSET)
        creation_date: Union[Unset, datetime.datetime]
        if isinstance(_creation_date, Unset):
            creation_date = UNSET
        else:
            creation_date = isoparse(_creation_date)

        _dividend_cash_action = d.pop("dividendCashAction", UNSET)
        dividend_cash_action: Union[Unset, AccountBucketDetailedResponseDividendCashAction]
        if isinstance(_dividend_cash_action, Unset):
            dividend_cash_action = UNSET
        else:
            dividend_cash_action = AccountBucketDetailedResponseDividendCashAction(_dividend_cash_action)

        _end_date = d.pop("endDate", UNSET)
        end_date: Union[Unset, datetime.datetime]
        if isinstance(_end_date, Unset):
            end_date = UNSET
        else:
            end_date = isoparse(_end_date)

        goal = d.pop("goal", UNSET)

        icon = d.pop("icon", UNSET)

        id = d.pop("id", UNSET)

        initial_investment = d.pop("initialInvestment", UNSET)

        _instrument_shares = d.pop("instrumentShares", UNSET)
        instrument_shares: Union[Unset, AccountBucketDetailedResponseInstrumentShares]
        if isinstance(_instrument_shares, Unset):
            instrument_shares = UNSET
        else:
            instrument_shares = AccountBucketDetailedResponseInstrumentShares.from_dict(_instrument_shares)

        name = d.pop("name", UNSET)

        public_url = d.pop("publicUrl", UNSET)

        account_bucket_detailed_response = cls(
            creation_date=creation_date,
            dividend_cash_action=dividend_cash_action,
            end_date=end_date,
            goal=goal,
            icon=icon,
            id=id,
            initial_investment=initial_investment,
            instrument_shares=instrument_shares,
            name=name,
            public_url=public_url,
        )

        account_bucket_detailed_response.additional_properties = d
        return account_bucket_detailed_response

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
