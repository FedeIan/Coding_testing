from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Cash")


@_attrs_define
class Cash:
    """
    Attributes:
        blocked (Union[Unset, float]):
        free (Union[Unset, float]):
        invested (Union[Unset, float]):
        pie_cash (Union[Unset, float]): Invested cash in pies
        ppl (Union[Unset, float]):
        result (Union[Unset, float]):
        total (Union[Unset, float]):
    """

    blocked: Union[Unset, float] = UNSET
    free: Union[Unset, float] = UNSET
    invested: Union[Unset, float] = UNSET
    pie_cash: Union[Unset, float] = UNSET
    ppl: Union[Unset, float] = UNSET
    result: Union[Unset, float] = UNSET
    total: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        blocked = self.blocked

        free = self.free

        invested = self.invested

        pie_cash = self.pie_cash

        ppl = self.ppl

        result = self.result

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if blocked is not UNSET:
            field_dict["blocked"] = blocked
        if free is not UNSET:
            field_dict["free"] = free
        if invested is not UNSET:
            field_dict["invested"] = invested
        if pie_cash is not UNSET:
            field_dict["pieCash"] = pie_cash
        if ppl is not UNSET:
            field_dict["ppl"] = ppl
        if result is not UNSET:
            field_dict["result"] = result
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        blocked = d.pop("blocked", UNSET)

        free = d.pop("free", UNSET)

        invested = d.pop("invested", UNSET)

        pie_cash = d.pop("pieCash", UNSET)

        ppl = d.pop("ppl", UNSET)

        result = d.pop("result", UNSET)

        total = d.pop("total", UNSET)

        cash = cls(
            blocked=blocked,
            free=free,
            invested=invested,
            pie_cash=pie_cash,
            ppl=ppl,
            result=result,
            total=total,
        )

        cash.additional_properties = d
        return cash

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
