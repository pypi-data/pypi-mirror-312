import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="COUNTERDatasetPeriod")


@_attrs_define
class COUNTERDatasetPeriod:
    """
    Attributes:
        begin_date (Union[Unset, datetime.datetime]):
        end_date (Union[Unset, datetime.datetime]):
    """

    begin_date: Union[Unset, datetime.datetime] = UNSET
    end_date: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        begin_date: Union[Unset, str] = UNSET
        if not isinstance(self.begin_date, Unset):
            begin_date = self.begin_date.isoformat()

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if begin_date is not UNSET:
            field_dict["begin-date"] = begin_date
        if end_date is not UNSET:
            field_dict["end-date"] = end_date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _begin_date = d.pop("begin-date", UNSET)
        begin_date: Union[Unset, datetime.datetime]
        if isinstance(_begin_date, Unset):
            begin_date = UNSET
        else:
            begin_date = isoparse(_begin_date)

        _end_date = d.pop("end-date", UNSET)
        end_date: Union[Unset, datetime.datetime]
        if isinstance(_end_date, Unset):
            end_date = UNSET
        else:
            end_date = isoparse(_end_date)

        counter_dataset_period = cls(
            begin_date=begin_date,
            end_date=end_date,
        )

        counter_dataset_period.additional_properties = d
        return counter_dataset_period

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
