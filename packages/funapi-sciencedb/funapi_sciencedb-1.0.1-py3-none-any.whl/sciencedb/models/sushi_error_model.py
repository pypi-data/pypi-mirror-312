from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sushi_error_model_severity import SUSHIErrorModelSeverity
from ..types import UNSET, Unset

T = TypeVar("T", bound="SUSHIErrorModel")


@_attrs_define
class SUSHIErrorModel:
    """Generalized format for presenting errors and exceptions.

    Attributes:
        code (int): Error number. See table of error. Example: 3040.
        message (str): Text describing the error. Example: Partial Data Returned..
        severity (SUSHIErrorModelSeverity): Severity of the error. Example: Warning.
        data (Union[Unset, str]): Additional data provided by the server to clarify the error. Example: Usage data has
            not been processed for all requested months..
        help_url (Union[Unset, str]): URL describing error details.
    """

    code: int
    message: str
    severity: SUSHIErrorModelSeverity
    data: Union[Unset, str] = UNSET
    help_url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code = self.code

        message = self.message

        severity = self.severity.value

        data = self.data

        help_url = self.help_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "Code": code,
                "Message": message,
                "Severity": severity,
            }
        )
        if data is not UNSET:
            field_dict["Data"] = data
        if help_url is not UNSET:
            field_dict["Help_URL"] = help_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        code = d.pop("Code")

        message = d.pop("Message")

        severity = SUSHIErrorModelSeverity(d.pop("Severity"))

        data = d.pop("Data", UNSET)

        help_url = d.pop("Help_URL", UNSET)

        sushi_error_model = cls(
            code=code,
            message=message,
            severity=severity,
            data=data,
            help_url=help_url,
        )

        sushi_error_model.additional_properties = d
        return sushi_error_model

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
