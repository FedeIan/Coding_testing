import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.report_data_included import ReportDataIncluded


T = TypeVar("T", bound="PublicReportRequest")


@_attrs_define
class PublicReportRequest:
    """
    Attributes:
        data_included (Union[Unset, ReportDataIncluded]):
        time_from (Union[Unset, datetime.datetime]):
        time_to (Union[Unset, datetime.datetime]):
    """

    data_included: Union[Unset, "ReportDataIncluded"] = UNSET
    time_from: Union[Unset, datetime.datetime] = UNSET
    time_to: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data_included: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.data_included, Unset):
            data_included = self.data_included.to_dict()

        time_from: Union[Unset, str] = UNSET
        if not isinstance(self.time_from, Unset):
            time_from = self.time_from.isoformat()

        time_to: Union[Unset, str] = UNSET
        if not isinstance(self.time_to, Unset):
            time_to = self.time_to.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data_included is not UNSET:
            field_dict["dataIncluded"] = data_included
        if time_from is not UNSET:
            field_dict["timeFrom"] = time_from
        if time_to is not UNSET:
            field_dict["timeTo"] = time_to

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.report_data_included import ReportDataIncluded

        d = src_dict.copy()
        _data_included = d.pop("dataIncluded", UNSET)
        data_included: Union[Unset, ReportDataIncluded]
        if isinstance(_data_included, Unset):
            data_included = UNSET
        else:
            data_included = ReportDataIncluded.from_dict(_data_included)

        _time_from = d.pop("timeFrom", UNSET)
        time_from: Union[Unset, datetime.datetime]
        if isinstance(_time_from, Unset):
            time_from = UNSET
        else:
            time_from = isoparse(_time_from)

        _time_to = d.pop("timeTo", UNSET)
        time_to: Union[Unset, datetime.datetime]
        if isinstance(_time_to, Unset):
            time_to = UNSET
        else:
            time_to = isoparse(_time_to)

        public_report_request = cls(
            data_included=data_included,
            time_from=time_from,
            time_to=time_to,
        )

        public_report_request.additional_properties = d
        return public_report_request

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
