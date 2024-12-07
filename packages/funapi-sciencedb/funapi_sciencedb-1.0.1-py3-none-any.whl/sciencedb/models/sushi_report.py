from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.counter_dataset_report import COUNTERDatasetReport


T = TypeVar("T", bound="SUSHIReport")


@_attrs_define
class SUSHIReport:
    """
    Attributes:
        report (Union[Unset, COUNTERDatasetReport]): Describes the formatting needs for the COUNTER Dataset Report.
            Response may include the Report_Header (optional), Report_Datasets (usage stats).
    """

    report: Union[Unset, "COUNTERDatasetReport"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        report: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.report, Unset):
            report = self.report.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if report is not UNSET:
            field_dict["report"] = report

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.counter_dataset_report import COUNTERDatasetReport

        d = src_dict.copy()
        _report = d.pop("report", UNSET)
        report: Union[Unset, COUNTERDatasetReport]
        if isinstance(_report, Unset):
            report = UNSET
        else:
            report = COUNTERDatasetReport.from_dict(_report)

        sushi_report = cls(
            report=report,
        )

        sushi_report.additional_properties = d
        return sushi_report

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
