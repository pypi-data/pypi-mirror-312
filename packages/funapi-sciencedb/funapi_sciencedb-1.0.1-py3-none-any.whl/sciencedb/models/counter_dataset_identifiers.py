from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.counter_dataset_identifiers_type import COUNTERDatasetIdentifiersType

T = TypeVar("T", bound="COUNTERDatasetIdentifiers")


@_attrs_define
class COUNTERDatasetIdentifiers:
    """
    Attributes:
        type (COUNTERDatasetIdentifiersType):  Example: doi.
        value (str): Value of the dataset identifier Example: 0931-865.
    """

    type: COUNTERDatasetIdentifiersType
    value: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = COUNTERDatasetIdentifiersType(d.pop("type"))

        value = d.pop("value")

        counter_dataset_identifiers = cls(
            type=type,
            value=value,
        )

        counter_dataset_identifiers.additional_properties = d
        return counter_dataset_identifiers

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
