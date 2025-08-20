from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account_bucket_detailed_response import AccountBucketDetailedResponse
    from ..models.account_bucket_instrument_result import AccountBucketInstrumentResult


T = TypeVar("T", bound="AccountBucketInstrumentsDetailedResponse")


@_attrs_define
class AccountBucketInstrumentsDetailedResponse:
    """
    Attributes:
        instruments (Union[Unset, list['AccountBucketInstrumentResult']]):
        settings (Union[Unset, AccountBucketDetailedResponse]):
    """

    instruments: Union[Unset, list["AccountBucketInstrumentResult"]] = UNSET
    settings: Union[Unset, "AccountBucketDetailedResponse"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        instruments: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.instruments, Unset):
            instruments = []
            for instruments_item_data in self.instruments:
                instruments_item = instruments_item_data.to_dict()
                instruments.append(instruments_item)

        settings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if instruments is not UNSET:
            field_dict["instruments"] = instruments
        if settings is not UNSET:
            field_dict["settings"] = settings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.account_bucket_detailed_response import AccountBucketDetailedResponse
        from ..models.account_bucket_instrument_result import AccountBucketInstrumentResult

        d = src_dict.copy()
        instruments = []
        _instruments = d.pop("instruments", UNSET)
        for instruments_item_data in _instruments or []:
            instruments_item = AccountBucketInstrumentResult.from_dict(instruments_item_data)

            instruments.append(instruments_item)

        _settings = d.pop("settings", UNSET)
        settings: Union[Unset, AccountBucketDetailedResponse]
        if isinstance(_settings, Unset):
            settings = UNSET
        else:
            settings = AccountBucketDetailedResponse.from_dict(_settings)

        account_bucket_instruments_detailed_response = cls(
            instruments=instruments,
            settings=settings,
        )

        account_bucket_instruments_detailed_response.additional_properties = d
        return account_bucket_instruments_detailed_response

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
