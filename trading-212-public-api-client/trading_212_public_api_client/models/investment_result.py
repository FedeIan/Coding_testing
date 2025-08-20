from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="InvestmentResult")


@_attrs_define
class InvestmentResult:
    """
    Attributes:
        price_avg_invested_value (Union[Unset, float]):
        price_avg_result (Union[Unset, float]):
        price_avg_result_coef (Union[Unset, float]):
        price_avg_value (Union[Unset, float]):
    """

    price_avg_invested_value: Union[Unset, float] = UNSET
    price_avg_result: Union[Unset, float] = UNSET
    price_avg_result_coef: Union[Unset, float] = UNSET
    price_avg_value: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        price_avg_invested_value = self.price_avg_invested_value

        price_avg_result = self.price_avg_result

        price_avg_result_coef = self.price_avg_result_coef

        price_avg_value = self.price_avg_value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if price_avg_invested_value is not UNSET:
            field_dict["priceAvgInvestedValue"] = price_avg_invested_value
        if price_avg_result is not UNSET:
            field_dict["priceAvgResult"] = price_avg_result
        if price_avg_result_coef is not UNSET:
            field_dict["priceAvgResultCoef"] = price_avg_result_coef
        if price_avg_value is not UNSET:
            field_dict["priceAvgValue"] = price_avg_value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        price_avg_invested_value = d.pop("priceAvgInvestedValue", UNSET)

        price_avg_result = d.pop("priceAvgResult", UNSET)

        price_avg_result_coef = d.pop("priceAvgResultCoef", UNSET)

        price_avg_value = d.pop("priceAvgValue", UNSET)

        investment_result = cls(
            price_avg_invested_value=price_avg_invested_value,
            price_avg_result=price_avg_result,
            price_avg_result_coef=price_avg_result_coef,
            price_avg_value=price_avg_value,
        )

        investment_result.additional_properties = d
        return investment_result

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
