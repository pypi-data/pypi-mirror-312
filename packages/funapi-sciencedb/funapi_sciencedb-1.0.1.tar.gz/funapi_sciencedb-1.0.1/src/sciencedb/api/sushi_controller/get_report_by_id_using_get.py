from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.sushi_report import SUSHIReport
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    publisher: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["publisher"] = publisher

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/report/{id}".format(
            id=id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[SUSHIReport]:
    if response.status_code == 200:
        response_200 = SUSHIReport.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SUSHIReport]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    publisher: Union[Unset, str] = UNSET,
) -> Response[SUSHIReport]:
    """This resource returns the COUNTER Dataset Report by id

    Args:
        id (str):
        publisher (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SUSHIReport]
    """

    kwargs = _get_kwargs(
        id=id,
        publisher=publisher,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    publisher: Union[Unset, str] = UNSET,
) -> Optional[SUSHIReport]:
    """This resource returns the COUNTER Dataset Report by id

    Args:
        id (str):
        publisher (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SUSHIReport
    """

    return sync_detailed(
        id=id,
        client=client,
        publisher=publisher,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    publisher: Union[Unset, str] = UNSET,
) -> Response[SUSHIReport]:
    """This resource returns the COUNTER Dataset Report by id

    Args:
        id (str):
        publisher (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SUSHIReport]
    """

    kwargs = _get_kwargs(
        id=id,
        publisher=publisher,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    publisher: Union[Unset, str] = UNSET,
) -> Optional[SUSHIReport]:
    """This resource returns the COUNTER Dataset Report by id

    Args:
        id (str):
        publisher (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SUSHIReport
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            publisher=publisher,
        )
    ).parsed
