from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SUSHIPageMeta")


@_attrs_define
class SUSHIPageMeta:
    """page wrapper of reports

    Attributes:
        page (Union[Unset, int]): page number. Example: 1.
        total (Union[Unset, int]): count of reports. Example: 100.
        total_pages (Union[Unset, int]): count of pages. Example: 10.
    """

    page: Union[Unset, int] = UNSET
    total: Union[Unset, int] = UNSET
    total_pages: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        page = self.page

        total = self.total

        total_pages = self.total_pages

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if page is not UNSET:
            field_dict["page"] = page
        if total is not UNSET:
            field_dict["total"] = total
        if total_pages is not UNSET:
            field_dict["totalPages"] = total_pages

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        page = d.pop("page", UNSET)

        total = d.pop("total", UNSET)

        total_pages = d.pop("totalPages", UNSET)

        sushi_page_meta = cls(
            page=page,
            total=total,
            total_pages=total_pages,
        )

        sushi_page_meta.additional_properties = d
        return sushi_page_meta

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
