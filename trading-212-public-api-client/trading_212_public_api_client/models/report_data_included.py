from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReportDataIncluded")


@_attrs_define
class ReportDataIncluded:
    """
    Attributes:
        include_dividends (Union[Unset, bool]):
        include_interest (Union[Unset, bool]):
        include_orders (Union[Unset, bool]):
        include_transactions (Union[Unset, bool]):
    """

    include_dividends: Union[Unset, bool] = UNSET
    include_interest: Union[Unset, bool] = UNSET
    include_orders: Union[Unset, bool] = UNSET
    include_transactions: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        include_dividends = self.include_dividends

        include_interest = self.include_interest

        include_orders = self.include_orders

        include_transactions = self.include_transactions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if include_dividends is not UNSET:
            field_dict["includeDividends"] = include_dividends
        if include_interest is not UNSET:
            field_dict["includeInterest"] = include_interest
        if include_orders is not UNSET:
            field_dict["includeOrders"] = include_orders
        if include_transactions is not UNSET:
            field_dict["includeTransactions"] = include_transactions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        include_dividends = d.pop("includeDividends", UNSET)

        include_interest = d.pop("includeInterest", UNSET)

        include_orders = d.pop("includeOrders", UNSET)

        include_transactions = d.pop("includeTransactions", UNSET)

        report_data_included = cls(
            include_dividends=include_dividends,
            include_interest=include_interest,
            include_orders=include_orders,
            include_transactions=include_transactions,
        )

        report_data_included.additional_properties = d
        return report_data_included

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
