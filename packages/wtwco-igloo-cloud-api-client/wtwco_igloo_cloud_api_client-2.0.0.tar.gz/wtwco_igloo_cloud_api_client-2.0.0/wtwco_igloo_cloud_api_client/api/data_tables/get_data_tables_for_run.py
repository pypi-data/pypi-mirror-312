from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.data_table_node_array_response import DataTableNodeArrayResponse
from ...models.response_wrapper import ResponseWrapper
from ...types import Response


def _get_kwargs(
    project_id: int,
    run_id: int,
    data_group_name: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/api/v2/projects/{project_id}/runs/{run_id}/datagroups/{data_group_name}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, DataTableNodeArrayResponse, ResponseWrapper]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = DataTableNodeArrayResponse.from_dict(response.json())

        return response_200
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
) -> Response[Union[Any, DataTableNodeArrayResponse, ResponseWrapper]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: int,
    run_id: int,
    data_group_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, DataTableNodeArrayResponse, ResponseWrapper]]:
    """Gets the collection of input data tables in a data group.

    Args:
        project_id (int):
        run_id (int):
        data_group_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DataTableNodeArrayResponse, ResponseWrapper]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        run_id=run_id,
        data_group_name=data_group_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: int,
    run_id: int,
    data_group_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, DataTableNodeArrayResponse, ResponseWrapper]]:
    """Gets the collection of input data tables in a data group.

    Args:
        project_id (int):
        run_id (int):
        data_group_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DataTableNodeArrayResponse, ResponseWrapper]
    """

    return sync_detailed(
        project_id=project_id,
        run_id=run_id,
        data_group_name=data_group_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    project_id: int,
    run_id: int,
    data_group_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, DataTableNodeArrayResponse, ResponseWrapper]]:
    """Gets the collection of input data tables in a data group.

    Args:
        project_id (int):
        run_id (int):
        data_group_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DataTableNodeArrayResponse, ResponseWrapper]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        run_id=run_id,
        data_group_name=data_group_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: int,
    run_id: int,
    data_group_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, DataTableNodeArrayResponse, ResponseWrapper]]:
    """Gets the collection of input data tables in a data group.

    Args:
        project_id (int):
        run_id (int):
        data_group_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DataTableNodeArrayResponse, ResponseWrapper]
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            run_id=run_id,
            data_group_name=data_group_name,
            client=client,
        )
    ).parsed
