from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchRecord")


@_attrs_define
class SearchRecord:
    """dataset's brief record of '/harvest' and '/search' API

    Attributes:
        clicks (Union[Unset, int]):
        language (Union[Unset, str]):
        reference_number (Union[Unset, int]):
        title (Union[Unset, str]): dataset's title
        introduction (Union[Unset, str]): dataset's introduction
        keyword (Union[Unset, str]): dataset's keywords, put together in quotation marks Example: kw_1;kw_2;kw_3.
        author (Union[Unset, str]): dataset's authors, put together in quotation marks Example: 2021-08-11 18:20:51.
        publish_date (Union[Unset, str]): publish date in ScienceDB Example: author_1;author_2;author_3.
        taxonomy (Union[Unset, str]): taxonomy in ScienceDB,put together in quotation marks,format is 'code'-'taxonomy'
            Example: 170-Earth science;00-Others.
        year (Union[Unset, str]): publish year in ScienceDB Example: 2021.
        doi (Union[Unset, str]): dataset's doi Example: 10.11922/sciencedb.00101.
    """

    clicks: Union[Unset, int] = UNSET
    language: Union[Unset, str] = UNSET
    reference_number: Union[Unset, int] = UNSET
    title: Union[Unset, str] = UNSET
    introduction: Union[Unset, str] = UNSET
    keyword: Union[Unset, str] = UNSET
    author: Union[Unset, str] = UNSET
    publish_date: Union[Unset, str] = UNSET
    taxonomy: Union[Unset, str] = UNSET
    year: Union[Unset, str] = UNSET
    doi: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        clicks = self.clicks

        language = self.language

        reference_number = self.reference_number

        title = self.title

        introduction = self.introduction

        keyword = self.keyword

        author = self.author

        publish_date = self.publish_date

        taxonomy = self.taxonomy

        year = self.year

        doi = self.doi

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if clicks is not UNSET:
            field_dict["clicks"] = clicks
        if language is not UNSET:
            field_dict["language"] = language
        if reference_number is not UNSET:
            field_dict["referenceNumber"] = reference_number
        if title is not UNSET:
            field_dict["title"] = title
        if introduction is not UNSET:
            field_dict["introduction"] = introduction
        if keyword is not UNSET:
            field_dict["keyword"] = keyword
        if author is not UNSET:
            field_dict["author"] = author
        if publish_date is not UNSET:
            field_dict["publishDate"] = publish_date
        if taxonomy is not UNSET:
            field_dict["taxonomy"] = taxonomy
        if year is not UNSET:
            field_dict["year"] = year
        if doi is not UNSET:
            field_dict["doi"] = doi

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        clicks = d.pop("clicks", UNSET)

        language = d.pop("language", UNSET)

        reference_number = d.pop("referenceNumber", UNSET)

        title = d.pop("title", UNSET)

        introduction = d.pop("introduction", UNSET)

        keyword = d.pop("keyword", UNSET)

        author = d.pop("author", UNSET)

        publish_date = d.pop("publishDate", UNSET)

        taxonomy = d.pop("taxonomy", UNSET)

        year = d.pop("year", UNSET)

        doi = d.pop("doi", UNSET)

        search_record = cls(
            clicks=clicks,
            language=language,
            reference_number=reference_number,
            title=title,
            introduction=introduction,
            keyword=keyword,
            author=author,
            publish_date=publish_date,
            taxonomy=taxonomy,
            year=year,
            doi=doi,
        )

        search_record.additional_properties = d
        return search_record

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
