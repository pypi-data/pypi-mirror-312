import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sushi_error_model import SUSHIErrorModel
    from ..models.sushi_report_header_report_attributes_item import (
        SUSHIReportHeaderReportAttributesItem,
    )
    from ..models.sushi_report_header_report_filters_item import (
        SUSHIReportHeaderReportFiltersItem,
    )


T = TypeVar("T", bound="SUSHIReportHeader")


@_attrs_define
class SUSHIReportHeader:
    """Generalized report header that defines the requested report, the requestor, the customer, filters applied,
    reportAttributes applied and any exceptions.

        Attributes:
            release (str): The release or version of the report. Example: RD1.
            report_id (str): The report ID or code or shortname. Typically this will be the same code provided in the Report
                parameter of the request. Example: DSR.
            report_name (str): The long name of the report. Example: Dataset Report.
            created (Union[Unset, datetime.datetime]): Time the report was prepared
            created_by (Union[Unset, str]): Name of the organization producing the report. Example: Science Data Bank.
            exceptions (Union[Unset, List['SUSHIErrorModel']]): Series of exceptions encounted when preparing the report.
            report_attributes (Union[Unset, List['SUSHIReportHeaderReportAttributesItem']]): Zero or more additional
                attributes applied to the report. Attributes inform the level of detail in the report.
            report_filters (Union[Unset, List['SUSHIReportHeaderReportFiltersItem']]): Zero or more report filters used for
                this report.  Typically  reflect filters provided on the Request.  Filters limit the data to be reported on.
    """

    release: str
    report_id: str
    report_name: str
    created: Union[Unset, datetime.datetime] = UNSET
    created_by: Union[Unset, str] = UNSET
    exceptions: Union[Unset, List["SUSHIErrorModel"]] = UNSET
    report_attributes: Union[Unset, List["SUSHIReportHeaderReportAttributesItem"]] = (
        UNSET
    )
    report_filters: Union[Unset, List["SUSHIReportHeaderReportFiltersItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        release = self.release

        report_id = self.report_id

        report_name = self.report_name

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        created_by = self.created_by

        exceptions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.exceptions, Unset):
            exceptions = []
            for exceptions_item_data in self.exceptions:
                exceptions_item = exceptions_item_data.to_dict()
                exceptions.append(exceptions_item)

        report_attributes: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.report_attributes, Unset):
            report_attributes = []
            for report_attributes_item_data in self.report_attributes:
                report_attributes_item = report_attributes_item_data.to_dict()
                report_attributes.append(report_attributes_item)

        report_filters: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.report_filters, Unset):
            report_filters = []
            for report_filters_item_data in self.report_filters:
                report_filters_item = report_filters_item_data.to_dict()
                report_filters.append(report_filters_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "release": release,
                "report-id": report_id,
                "report-name": report_name,
            }
        )
        if created is not UNSET:
            field_dict["created"] = created
        if created_by is not UNSET:
            field_dict["created-by"] = created_by
        if exceptions is not UNSET:
            field_dict["exceptions"] = exceptions
        if report_attributes is not UNSET:
            field_dict["report-attributes"] = report_attributes
        if report_filters is not UNSET:
            field_dict["report-filters"] = report_filters

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.sushi_error_model import SUSHIErrorModel
        from ..models.sushi_report_header_report_attributes_item import (
            SUSHIReportHeaderReportAttributesItem,
        )
        from ..models.sushi_report_header_report_filters_item import (
            SUSHIReportHeaderReportFiltersItem,
        )

        d = src_dict.copy()
        release = d.pop("release")

        report_id = d.pop("report-id")

        report_name = d.pop("report-name")

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        created_by = d.pop("created-by", UNSET)

        exceptions = []
        _exceptions = d.pop("exceptions", UNSET)
        for exceptions_item_data in _exceptions or []:
            exceptions_item = SUSHIErrorModel.from_dict(exceptions_item_data)

            exceptions.append(exceptions_item)

        report_attributes = []
        _report_attributes = d.pop("report-attributes", UNSET)
        for report_attributes_item_data in _report_attributes or []:
            report_attributes_item = SUSHIReportHeaderReportAttributesItem.from_dict(
                report_attributes_item_data
            )

            report_attributes.append(report_attributes_item)

        report_filters = []
        _report_filters = d.pop("report-filters", UNSET)
        for report_filters_item_data in _report_filters or []:
            report_filters_item = SUSHIReportHeaderReportFiltersItem.from_dict(
                report_filters_item_data
            )

            report_filters.append(report_filters_item)

        sushi_report_header = cls(
            release=release,
            report_id=report_id,
            report_name=report_name,
            created=created,
            created_by=created_by,
            exceptions=exceptions,
            report_attributes=report_attributes,
            report_filters=report_filters,
        )

        sushi_report_header.additional_properties = d
        return sushi_report_header

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
