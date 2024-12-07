from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.sushi_report_page import SUSHIReportPage
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    pagenumber: Union[Unset, int] = 1,
    pagesize: Union[Unset, int] = 10,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["page[number]"] = pagenumber

    params["page[size]"] = pagesize

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/reports",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[SUSHIReportPage]:
    if response.status_code == 200:
        response_200 = SUSHIReportPage.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SUSHIReportPage]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    pagenumber: Union[Unset, int] = 1,
    pagesize: Union[Unset, int] = 10,
) -> Response[SUSHIReportPage]:
    """getReports

     This resource returns a list of reports supported by the API for a given application.

    Args:
        pagenumber (Union[Unset, int]):  Default: 1.
        pagesize (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SUSHIReportPage]
    """

    kwargs = _get_kwargs(
        pagenumber=pagenumber,
        pagesize=pagesize,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    pagenumber: Union[Unset, int] = 1,
    pagesize: Union[Unset, int] = 10,
) -> Optional[SUSHIReportPage]:
    """getReports

     This resource returns a list of reports supported by the API for a given application.

    Args:
        pagenumber (Union[Unset, int]):  Default: 1.
        pagesize (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SUSHIReportPage
    """

    return sync_detailed(
        client=client,
        pagenumber=pagenumber,
        pagesize=pagesize,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    pagenumber: Union[Unset, int] = 1,
    pagesize: Union[Unset, int] = 10,
) -> Response[SUSHIReportPage]:
    """getReports

     This resource returns a list of reports supported by the API for a given application.

    Args:
        pagenumber (Union[Unset, int]):  Default: 1.
        pagesize (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SUSHIReportPage]
    """

    kwargs = _get_kwargs(
        pagenumber=pagenumber,
        pagesize=pagesize,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    pagenumber: Union[Unset, int] = 1,
    pagesize: Union[Unset, int] = 10,
) -> Optional[SUSHIReportPage]:
    """getReports

     This resource returns a list of reports supported by the API for a given application.

    Args:
        pagenumber (Union[Unset, int]):  Default: 1.
        pagesize (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SUSHIReportPage
    """

    return (
        await asyncio_detailed(
            client=client,
            pagenumber=pagenumber,
            pagesize=pagesize,
        )
    ).parsed
