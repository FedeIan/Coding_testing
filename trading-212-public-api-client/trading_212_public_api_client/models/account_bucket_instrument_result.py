from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.instrument_issue import InstrumentIssue
    from ..models.investment_result import InvestmentResult


T = TypeVar("T", bound="AccountBucketInstrumentResult")


@_attrs_define
class AccountBucketInstrumentResult:
    """
    Attributes:
        current_share (Union[Unset, float]):
        expected_share (Union[Unset, float]):
        issues (Union[Unset, list['InstrumentIssue']]):
        owned_quantity (Union[Unset, float]):
        result (Union[Unset, InvestmentResult]):
        ticker (Union[Unset, str]):
    """

    current_share: Union[Unset, float] = UNSET
    expected_share: Union[Unset, float] = UNSET
    issues: Union[Unset, list["InstrumentIssue"]] = UNSET
    owned_quantity: Union[Unset, float] = UNSET
    result: Union[Unset, "InvestmentResult"] = UNSET
    ticker: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        current_share = self.current_share

        expected_share = self.expected_share

        issues: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.issues, Unset):
            issues = []
            for issues_item_data in self.issues:
                issues_item = issues_item_data.to_dict()
                issues.append(issues_item)

        owned_quantity = self.owned_quantity

        result: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.result, Unset):
            result = self.result.to_dict()

        ticker = self.ticker

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if current_share is not UNSET:
            field_dict["currentShare"] = current_share
        if expected_share is not UNSET:
            field_dict["expectedShare"] = expected_share
        if issues is not UNSET:
            field_dict["issues"] = issues
        if owned_quantity is not UNSET:
            field_dict["ownedQuantity"] = owned_quantity
        if result is not UNSET:
            field_dict["result"] = result
        if ticker is not UNSET:
            field_dict["ticker"] = ticker

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.instrument_issue import InstrumentIssue
        from ..models.investment_result import InvestmentResult

        d = src_dict.copy()
        current_share = d.pop("currentShare", UNSET)

        expected_share = d.pop("expectedShare", UNSET)

        issues = []
        _issues = d.pop("issues", UNSET)
        for issues_item_data in _issues or []:
            issues_item = InstrumentIssue.from_dict(issues_item_data)

            issues.append(issues_item)

        owned_quantity = d.pop("ownedQuantity", UNSET)

        _result = d.pop("result", UNSET)
        result: Union[Unset, InvestmentResult]
        if isinstance(_result, Unset):
            result = UNSET
        else:
            result = InvestmentResult.from_dict(_result)

        ticker = d.pop("ticker", UNSET)

        account_bucket_instrument_result = cls(
            current_share=current_share,
            expected_share=expected_share,
            issues=issues,
            owned_quantity=owned_quantity,
            result=result,
            ticker=ticker,
        )

        account_bucket_instrument_result.additional_properties = d
        return account_bucket_instrument_result

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
