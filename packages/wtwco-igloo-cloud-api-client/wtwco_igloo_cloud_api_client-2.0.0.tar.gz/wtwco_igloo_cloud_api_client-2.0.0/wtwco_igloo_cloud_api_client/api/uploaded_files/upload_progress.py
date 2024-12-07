from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.response_wrapper import ResponseWrapper
from ...models.upload_progress import UploadProgress
from ...types import Response


def _get_kwargs(
    file_id: int,
    upload_identifier: str,
    *,
    body: UploadProgress,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/api/v2/uploadedfiles/{file_id}/upload/{upload_identifier}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ResponseWrapper]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(Any, None)
        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = cast(Any, None)
        return response_403
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
) -> Response[Union[Any, ResponseWrapper]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    file_id: int,
    upload_identifier: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UploadProgress,
) -> Response[Union[Any, ResponseWrapper]]:
    """Update the file upload progress information. You must call this endpoint with UploadPercent equal to
    100
    to indicate that the file upload process has completed.
    When this has been done the status of the file will change to UploadCompleting while the system
    scans the contents, followed by Uploaded
    a short time later.

    Args:
        file_id (int):
        upload_identifier (str):
        body (UploadProgress):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ResponseWrapper]]
    """

    kwargs = _get_kwargs(
        file_id=file_id,
        upload_identifier=upload_identifier,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    file_id: int,
    upload_identifier: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UploadProgress,
) -> Optional[Union[Any, ResponseWrapper]]:
    """Update the file upload progress information. You must call this endpoint with UploadPercent equal to
    100
    to indicate that the file upload process has completed.
    When this has been done the status of the file will change to UploadCompleting while the system
    scans the contents, followed by Uploaded
    a short time later.

    Args:
        file_id (int):
        upload_identifier (str):
        body (UploadProgress):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ResponseWrapper]
    """

    return sync_detailed(
        file_id=file_id,
        upload_identifier=upload_identifier,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    file_id: int,
    upload_identifier: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UploadProgress,
) -> Response[Union[Any, ResponseWrapper]]:
    """Update the file upload progress information. You must call this endpoint with UploadPercent equal to
    100
    to indicate that the file upload process has completed.
    When this has been done the status of the file will change to UploadCompleting while the system
    scans the contents, followed by Uploaded
    a short time later.

    Args:
        file_id (int):
        upload_identifier (str):
        body (UploadProgress):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ResponseWrapper]]
    """

    kwargs = _get_kwargs(
        file_id=file_id,
        upload_identifier=upload_identifier,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    file_id: int,
    upload_identifier: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UploadProgress,
) -> Optional[Union[Any, ResponseWrapper]]:
    """Update the file upload progress information. You must call this endpoint with UploadPercent equal to
    100
    to indicate that the file upload process has completed.
    When this has been done the status of the file will change to UploadCompleting while the system
    scans the contents, followed by Uploaded
    a short time later.

    Args:
        file_id (int):
        upload_identifier (str):
        body (UploadProgress):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ResponseWrapper]
    """

    return (
        await asyncio_detailed(
            file_id=file_id,
            upload_identifier=upload_identifier,
            client=client,
            body=body,
        )
    ).parsed
