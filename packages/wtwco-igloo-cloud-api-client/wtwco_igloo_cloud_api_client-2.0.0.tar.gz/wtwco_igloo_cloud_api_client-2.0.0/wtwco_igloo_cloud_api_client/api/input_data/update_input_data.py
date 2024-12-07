from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.response_wrapper import ResponseWrapper
from ...models.update_input_data import UpdateInputData
from ...types import Response


def _get_kwargs(
    project_id: int,
    run_id: int,
    *,
    body: UpdateInputData,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/api/v2/projects/{project_id}/runs/{run_id}/inputdata",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ResponseWrapper]]:
    if response.status_code == HTTPStatus.NO_CONTENT:
        response_204 = cast(Any, None)
        return response_204
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
    if response.status_code == HTTPStatus.CONFLICT:
        response_409 = cast(Any, None)
        return response_409
    if response.status_code == HTTPStatus.GONE:
        response_410 = cast(Any, None)
        return response_410
    if response.status_code == HTTPStatus.UNSUPPORTED_MEDIA_TYPE:
        response_415 = ResponseWrapper.from_dict(response.json())

        return response_415
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, ResponseWrapper]]:
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
    body: UpdateInputData,
) -> Response[Union[Any, ResponseWrapper]]:
    """Make some updates to the input data for a run.

    Args:
        project_id (int):
        run_id (int):
        body (UpdateInputData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ResponseWrapper]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        run_id=run_id,
        body=body,
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
    body: UpdateInputData,
) -> Optional[Union[Any, ResponseWrapper]]:
    """Make some updates to the input data for a run.

    Args:
        project_id (int):
        run_id (int):
        body (UpdateInputData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ResponseWrapper]
    """

    return sync_detailed(
        project_id=project_id,
        run_id=run_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    project_id: int,
    run_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateInputData,
) -> Response[Union[Any, ResponseWrapper]]:
    """Make some updates to the input data for a run.

    Args:
        project_id (int):
        run_id (int):
        body (UpdateInputData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ResponseWrapper]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        run_id=run_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: int,
    run_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateInputData,
) -> Optional[Union[Any, ResponseWrapper]]:
    """Make some updates to the input data for a run.

    Args:
        project_id (int):
        run_id (int):
        body (UpdateInputData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ResponseWrapper]
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            run_id=run_id,
            client=client,
            body=body,
        )
    ).parsed
