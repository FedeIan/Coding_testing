import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.report_response_status import ReportResponseStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.report_data_included import ReportDataIncluded


T = TypeVar("T", bound="ReportResponse")


@_attrs_define
class ReportResponse:
    """
    Attributes:
        data_included (Union[Unset, ReportDataIncluded]):
        download_link (Union[Unset, str]):
        report_id (Union[Unset, int]):
        status (Union[Unset, ReportResponseStatus]):
        time_from (Union[Unset, datetime.datetime]):
        time_to (Union[Unset, datetime.datetime]):
    """

    data_included: Union[Unset, "ReportDataIncluded"] = UNSET
    download_link: Union[Unset, str] = UNSET
    report_id: Union[Unset, int] = UNSET
    status: Union[Unset, ReportResponseStatus] = UNSET
    time_from: Union[Unset, datetime.datetime] = UNSET
    time_to: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data_included: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.data_included, Unset):
            data_included = self.data_included.to_dict()

        download_link = self.download_link

        report_id = self.report_id

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

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
        if download_link is not UNSET:
            field_dict["downloadLink"] = download_link
        if report_id is not UNSET:
            field_dict["reportId"] = report_id
        if status is not UNSET:
            field_dict["status"] = status
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

        download_link = d.pop("downloadLink", UNSET)

        report_id = d.pop("reportId", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, ReportResponseStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ReportResponseStatus(_status)

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

        report_response = cls(
            data_included=data_included,
            download_link=download_link,
            report_id=report_id,
            status=status,
            time_from=time_from,
            time_to=time_to,
        )

        report_response.additional_properties = d
        return report_response

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
