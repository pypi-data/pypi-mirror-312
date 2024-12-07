from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.sushi_service_status import SUSHIServiceStatus
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    platform: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["platform"] = platform

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/status",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["SUSHIServiceStatus"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = SUSHIServiceStatus.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["SUSHIServiceStatus"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    platform: Union[Unset, str] = UNSET,
) -> Response[List["SUSHIServiceStatus"]]:
    """getAPIStatus

     This resource returns the current status of the reporting service supported by this API.

    Args:
        platform (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['SUSHIServiceStatus']]
    """

    kwargs = _get_kwargs(
        platform=platform,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    platform: Union[Unset, str] = UNSET,
) -> Optional[List["SUSHIServiceStatus"]]:
    """getAPIStatus

     This resource returns the current status of the reporting service supported by this API.

    Args:
        platform (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['SUSHIServiceStatus']
    """

    return sync_detailed(
        client=client,
        platform=platform,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    platform: Union[Unset, str] = UNSET,
) -> Response[List["SUSHIServiceStatus"]]:
    """getAPIStatus

     This resource returns the current status of the reporting service supported by this API.

    Args:
        platform (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['SUSHIServiceStatus']]
    """

    kwargs = _get_kwargs(
        platform=platform,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    platform: Union[Unset, str] = UNSET,
) -> Optional[List["SUSHIServiceStatus"]]:
    """getAPIStatus

     This resource returns the current status of the reporting service supported by this API.

    Args:
        platform (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['SUSHIServiceStatus']
    """

    return (
        await asyncio_detailed(
            client=client,
            platform=platform,
        )
    ).parsed
