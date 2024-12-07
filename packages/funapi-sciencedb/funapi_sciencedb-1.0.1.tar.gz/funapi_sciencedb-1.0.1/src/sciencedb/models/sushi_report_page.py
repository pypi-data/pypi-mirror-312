from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sushi_page_meta import SUSHIPageMeta
    from ..models.sushi_report_list import SUSHIReportList


T = TypeVar("T", bound="SUSHIReportPage")


@_attrs_define
class SUSHIReportPage:
    """page wrapper of reports

    Attributes:
        reports (Union[Unset, List['SUSHIReportList']]): list of reports
        meta (Union[Unset, SUSHIPageMeta]): page wrapper of reports
    """

    reports: Union[Unset, List["SUSHIReportList"]] = UNSET
    meta: Union[Unset, "SUSHIPageMeta"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        reports: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.reports, Unset):
            reports = []
            for reports_item_data in self.reports:
                reports_item = reports_item_data.to_dict()
                reports.append(reports_item)

        meta: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if reports is not UNSET:
            field_dict["reports"] = reports
        if meta is not UNSET:
            field_dict["meta"] = meta

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.sushi_page_meta import SUSHIPageMeta
        from ..models.sushi_report_list import SUSHIReportList

        d = src_dict.copy()
        reports = []
        _reports = d.pop("reports", UNSET)
        for reports_item_data in _reports or []:
            reports_item = SUSHIReportList.from_dict(reports_item_data)

            reports.append(reports_item)

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, SUSHIPageMeta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = SUSHIPageMeta.from_dict(_meta)

        sushi_report_page = cls(
            reports=reports,
            meta=meta,
        )

        sushi_report_page.additional_properties = d
        return sushi_report_page

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
