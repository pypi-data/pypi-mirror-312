from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.counter_dataset_usage import COUNTERDatasetUsage
    from ..models.sushi_report_header import SUSHIReportHeader


T = TypeVar("T", bound="COUNTERDatasetReport")


@_attrs_define
class COUNTERDatasetReport:
    """Describes the formatting needs for the COUNTER Dataset Report. Response may include the Report_Header (optional),
    Report_Datasets (usage stats).

        Attributes:
            id (Union[Unset, str]): id of report.
            report_header (Union[Unset, SUSHIReportHeader]): Generalized report header that defines the requested report,
                the requestor, the customer, filters applied, reportAttributes applied and any exceptions.
            report_datasets (Union[Unset, List['COUNTERDatasetUsage']]): list of datasets .
    """

    id: Union[Unset, str] = UNSET
    report_header: Union[Unset, "SUSHIReportHeader"] = UNSET
    report_datasets: Union[Unset, List["COUNTERDatasetUsage"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        report_header: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.report_header, Unset):
            report_header = self.report_header.to_dict()

        report_datasets: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.report_datasets, Unset):
            report_datasets = []
            for report_datasets_item_data in self.report_datasets:
                report_datasets_item = report_datasets_item_data.to_dict()
                report_datasets.append(report_datasets_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if report_header is not UNSET:
            field_dict["report-header"] = report_header
        if report_datasets is not UNSET:
            field_dict["report-datasets"] = report_datasets

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.counter_dataset_usage import COUNTERDatasetUsage
        from ..models.sushi_report_header import SUSHIReportHeader

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _report_header = d.pop("report-header", UNSET)
        report_header: Union[Unset, SUSHIReportHeader]
        if isinstance(_report_header, Unset):
            report_header = UNSET
        else:
            report_header = SUSHIReportHeader.from_dict(_report_header)

        report_datasets = []
        _report_datasets = d.pop("report-datasets", UNSET)
        for report_datasets_item_data in _report_datasets or []:
            report_datasets_item = COUNTERDatasetUsage.from_dict(
                report_datasets_item_data
            )

            report_datasets.append(report_datasets_item)

        counter_dataset_report = cls(
            id=id,
            report_header=report_header,
            report_datasets=report_datasets,
        )

        counter_dataset_report.additional_properties = d
        return counter_dataset_report

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
