from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.working_schedule import WorkingSchedule


T = TypeVar("T", bound="Exchange")


@_attrs_define
class Exchange:
    """
    Attributes:
        id (Union[Unset, int]):
        name (Union[Unset, str]):
        working_schedules (Union[Unset, list['WorkingSchedule']]):
    """

    id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    working_schedules: Union[Unset, list["WorkingSchedule"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        working_schedules: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.working_schedules, Unset):
            working_schedules = []
            for working_schedules_item_data in self.working_schedules:
                working_schedules_item = working_schedules_item_data.to_dict()
                working_schedules.append(working_schedules_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if working_schedules is not UNSET:
            field_dict["workingSchedules"] = working_schedules

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.working_schedule import WorkingSchedule

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        working_schedules = []
        _working_schedules = d.pop("workingSchedules", UNSET)
        for working_schedules_item_data in _working_schedules or []:
            working_schedules_item = WorkingSchedule.from_dict(working_schedules_item_data)

            working_schedules.append(working_schedules_item)

        exchange = cls(
            id=id,
            name=name,
            working_schedules=working_schedules,
        )

        exchange.additional_properties = d
        return exchange

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
