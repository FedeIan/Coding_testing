from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DuplicateBucketRequest")


@_attrs_define
class DuplicateBucketRequest:
    """
    Attributes:
        icon (Union[Unset, str]):
        name (Union[Unset, str]):
    """

    icon: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        icon = self.icon

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if icon is not UNSET:
            field_dict["icon"] = icon
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        icon = d.pop("icon", UNSET)

        name = d.pop("name", UNSET)

        duplicate_bucket_request = cls(
            icon=icon,
            name=name,
        )

        duplicate_bucket_request.additional_properties = d
        return duplicate_bucket_request

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
