import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.historical_order_executor import HistoricalOrderExecutor
from ..models.historical_order_fill_type import HistoricalOrderFillType
from ..models.historical_order_status import HistoricalOrderStatus
from ..models.historical_order_time_validity import HistoricalOrderTimeValidity
from ..models.historical_order_type import HistoricalOrderType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tax import Tax


T = TypeVar("T", bound="HistoricalOrder")


@_attrs_define
class HistoricalOrder:
    """
    Attributes:
        date_created (Union[Unset, datetime.datetime]):
        date_executed (Union[Unset, datetime.datetime]):
        date_modified (Union[Unset, datetime.datetime]):
        executor (Union[Unset, HistoricalOrderExecutor]):
        fill_cost (Union[Unset, float]): In the instrument currency
        fill_id (Union[Unset, int]):
        fill_price (Union[Unset, float]): In the instrument currency
        fill_result (Union[Unset, float]):
        fill_type (Union[Unset, HistoricalOrderFillType]):
        filled_quantity (Union[Unset, float]): Applicable to quantity orders
        filled_value (Union[Unset, float]): Applicable to value orders
        id (Union[Unset, int]):
        limit_price (Union[Unset, float]): Applicable to limit orders
        ordered_quantity (Union[Unset, float]): Applicable to quantity orders
        ordered_value (Union[Unset, float]): Applicable to value orders
        parent_order (Union[Unset, int]):
        status (Union[Unset, HistoricalOrderStatus]):
        stop_price (Union[Unset, float]): Applicable to stop orders
        taxes (Union[Unset, list['Tax']]):
        ticker (Union[Unset, str]):
        time_validity (Union[Unset, HistoricalOrderTimeValidity]): Applicable to stop, limit and stopLimit orders
        type_ (Union[Unset, HistoricalOrderType]):
    """

    date_created: Union[Unset, datetime.datetime] = UNSET
    date_executed: Union[Unset, datetime.datetime] = UNSET
    date_modified: Union[Unset, datetime.datetime] = UNSET
    executor: Union[Unset, HistoricalOrderExecutor] = UNSET
    fill_cost: Union[Unset, float] = UNSET
    fill_id: Union[Unset, int] = UNSET
    fill_price: Union[Unset, float] = UNSET
    fill_result: Union[Unset, float] = UNSET
    fill_type: Union[Unset, HistoricalOrderFillType] = UNSET
    filled_quantity: Union[Unset, float] = UNSET
    filled_value: Union[Unset, float] = UNSET
    id: Union[Unset, int] = UNSET
    limit_price: Union[Unset, float] = UNSET
    ordered_quantity: Union[Unset, float] = UNSET
    ordered_value: Union[Unset, float] = UNSET
    parent_order: Union[Unset, int] = UNSET
    status: Union[Unset, HistoricalOrderStatus] = UNSET
    stop_price: Union[Unset, float] = UNSET
    taxes: Union[Unset, list["Tax"]] = UNSET
    ticker: Union[Unset, str] = UNSET
    time_validity: Union[Unset, HistoricalOrderTimeValidity] = UNSET
    type_: Union[Unset, HistoricalOrderType] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date_created: Union[Unset, str] = UNSET
        if not isinstance(self.date_created, Unset):
            date_created = self.date_created.isoformat()

        date_executed: Union[Unset, str] = UNSET
        if not isinstance(self.date_executed, Unset):
            date_executed = self.date_executed.isoformat()

        date_modified: Union[Unset, str] = UNSET
        if not isinstance(self.date_modified, Unset):
            date_modified = self.date_modified.isoformat()

        executor: Union[Unset, str] = UNSET
        if not isinstance(self.executor, Unset):
            executor = self.executor.value

        fill_cost = self.fill_cost

        fill_id = self.fill_id

        fill_price = self.fill_price

        fill_result = self.fill_result

        fill_type: Union[Unset, str] = UNSET
        if not isinstance(self.fill_type, Unset):
            fill_type = self.fill_type.value

        filled_quantity = self.filled_quantity

        filled_value = self.filled_value

        id = self.id

        limit_price = self.limit_price

        ordered_quantity = self.ordered_quantity

        ordered_value = self.ordered_value

        parent_order = self.parent_order

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        stop_price = self.stop_price

        taxes: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.taxes, Unset):
            taxes = []
            for taxes_item_data in self.taxes:
                taxes_item = taxes_item_data.to_dict()
                taxes.append(taxes_item)

        ticker = self.ticker

        time_validity: Union[Unset, str] = UNSET
        if not isinstance(self.time_validity, Unset):
            time_validity = self.time_validity.value

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if date_created is not UNSET:
            field_dict["dateCreated"] = date_created
        if date_executed is not UNSET:
            field_dict["dateExecuted"] = date_executed
        if date_modified is not UNSET:
            field_dict["dateModified"] = date_modified
        if executor is not UNSET:
            field_dict["executor"] = executor
        if fill_cost is not UNSET:
            field_dict["fillCost"] = fill_cost
        if fill_id is not UNSET:
            field_dict["fillId"] = fill_id
        if fill_price is not UNSET:
            field_dict["fillPrice"] = fill_price
        if fill_result is not UNSET:
            field_dict["fillResult"] = fill_result
        if fill_type is not UNSET:
            field_dict["fillType"] = fill_type
        if filled_quantity is not UNSET:
            field_dict["filledQuantity"] = filled_quantity
        if filled_value is not UNSET:
            field_dict["filledValue"] = filled_value
        if id is not UNSET:
            field_dict["id"] = id
        if limit_price is not UNSET:
            field_dict["limitPrice"] = limit_price
        if ordered_quantity is not UNSET:
            field_dict["orderedQuantity"] = ordered_quantity
        if ordered_value is not UNSET:
            field_dict["orderedValue"] = ordered_value
        if parent_order is not UNSET:
            field_dict["parentOrder"] = parent_order
        if status is not UNSET:
            field_dict["status"] = status
        if stop_price is not UNSET:
            field_dict["stopPrice"] = stop_price
        if taxes is not UNSET:
            field_dict["taxes"] = taxes
        if ticker is not UNSET:
            field_dict["ticker"] = ticker
        if time_validity is not UNSET:
            field_dict["timeValidity"] = time_validity
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.tax import Tax

        d = src_dict.copy()
        _date_created = d.pop("dateCreated", UNSET)
        date_created: Union[Unset, datetime.datetime]
        if isinstance(_date_created, Unset):
            date_created = UNSET
        else:
            date_created = isoparse(_date_created)

        _date_executed = d.pop("dateExecuted", UNSET)
        date_executed: Union[Unset, datetime.datetime]
        if isinstance(_date_executed, Unset):
            date_executed = UNSET
        else:
            date_executed = isoparse(_date_executed)

        _date_modified = d.pop("dateModified", UNSET)
        date_modified: Union[Unset, datetime.datetime]
        if isinstance(_date_modified, Unset):
            date_modified = UNSET
        else:
            date_modified = isoparse(_date_modified)

        _executor = d.pop("executor", UNSET)
        executor: Union[Unset, HistoricalOrderExecutor]
        if isinstance(_executor, Unset):
            executor = UNSET
        else:
            executor = HistoricalOrderExecutor(_executor)

        fill_cost = d.pop("fillCost", UNSET)

        fill_id = d.pop("fillId", UNSET)

        fill_price = d.pop("fillPrice", UNSET)

        fill_result = d.pop("fillResult", UNSET)

        _fill_type = d.pop("fillType", UNSET)
        fill_type: Union[Unset, HistoricalOrderFillType]
        if isinstance(_fill_type, Unset):
            fill_type = UNSET
        else:
            fill_type = HistoricalOrderFillType(_fill_type)

        filled_quantity = d.pop("filledQuantity", UNSET)

        filled_value = d.pop("filledValue", UNSET)

        id = d.pop("id", UNSET)

        limit_price = d.pop("limitPrice", UNSET)

        ordered_quantity = d.pop("orderedQuantity", UNSET)

        ordered_value = d.pop("orderedValue", UNSET)

        parent_order = d.pop("parentOrder", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, HistoricalOrderStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = HistoricalOrderStatus(_status)

        stop_price = d.pop("stopPrice", UNSET)

        taxes = []
        _taxes = d.pop("taxes", UNSET)
        for taxes_item_data in _taxes or []:
            taxes_item = Tax.from_dict(taxes_item_data)

            taxes.append(taxes_item)

        ticker = d.pop("ticker", UNSET)

        _time_validity = d.pop("timeValidity", UNSET)
        time_validity: Union[Unset, HistoricalOrderTimeValidity]
        if isinstance(_time_validity, Unset):
            time_validity = UNSET
        else:
            time_validity = HistoricalOrderTimeValidity(_time_validity)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, HistoricalOrderType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = HistoricalOrderType(_type_)

        historical_order = cls(
            date_created=date_created,
            date_executed=date_executed,
            date_modified=date_modified,
            executor=executor,
            fill_cost=fill_cost,
            fill_id=fill_id,
            fill_price=fill_price,
            fill_result=fill_result,
            fill_type=fill_type,
            filled_quantity=filled_quantity,
            filled_value=filled_value,
            id=id,
            limit_price=limit_price,
            ordered_quantity=ordered_quantity,
            ordered_value=ordered_value,
            parent_order=parent_order,
            status=status,
            stop_price=stop_price,
            taxes=taxes,
            ticker=ticker,
            time_validity=time_validity,
            type_=type_,
        )

        historical_order.additional_properties = d
        return historical_order

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
