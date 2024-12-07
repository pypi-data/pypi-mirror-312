from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sushi_report_header import SUSHIReportHeader


T = TypeVar("T", bound="SUSHIReportList")


@_attrs_define
class SUSHIReportList:
    """list wrapper of reports

    Attributes:
        id (Union[Unset, str]): report id. Example: sciencedb-2022-01.
        report_header (Union[Unset, SUSHIReportHeader]): Generalized report header that defines the requested report,
            the requestor, the customer, filters applied, reportAttributes applied and any exceptions.
    """

    id: Union[Unset, str] = UNSET
    report_header: Union[Unset, "SUSHIReportHeader"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        report_header: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.report_header, Unset):
            report_header = self.report_header.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if report_header is not UNSET:
            field_dict["report-header"] = report_header

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.sushi_report_header import SUSHIReportHeader

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _report_header = d.pop("report-header", UNSET)
        report_header: Union[Unset, SUSHIReportHeader]
        if isinstance(_report_header, Unset):
            report_header = UNSET
        else:
            report_header = SUSHIReportHeader.from_dict(_report_header)

        sushi_report_list = cls(
            id=id,
            report_header=report_header,
        )

        sushi_report_list.additional_properties = d
        return sushi_report_list

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
