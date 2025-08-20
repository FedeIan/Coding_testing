from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.instrument_issue_name import InstrumentIssueName
from ..models.instrument_issue_severity import InstrumentIssueSeverity
from ..types import UNSET, Unset

T = TypeVar("T", bound="InstrumentIssue")


@_attrs_define
class InstrumentIssue:
    """
    Attributes:
        name (Union[Unset, InstrumentIssueName]):
        severity (Union[Unset, InstrumentIssueSeverity]):
    """

    name: Union[Unset, InstrumentIssueName] = UNSET
    severity: Union[Unset, InstrumentIssueSeverity] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name: Union[Unset, str] = UNSET
        if not isinstance(self.name, Unset):
            name = self.name.value

        severity: Union[Unset, str] = UNSET
        if not isinstance(self.severity, Unset):
            severity = self.severity.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if severity is not UNSET:
            field_dict["severity"] = severity

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        _name = d.pop("name", UNSET)
        name: Union[Unset, InstrumentIssueName]
        if isinstance(_name, Unset):
            name = UNSET
        else:
            name = InstrumentIssueName(_name)

        _severity = d.pop("severity", UNSET)
        severity: Union[Unset, InstrumentIssueSeverity]
        if isinstance(_severity, Unset):
            severity = UNSET
        else:
            severity = InstrumentIssueSeverity(_severity)

        instrument_issue = cls(
            name=name,
            severity=severity,
        )

        instrument_issue.additional_properties = d
        return instrument_issue

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
