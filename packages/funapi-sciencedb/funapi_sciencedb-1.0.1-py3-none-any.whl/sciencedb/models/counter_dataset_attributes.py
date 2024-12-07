from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.counter_dataset_attributes_type import COUNTERDatasetAttributesType

T = TypeVar("T", bound="COUNTERDatasetAttributes")


@_attrs_define
class COUNTERDatasetAttributes:
    """
    Attributes:
        type (COUNTERDatasetAttributesType): Item attribute types are defined by NISO Journal Article Version and other
            work... Example: dataset-version.
        value (str): Value of the item attribute Example: VoR.
    """

    type: COUNTERDatasetAttributesType
    value: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "Type": type,
                "Value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = COUNTERDatasetAttributesType(d.pop("Type"))

        value = d.pop("Value")

        counter_dataset_attributes = cls(
            type=type,
            value=value,
        )

        counter_dataset_attributes.additional_properties = d
        return counter_dataset_attributes

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
