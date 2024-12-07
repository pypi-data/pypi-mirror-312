from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.data_table_include import DataTableInclude
from ...models.response_wrapper import ResponseWrapper
from ...models.table_data_response import TableDataResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: int,
    run_id: int,
    data_group_name: str,
    data_table_name: str,
    *,
    include: Union[Unset, DataTableInclude] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_include: Union[Unset, str] = UNSET
    if not isinstance(include, Unset):
        json_include = include.value

    params["include"] = json_include

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/api/v2/projects/{project_id}/runs/{run_id}/datagroups/{data_group_name}/{data_table_name}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ResponseWrapper, TableDataResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = TableDataResponse.from_dict(response.json())

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
) -> Response[Union[Any, ResponseWrapper, TableDataResponse]]:
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
    data_table_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include: Union[Unset, DataTableInclude] = UNSET,
) -> Response[Union[Any, ResponseWrapper, TableDataResponse]]:
    """Gets the definition and/or the data of an input data table.

    Args:
        project_id (int):
        run_id (int):
        data_group_name (str):
        data_table_name (str):
        include (Union[Unset, DataTableInclude]): Used in a GetDataTableForRun query to indicate
            whether you are interested in the table definition, the table data or both of these
            things.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ResponseWrapper, TableDataResponse]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        run_id=run_id,
        data_group_name=data_group_name,
        data_table_name=data_table_name,
        include=include,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: int,
    run_id: int,
    data_group_name: str,
    data_table_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include: Union[Unset, DataTableInclude] = UNSET,
) -> Optional[Union[Any, ResponseWrapper, TableDataResponse]]:
    """Gets the definition and/or the data of an input data table.

    Args:
        project_id (int):
        run_id (int):
        data_group_name (str):
        data_table_name (str):
        include (Union[Unset, DataTableInclude]): Used in a GetDataTableForRun query to indicate
            whether you are interested in the table definition, the table data or both of these
            things.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ResponseWrapper, TableDataResponse]
    """

    return sync_detailed(
        project_id=project_id,
        run_id=run_id,
        data_group_name=data_group_name,
        data_table_name=data_table_name,
        client=client,
        include=include,
    ).parsed


async def asyncio_detailed(
    project_id: int,
    run_id: int,
    data_group_name: str,
    data_table_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include: Union[Unset, DataTableInclude] = UNSET,
) -> Response[Union[Any, ResponseWrapper, TableDataResponse]]:
    """Gets the definition and/or the data of an input data table.

    Args:
        project_id (int):
        run_id (int):
        data_group_name (str):
        data_table_name (str):
        include (Union[Unset, DataTableInclude]): Used in a GetDataTableForRun query to indicate
            whether you are interested in the table definition, the table data or both of these
            things.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ResponseWrapper, TableDataResponse]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        run_id=run_id,
        data_group_name=data_group_name,
        data_table_name=data_table_name,
        include=include,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: int,
    run_id: int,
    data_group_name: str,
    data_table_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include: Union[Unset, DataTableInclude] = UNSET,
) -> Optional[Union[Any, ResponseWrapper, TableDataResponse]]:
    """Gets the definition and/or the data of an input data table.

    Args:
        project_id (int):
        run_id (int):
        data_group_name (str):
        data_table_name (str):
        include (Union[Unset, DataTableInclude]): Used in a GetDataTableForRun query to indicate
            whether you are interested in the table definition, the table data or both of these
            things.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ResponseWrapper, TableDataResponse]
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            run_id=run_id,
            data_group_name=data_group_name,
            data_table_name=data_table_name,
            client=client,
            include=include,
        )
    ).parsed
