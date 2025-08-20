from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.time_event import TimeEvent


T = TypeVar("T", bound="WorkingSchedule")


@_attrs_define
class WorkingSchedule:
    """
    Attributes:
        id (Union[Unset, int]):
        time_events (Union[Unset, list['TimeEvent']]):
    """

    id: Union[Unset, int] = UNSET
    time_events: Union[Unset, list["TimeEvent"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        time_events: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.time_events, Unset):
            time_events = []
            for time_events_item_data in self.time_events:
                time_events_item = time_events_item_data.to_dict()
                time_events.append(time_events_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if time_events is not UNSET:
            field_dict["timeEvents"] = time_events

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.time_event import TimeEvent

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        time_events = []
        _time_events = d.pop("timeEvents", UNSET)
        for time_events_item_data in _time_events or []:
            time_events_item = TimeEvent.from_dict(time_events_item_data)

            time_events.append(time_events_item)

        working_schedule = cls(
            id=id,
            time_events=time_events,
        )

        working_schedule.additional_properties = d
        return working_schedule

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
