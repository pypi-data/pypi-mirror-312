from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metrics_result import MetricsResult


T = TypeVar("T", bound="APIResultMetricsResult")


@_attrs_define
class APIResultMetricsResult:
    """the api result model

    Attributes:
        code (Union[Unset, int]): 20000 means success, other means error
        message (Union[Unset, str]): code's description in Chinese
        get_message_en (Union[Unset, str]): code's description in English
        data (Union[Unset, MetricsResult]): wrapper of records of '/harvest' and '/search' and '/metrics' API
    """

    code: Union[Unset, int] = UNSET
    message: Union[Unset, str] = UNSET
    get_message_en: Union[Unset, str] = UNSET
    data: Union[Unset, "MetricsResult"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code = self.code

        message = self.message

        get_message_en = self.get_message_en

        data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if code is not UNSET:
            field_dict["code"] = code
        if message is not UNSET:
            field_dict["message"] = message
        if get_message_en is not UNSET:
            field_dict["getMessageEn"] = get_message_en
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.metrics_result import MetricsResult

        d = src_dict.copy()
        code = d.pop("code", UNSET)

        message = d.pop("message", UNSET)

        get_message_en = d.pop("getMessageEn", UNSET)

        _data = d.pop("data", UNSET)
        data: Union[Unset, MetricsResult]
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = MetricsResult.from_dict(_data)

        api_result_metrics_result = cls(
            code=code,
            message=message,
            get_message_en=get_message_en,
            data=data,
        )

        api_result_metrics_result.additional_properties = d
        return api_result_metrics_result

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
