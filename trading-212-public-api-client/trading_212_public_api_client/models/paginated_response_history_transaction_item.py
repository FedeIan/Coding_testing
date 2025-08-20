from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.history_transaction_item import HistoryTransactionItem


T = TypeVar("T", bound="PaginatedResponseHistoryTransactionItem")


@_attrs_define
class PaginatedResponseHistoryTransactionItem:
    """
    Attributes:
        items (Union[Unset, list['HistoryTransactionItem']]):
        next_page_path (Union[Unset, str]):
    """

    items: Union[Unset, list["HistoryTransactionItem"]] = UNSET
    next_page_path: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        items: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.items, Unset):
            items = []
            for items_item_data in self.items:
                items_item = items_item_data.to_dict()
                items.append(items_item)

        next_page_path = self.next_page_path

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if items is not UNSET:
            field_dict["items"] = items
        if next_page_path is not UNSET:
            field_dict["nextPagePath"] = next_page_path

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.history_transaction_item import HistoryTransactionItem

        d = src_dict.copy()
        items = []
        _items = d.pop("items", UNSET)
        for items_item_data in _items or []:
            items_item = HistoryTransactionItem.from_dict(items_item_data)

            items.append(items_item)

        next_page_path = d.pop("nextPagePath", UNSET)

        paginated_response_history_transaction_item = cls(
            items=items,
            next_page_path=next_page_path,
        )

        paginated_response_history_transaction_item.additional_properties = d
        return paginated_response_history_transaction_item

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
