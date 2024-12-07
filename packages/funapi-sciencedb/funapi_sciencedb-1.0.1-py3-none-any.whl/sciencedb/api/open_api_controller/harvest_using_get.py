from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_search_result import APIResultSearchResult
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    end_time: Union[Unset, str] = "2099-01-01",
    page: Union[Unset, int] = 1,
    size: Union[Unset, int] = 10,
    start_time: Union[Unset, str] = "1970-01-01",
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["end_time"] = end_time

    params["page"] = page

    params["size"] = size

    params["start_time"] = start_time

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/harvest",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[APIResultSearchResult]:
    if response.status_code == 200:
        response_200 = APIResultSearchResult.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[APIResultSearchResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    end_time: Union[Unset, str] = "2099-01-01",
    page: Union[Unset, int] = 1,
    size: Union[Unset, int] = 10,
    start_time: Union[Unset, str] = "1970-01-01",
) -> Response[APIResultSearchResult]:
    """harvest dataset by dataset's publish time period(start_time and end_time)

     result is order by publish time desc

    Args:
        end_time (Union[Unset, str]):  Default: '2099-01-01'.
        page (Union[Unset, int]):  Default: 1.
        size (Union[Unset, int]):  Default: 10.
        start_time (Union[Unset, str]):  Default: '1970-01-01'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIResultSearchResult]
    """

    kwargs = _get_kwargs(
        end_time=end_time,
        page=page,
        size=size,
        start_time=start_time,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    end_time: Union[Unset, str] = "2099-01-01",
    page: Union[Unset, int] = 1,
    size: Union[Unset, int] = 10,
    start_time: Union[Unset, str] = "1970-01-01",
) -> Optional[APIResultSearchResult]:
    """harvest dataset by dataset's publish time period(start_time and end_time)

     result is order by publish time desc

    Args:
        end_time (Union[Unset, str]):  Default: '2099-01-01'.
        page (Union[Unset, int]):  Default: 1.
        size (Union[Unset, int]):  Default: 10.
        start_time (Union[Unset, str]):  Default: '1970-01-01'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIResultSearchResult
    """

    return sync_detailed(
        client=client,
        end_time=end_time,
        page=page,
        size=size,
        start_time=start_time,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    end_time: Union[Unset, str] = "2099-01-01",
    page: Union[Unset, int] = 1,
    size: Union[Unset, int] = 10,
    start_time: Union[Unset, str] = "1970-01-01",
) -> Response[APIResultSearchResult]:
    """harvest dataset by dataset's publish time period(start_time and end_time)

     result is order by publish time desc

    Args:
        end_time (Union[Unset, str]):  Default: '2099-01-01'.
        page (Union[Unset, int]):  Default: 1.
        size (Union[Unset, int]):  Default: 10.
        start_time (Union[Unset, str]):  Default: '1970-01-01'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIResultSearchResult]
    """

    kwargs = _get_kwargs(
        end_time=end_time,
        page=page,
        size=size,
        start_time=start_time,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    end_time: Union[Unset, str] = "2099-01-01",
    page: Union[Unset, int] = 1,
    size: Union[Unset, int] = 10,
    start_time: Union[Unset, str] = "1970-01-01",
) -> Optional[APIResultSearchResult]:
    """harvest dataset by dataset's publish time period(start_time and end_time)

     result is order by publish time desc

    Args:
        end_time (Union[Unset, str]):  Default: '2099-01-01'.
        page (Union[Unset, int]):  Default: 1.
        size (Union[Unset, int]):  Default: 10.
        start_time (Union[Unset, str]):  Default: '1970-01-01'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIResultSearchResult
    """

    return (
        await asyncio_detailed(
            client=client,
            end_time=end_time,
            page=page,
            size=size,
            start_time=start_time,
        )
    ).parsed
