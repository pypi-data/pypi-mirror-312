from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.search_record import SearchRecord


T = TypeVar("T", bound="SearchResult")


@_attrs_define
class SearchResult:
    """wrapper of records of '/harvest' and '/search' API

    Attributes:
        page_no (Union[Unset, int]):
        page_size (Union[Unset, int]):
        total_pages (Union[Unset, int]): total pages of records
        total_elements (Union[Unset, int]): total number of records
        recommend_data (Union[Unset, List['SearchRecord']]): the list of current page records
    """

    page_no: Union[Unset, int] = UNSET
    page_size: Union[Unset, int] = UNSET
    total_pages: Union[Unset, int] = UNSET
    total_elements: Union[Unset, int] = UNSET
    recommend_data: Union[Unset, List["SearchRecord"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        page_no = self.page_no

        page_size = self.page_size

        total_pages = self.total_pages

        total_elements = self.total_elements

        recommend_data: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.recommend_data, Unset):
            recommend_data = []
            for recommend_data_item_data in self.recommend_data:
                recommend_data_item = recommend_data_item_data.to_dict()
                recommend_data.append(recommend_data_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if page_no is not UNSET:
            field_dict["pageNo"] = page_no
        if page_size is not UNSET:
            field_dict["pageSize"] = page_size
        if total_pages is not UNSET:
            field_dict["totalPages"] = total_pages
        if total_elements is not UNSET:
            field_dict["totalElements"] = total_elements
        if recommend_data is not UNSET:
            field_dict["recommendData"] = recommend_data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.search_record import SearchRecord

        d = src_dict.copy()
        page_no = d.pop("pageNo", UNSET)

        page_size = d.pop("pageSize", UNSET)

        total_pages = d.pop("totalPages", UNSET)

        total_elements = d.pop("totalElements", UNSET)

        recommend_data = []
        _recommend_data = d.pop("recommendData", UNSET)
        for recommend_data_item_data in _recommend_data or []:
            recommend_data_item = SearchRecord.from_dict(recommend_data_item_data)

            recommend_data.append(recommend_data_item)

        search_result = cls(
            page_no=page_no,
            page_size=page_size,
            total_pages=total_pages,
            total_elements=total_elements,
            recommend_data=recommend_data,
        )

        search_result.additional_properties = d
        return search_result

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
