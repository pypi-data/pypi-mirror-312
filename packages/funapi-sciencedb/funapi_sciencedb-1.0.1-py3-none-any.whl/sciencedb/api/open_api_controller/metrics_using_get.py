from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_metrics_result import APIResultMetricsResult
from ...types import UNSET, Response


def _get_kwargs(
    *,
    doi: str,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["doi"] = doi

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/metrics",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[APIResultMetricsResult]:
    if response.status_code == 200:
        response_200 = APIResultMetricsResult.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[APIResultMetricsResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    doi: str,
) -> Response[APIResultMetricsResult]:
    """search dataset metrics by doi

     search dataset metrics by doi

    Args:
        doi (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIResultMetricsResult]
    """

    kwargs = _get_kwargs(
        doi=doi,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    doi: str,
) -> Optional[APIResultMetricsResult]:
    """search dataset metrics by doi

     search dataset metrics by doi

    Args:
        doi (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIResultMetricsResult
    """

    return sync_detailed(
        client=client,
        doi=doi,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    doi: str,
) -> Response[APIResultMetricsResult]:
    """search dataset metrics by doi

     search dataset metrics by doi

    Args:
        doi (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIResultMetricsResult]
    """

    kwargs = _get_kwargs(
        doi=doi,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    doi: str,
) -> Optional[APIResultMetricsResult]:
    """search dataset metrics by doi

     search dataset metrics by doi

    Args:
        doi (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIResultMetricsResult
    """

    return (
        await asyncio_detailed(
            client=client,
            doi=doi,
        )
    ).parsed
