from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.account_bucket_result_response_status import AccountBucketResultResponseStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dividend_details import DividendDetails
    from ..models.investment_result import InvestmentResult


T = TypeVar("T", bound="AccountBucketResultResponse")


@_attrs_define
class AccountBucketResultResponse:
    """
    Attributes:
        cash (Union[Unset, float]): Amount of money put into the pie in account currency
        dividend_details (Union[Unset, DividendDetails]):
        id (Union[Unset, int]):
        progress (Union[Unset, float]): Progress of the pie based on the set goal Example: 0.5.
        result (Union[Unset, InvestmentResult]):
        status (Union[Unset, AccountBucketResultResponseStatus]): Status of the pie based on the set goal
    """

    cash: Union[Unset, float] = UNSET
    dividend_details: Union[Unset, "DividendDetails"] = UNSET
    id: Union[Unset, int] = UNSET
    progress: Union[Unset, float] = UNSET
    result: Union[Unset, "InvestmentResult"] = UNSET
    status: Union[Unset, AccountBucketResultResponseStatus] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cash = self.cash

        dividend_details: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.dividend_details, Unset):
            dividend_details = self.dividend_details.to_dict()

        id = self.id

        progress = self.progress

        result: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.result, Unset):
            result = self.result.to_dict()

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cash is not UNSET:
            field_dict["cash"] = cash
        if dividend_details is not UNSET:
            field_dict["dividendDetails"] = dividend_details
        if id is not UNSET:
            field_dict["id"] = id
        if progress is not UNSET:
            field_dict["progress"] = progress
        if result is not UNSET:
            field_dict["result"] = result
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.dividend_details import DividendDetails
        from ..models.investment_result import InvestmentResult

        d = src_dict.copy()
        cash = d.pop("cash", UNSET)

        _dividend_details = d.pop("dividendDetails", UNSET)
        dividend_details: Union[Unset, DividendDetails]
        if isinstance(_dividend_details, Unset):
            dividend_details = UNSET
        else:
            dividend_details = DividendDetails.from_dict(_dividend_details)

        id = d.pop("id", UNSET)

        progress = d.pop("progress", UNSET)

        _result = d.pop("result", UNSET)
        result: Union[Unset, InvestmentResult]
        if isinstance(_result, Unset):
            result = UNSET
        else:
            result = InvestmentResult.from_dict(_result)

        _status = d.pop("status", UNSET)
        status: Union[Unset, AccountBucketResultResponseStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = AccountBucketResultResponseStatus(_status)

        account_bucket_result_response = cls(
            cash=cash,
            dividend_details=dividend_details,
            id=id,
            progress=progress,
            result=result,
            status=status,
        )

        account_bucket_result_response.additional_properties = d
        return account_bucket_result_response

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
