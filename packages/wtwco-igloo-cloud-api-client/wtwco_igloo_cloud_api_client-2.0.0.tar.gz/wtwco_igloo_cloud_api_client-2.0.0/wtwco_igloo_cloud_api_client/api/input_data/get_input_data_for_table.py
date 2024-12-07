from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.input_data_response import InputDataResponse
from ...models.response_wrapper import ResponseWrapper
from ...types import Response


def _get_kwargs(
    project_id: int,
    run_id: int,
    data_table_name: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/api/v2/projects/{project_id}/runs/{run_id}/inputdata/{data_table_name}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, InputDataResponse, ResponseWrapper]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = InputDataResponse.from_dict(response.json())

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
    if response.status_code == HTTPStatus.CONFLICT:
        response_409 = cast(Any, None)
        return response_409
    if response.status_code == HTTPStatus.UNSUPPORTED_MEDIA_TYPE:
        response_415 = ResponseWrapper.from_dict(response.json())

        return response_415
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, InputDataResponse, ResponseWrapper]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: int,
    run_id: int,
    data_table_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, InputDataResponse, ResponseWrapper]]:
    """Get the input data in a table for a run.

    Args:
        project_id (int):
        run_id (int):
        data_table_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, InputDataResponse, ResponseWrapper]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        run_id=run_id,
        data_table_name=data_table_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: int,
    run_id: int,
    data_table_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, InputDataResponse, ResponseWrapper]]:
    """Get the input data in a table for a run.

    Args:
        project_id (int):
        run_id (int):
        data_table_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, InputDataResponse, ResponseWrapper]
    """

    return sync_detailed(
        project_id=project_id,
        run_id=run_id,
        data_table_name=data_table_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    project_id: int,
    run_id: int,
    data_table_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, InputDataResponse, ResponseWrapper]]:
    """Get the input data in a table for a run.

    Args:
        project_id (int):
        run_id (int):
        data_table_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, InputDataResponse, ResponseWrapper]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        run_id=run_id,
        data_table_name=data_table_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: int,
    run_id: int,
    data_table_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, InputDataResponse, ResponseWrapper]]:
    """Get the input data in a table for a run.

    Args:
        project_id (int):
        run_id (int):
        data_table_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, InputDataResponse, ResponseWrapper]
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            run_id=run_id,
            data_table_name=data_table_name,
            client=client,
        )
    ).parsed
