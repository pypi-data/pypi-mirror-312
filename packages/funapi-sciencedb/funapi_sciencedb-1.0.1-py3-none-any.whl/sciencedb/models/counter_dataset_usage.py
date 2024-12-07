from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.counter_dataset_usage_data_type import COUNTERDatasetUsageDataType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.counter_dataset_attributes import COUNTERDatasetAttributes
    from ..models.counter_dataset_contributors import COUNTERDatasetContributors
    from ..models.counter_dataset_dates import COUNTERDatasetDates
    from ..models.counter_dataset_identifiers import COUNTERDatasetIdentifiers
    from ..models.counter_dataset_performance import COUNTERDatasetPerformance
    from ..models.counter_publisher_identifiers import COUNTERPublisherIdentifiers


T = TypeVar("T", bound="COUNTERDatasetUsage")


@_attrs_define
class COUNTERDatasetUsage:
    """Defines the output for the Report_Datasets being returned in a Dataset Report.

    Attributes:
        data_type (COUNTERDatasetUsageDataType): Nature of the dataset being reported. Example: Dataset.
        dataset_title (str): Name of the dataset being reported. Example: Lake Erie Fish Community Data.
        performance (List['COUNTERDatasetPerformance']): The usage data related to the report dataset
        platform (str): Name of the platform Example: Science Data Bank.
        publisher (str): Name of publisher of the dataset Example: Science Data Bank.
        publisher_id (List['COUNTERPublisherIdentifiers']): The identifier for the publisher.
        dataset_attributes (Union[Unset, List['COUNTERDatasetAttributes']]): Other attributes related related to the
            dataset.
        dataset_contributors (Union[Unset, List['COUNTERDatasetContributors']]): The identifier for contributor (i.e.
            creator) of the dataset.
        dataset_dates (Union[Unset, List['COUNTERDatasetDates']]): Publication or other date(s)related to the dataset.
        dataset_id (Union[Unset, List['COUNTERDatasetIdentifiers']]): The identifier for the report dataset
        yop (Union[Unset, str]): Year of publication in the format of 'yyyy'. Use '0001' for unknown and '9999' for
            articles in press. Example: 2010.
    """

    data_type: COUNTERDatasetUsageDataType
    dataset_title: str
    performance: List["COUNTERDatasetPerformance"]
    platform: str
    publisher: str
    publisher_id: List["COUNTERPublisherIdentifiers"]
    dataset_attributes: Union[Unset, List["COUNTERDatasetAttributes"]] = UNSET
    dataset_contributors: Union[Unset, List["COUNTERDatasetContributors"]] = UNSET
    dataset_dates: Union[Unset, List["COUNTERDatasetDates"]] = UNSET
    dataset_id: Union[Unset, List["COUNTERDatasetIdentifiers"]] = UNSET
    yop: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data_type = self.data_type.value

        dataset_title = self.dataset_title

        performance = []
        for performance_item_data in self.performance:
            performance_item = performance_item_data.to_dict()
            performance.append(performance_item)

        platform = self.platform

        publisher = self.publisher

        publisher_id = []
        for publisher_id_item_data in self.publisher_id:
            publisher_id_item = publisher_id_item_data.to_dict()
            publisher_id.append(publisher_id_item)

        dataset_attributes: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.dataset_attributes, Unset):
            dataset_attributes = []
            for dataset_attributes_item_data in self.dataset_attributes:
                dataset_attributes_item = dataset_attributes_item_data.to_dict()
                dataset_attributes.append(dataset_attributes_item)

        dataset_contributors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.dataset_contributors, Unset):
            dataset_contributors = []
            for dataset_contributors_item_data in self.dataset_contributors:
                dataset_contributors_item = dataset_contributors_item_data.to_dict()
                dataset_contributors.append(dataset_contributors_item)

        dataset_dates: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.dataset_dates, Unset):
            dataset_dates = []
            for dataset_dates_item_data in self.dataset_dates:
                dataset_dates_item = dataset_dates_item_data.to_dict()
                dataset_dates.append(dataset_dates_item)

        dataset_id: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.dataset_id, Unset):
            dataset_id = []
            for dataset_id_item_data in self.dataset_id:
                dataset_id_item = dataset_id_item_data.to_dict()
                dataset_id.append(dataset_id_item)

        yop = self.yop

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data-type": data_type,
                "dataset-title": dataset_title,
                "performance": performance,
                "platform": platform,
                "publisher": publisher,
                "publisher-id": publisher_id,
            }
        )
        if dataset_attributes is not UNSET:
            field_dict["dataset-attributes"] = dataset_attributes
        if dataset_contributors is not UNSET:
            field_dict["dataset-contributors"] = dataset_contributors
        if dataset_dates is not UNSET:
            field_dict["dataset-dates"] = dataset_dates
        if dataset_id is not UNSET:
            field_dict["dataset-id"] = dataset_id
        if yop is not UNSET:
            field_dict["yop"] = yop

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.counter_dataset_attributes import COUNTERDatasetAttributes
        from ..models.counter_dataset_contributors import COUNTERDatasetContributors
        from ..models.counter_dataset_dates import COUNTERDatasetDates
        from ..models.counter_dataset_identifiers import COUNTERDatasetIdentifiers
        from ..models.counter_dataset_performance import COUNTERDatasetPerformance
        from ..models.counter_publisher_identifiers import COUNTERPublisherIdentifiers

        d = src_dict.copy()
        data_type = COUNTERDatasetUsageDataType(d.pop("data-type"))

        dataset_title = d.pop("dataset-title")

        performance = []
        _performance = d.pop("performance")
        for performance_item_data in _performance:
            performance_item = COUNTERDatasetPerformance.from_dict(
                performance_item_data
            )

            performance.append(performance_item)

        platform = d.pop("platform")

        publisher = d.pop("publisher")

        publisher_id = []
        _publisher_id = d.pop("publisher-id")
        for publisher_id_item_data in _publisher_id:
            publisher_id_item = COUNTERPublisherIdentifiers.from_dict(
                publisher_id_item_data
            )

            publisher_id.append(publisher_id_item)

        dataset_attributes = []
        _dataset_attributes = d.pop("dataset-attributes", UNSET)
        for dataset_attributes_item_data in _dataset_attributes or []:
            dataset_attributes_item = COUNTERDatasetAttributes.from_dict(
                dataset_attributes_item_data
            )

            dataset_attributes.append(dataset_attributes_item)

        dataset_contributors = []
        _dataset_contributors = d.pop("dataset-contributors", UNSET)
        for dataset_contributors_item_data in _dataset_contributors or []:
            dataset_contributors_item = COUNTERDatasetContributors.from_dict(
                dataset_contributors_item_data
            )

            dataset_contributors.append(dataset_contributors_item)

        dataset_dates = []
        _dataset_dates = d.pop("dataset-dates", UNSET)
        for dataset_dates_item_data in _dataset_dates or []:
            dataset_dates_item = COUNTERDatasetDates.from_dict(dataset_dates_item_data)

            dataset_dates.append(dataset_dates_item)

        dataset_id = []
        _dataset_id = d.pop("dataset-id", UNSET)
        for dataset_id_item_data in _dataset_id or []:
            dataset_id_item = COUNTERDatasetIdentifiers.from_dict(dataset_id_item_data)

            dataset_id.append(dataset_id_item)

        yop = d.pop("yop", UNSET)

        counter_dataset_usage = cls(
            data_type=data_type,
            dataset_title=dataset_title,
            performance=performance,
            platform=platform,
            publisher=publisher,
            publisher_id=publisher_id,
            dataset_attributes=dataset_attributes,
            dataset_contributors=dataset_contributors,
            dataset_dates=dataset_dates,
            dataset_id=dataset_id,
            yop=yop,
        )

        counter_dataset_usage.additional_properties = d
        return counter_dataset_usage

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
