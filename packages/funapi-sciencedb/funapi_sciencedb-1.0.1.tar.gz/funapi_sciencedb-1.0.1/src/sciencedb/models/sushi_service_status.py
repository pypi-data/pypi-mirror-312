from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sushi_service_status_alerts_item import SUSHIServiceStatusAlertsItem


T = TypeVar("T", bound="SUSHIServiceStatus")


@_attrs_define
class SUSHIServiceStatus:
    """
    Attributes:
        service_active (bool): Indicator if the service is currently able to deliver reports. Example: True.
        alerts (Union[Unset, List['SUSHIServiceStatusAlertsItem']]): Any alerts related to service interuptions and
            status.
        description (Union[Unset, str]): Description of the service. Example: COUNTER Research Data Usage Reports for
            the UK Data Service - ReShare..
        note (Union[Unset, str]): A general note about the service. Example: A given customer can request a maximum of 5
            requests per day for a given report.
        registry_url (Union[Unset, str]): If available, the URL separate registry with additional information about the
            service. Example: https://www.projectcounter.org/counter-user/ebsco-database/.
    """

    service_active: bool
    alerts: Union[Unset, List["SUSHIServiceStatusAlertsItem"]] = UNSET
    description: Union[Unset, str] = UNSET
    note: Union[Unset, str] = UNSET
    registry_url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        service_active = self.service_active

        alerts: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.alerts, Unset):
            alerts = []
            for alerts_item_data in self.alerts:
                alerts_item = alerts_item_data.to_dict()
                alerts.append(alerts_item)

        description = self.description

        note = self.note

        registry_url = self.registry_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ServiceActive": service_active,
            }
        )
        if alerts is not UNSET:
            field_dict["Alerts"] = alerts
        if description is not UNSET:
            field_dict["Description"] = description
        if note is not UNSET:
            field_dict["Note"] = note
        if registry_url is not UNSET:
            field_dict["RegistryURL"] = registry_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.sushi_service_status_alerts_item import (
            SUSHIServiceStatusAlertsItem,
        )

        d = src_dict.copy()
        service_active = d.pop("ServiceActive")

        alerts = []
        _alerts = d.pop("Alerts", UNSET)
        for alerts_item_data in _alerts or []:
            alerts_item = SUSHIServiceStatusAlertsItem.from_dict(alerts_item_data)

            alerts.append(alerts_item)

        description = d.pop("Description", UNSET)

        note = d.pop("Note", UNSET)

        registry_url = d.pop("RegistryURL", UNSET)

        sushi_service_status = cls(
            service_active=service_active,
            alerts=alerts,
            description=description,
            note=note,
            registry_url=registry_url,
        )

        sushi_service_status.additional_properties = d
        return sushi_service_status

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
