from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.paginated_response_historical_order import PaginatedResponseHistoricalOrder
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: Union[Unset, int] = UNSET,
    ticker: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["ticker"] = ticker

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v0/equity/history/orders",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, PaginatedResponseHistoricalOrder]]:
    if response.status_code == 200:
        response_200 = PaginatedResponseHistoricalOrder.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == 408:
        response_408 = cast(Any, None)
        return response_408
    if response.status_code == 429:
        response_429 = cast(Any, None)
        return response_429
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, PaginatedResponseHistoricalOrder]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    cursor: Union[Unset, int] = UNSET,
    ticker: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Response[Union[Any, PaginatedResponseHistoricalOrder]]:
    """Historical order data

    Args:
        cursor (Union[Unset, int]):
        ticker (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PaginatedResponseHistoricalOrder]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        ticker=ticker,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    cursor: Union[Unset, int] = UNSET,
    ticker: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Optional[Union[Any, PaginatedResponseHistoricalOrder]]:
    """Historical order data

    Args:
        cursor (Union[Unset, int]):
        ticker (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PaginatedResponseHistoricalOrder]
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
        ticker=ticker,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    cursor: Union[Unset, int] = UNSET,
    ticker: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Response[Union[Any, PaginatedResponseHistoricalOrder]]:
    """Historical order data

    Args:
        cursor (Union[Unset, int]):
        ticker (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PaginatedResponseHistoricalOrder]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        ticker=ticker,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    cursor: Union[Unset, int] = UNSET,
    ticker: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Optional[Union[Any, PaginatedResponseHistoricalOrder]]:
    """Historical order data

    Args:
        cursor (Union[Unset, int]):
        ticker (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PaginatedResponseHistoricalOrder]
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
            ticker=ticker,
            limit=limit,
        )
    ).parsed
