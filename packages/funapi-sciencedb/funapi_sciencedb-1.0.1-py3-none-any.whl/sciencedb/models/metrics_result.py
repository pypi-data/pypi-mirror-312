from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MetricsResult")


@_attrs_define
class MetricsResult:
    """wrapper of records of '/harvest' and '/search' and '/metrics' API

    Attributes:
        title_zh (Union[Unset, str]): Chinese title of dataset
        title_en (Union[Unset, str]): English title of dataset
        visit (Union[Unset, int]): Number of data set accesses
        download (Union[Unset, int]): Number of data set downloads
        ref_papers (Union[Unset, int]): The number of papers cited in the dataset
    """

    title_zh: Union[Unset, str] = UNSET
    title_en: Union[Unset, str] = UNSET
    visit: Union[Unset, int] = UNSET
    download: Union[Unset, int] = UNSET
    ref_papers: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        title_zh = self.title_zh

        title_en = self.title_en

        visit = self.visit

        download = self.download

        ref_papers = self.ref_papers

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if title_zh is not UNSET:
            field_dict["titleZh"] = title_zh
        if title_en is not UNSET:
            field_dict["titleEn"] = title_en
        if visit is not UNSET:
            field_dict["visit"] = visit
        if download is not UNSET:
            field_dict["download"] = download
        if ref_papers is not UNSET:
            field_dict["refPapers"] = ref_papers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        title_zh = d.pop("titleZh", UNSET)

        title_en = d.pop("titleEn", UNSET)

        visit = d.pop("visit", UNSET)

        download = d.pop("download", UNSET)

        ref_papers = d.pop("refPapers", UNSET)

        metrics_result = cls(
            title_zh=title_zh,
            title_en=title_en,
            visit=visit,
            download=download,
            ref_papers=ref_papers,
        )

        metrics_result.additional_properties = d
        return metrics_result

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
