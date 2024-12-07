from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.output_data_response import OutputDataResponse
from ...models.response_wrapper import ResponseWrapper
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: int,
    run_id: int,
    *,
    table_name: Union[Unset, str] = UNSET,
    pool: Union[Unset, str] = UNSET,
    wait_seconds: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["tableName"] = table_name

    params["pool"] = pool

    params["waitSeconds"] = wait_seconds

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/api/v2/projects/{project_id}/runs/{run_id}/outputdata",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, OutputDataResponse, ResponseWrapper]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = OutputDataResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == HTTPStatus.NOT_ACCEPTABLE:
        response_406 = ResponseWrapper.from_dict(response.json())

        return response_406
    if response.status_code == HTTPStatus.UNSUPPORTED_MEDIA_TYPE:
        response_415 = ResponseWrapper.from_dict(response.json())

        return response_415
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, OutputDataResponse, ResponseWrapper]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: int,
    run_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    table_name: Union[Unset, str] = UNSET,
    pool: Union[Unset, str] = UNSET,
    wait_seconds: Union[Unset, int] = 0,
) -> Response[Union[Any, OutputDataResponse, ResponseWrapper]]:
    """Gets the output data for a run, this will force a run to be submitted if necessary

    Args:
        project_id (int):
        run_id (int):
        table_name (Union[Unset, str]):
        pool (Union[Unset, str]):
        wait_seconds (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, OutputDataResponse, ResponseWrapper]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        run_id=run_id,
        table_name=table_name,
        pool=pool,
        wait_seconds=wait_seconds,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: int,
    run_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    table_name: Union[Unset, str] = UNSET,
    pool: Union[Unset, str] = UNSET,
    wait_seconds: Union[Unset, int] = 0,
) -> Optional[Union[Any, OutputDataResponse, ResponseWrapper]]:
    """Gets the output data for a run, this will force a run to be submitted if necessary

    Args:
        project_id (int):
        run_id (int):
        table_name (Union[Unset, str]):
        pool (Union[Unset, str]):
        wait_seconds (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, OutputDataResponse, ResponseWrapper]
    """

    return sync_detailed(
        project_id=project_id,
        run_id=run_id,
        client=client,
        table_name=table_name,
        pool=pool,
        wait_seconds=wait_seconds,
    ).parsed


async def asyncio_detailed(
    project_id: int,
    run_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    table_name: Union[Unset, str] = UNSET,
    pool: Union[Unset, str] = UNSET,
    wait_seconds: Union[Unset, int] = 0,
) -> Response[Union[Any, OutputDataResponse, ResponseWrapper]]:
    """Gets the output data for a run, this will force a run to be submitted if necessary

    Args:
        project_id (int):
        run_id (int):
        table_name (Union[Unset, str]):
        pool (Union[Unset, str]):
        wait_seconds (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, OutputDataResponse, ResponseWrapper]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        run_id=run_id,
        table_name=table_name,
        pool=pool,
        wait_seconds=wait_seconds,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: int,
    run_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    table_name: Union[Unset, str] = UNSET,
    pool: Union[Unset, str] = UNSET,
    wait_seconds: Union[Unset, int] = 0,
) -> Optional[Union[Any, OutputDataResponse, ResponseWrapper]]:
    """Gets the output data for a run, this will force a run to be submitted if necessary

    Args:
        project_id (int):
        run_id (int):
        table_name (Union[Unset, str]):
        pool (Union[Unset, str]):
        wait_seconds (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, OutputDataResponse, ResponseWrapper]
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            run_id=run_id,
            client=client,
            table_name=table_name,
            pool=pool,
            wait_seconds=wait_seconds,
        )
    ).parsed
