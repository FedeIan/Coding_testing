import datetime
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.time_event_type import TimeEventType
from ..types import UNSET, Unset

T = TypeVar("T", bound="TimeEvent")


@_attrs_define
class TimeEvent:
    """
    Attributes:
        date (Union[Unset, datetime.datetime]):
        type_ (Union[Unset, TimeEventType]):
    """

    date: Union[Unset, datetime.datetime] = UNSET
    type_: Union[Unset, TimeEventType] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if date is not UNSET:
            field_dict["date"] = date
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.datetime]
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, TimeEventType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = TimeEventType(_type_)

        time_event = cls(
            date=date,
            type_=type_,
        )

        time_event.additional_properties = d
        return time_event

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
