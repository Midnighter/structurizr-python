# Copyright (c) 2020, Moritz E. Beber.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Ensure the expected behaviour of the Structurizr client."""


from collections import namedtuple
from datetime import datetime
from gzip import GzipFile
from pathlib import Path
from typing import List

import httpx
import pytest
from httpx import URL, Request, Response
from pytest_mock import MockerFixture

from structurizr.api.structurizr_client import StructurizrClient
from structurizr.api.structurizr_client_exception import StructurizrClientException
from structurizr.workspace import Workspace


MockSettings = namedtuple(
    "MockSettings",
    "url workspace_id api_key api_secret user agent workspace_archive_location",
)


@pytest.fixture(scope="module")
def mock_settings():
    """Provide standardized settings."""
    return MockSettings(
        url="https://api.structurizr.com",
        workspace_id=19,
        api_key="7f4e4edc-f61c-4ff2-97c9-ea4bc2a7c98c",
        api_secret="ae140655-da7c-4a8d-9467-5a7d9792fca0",
        user="astley@localhost",
        agent="structurizr-python/1.0.0",
        workspace_archive_location=Path("."),
    )


@pytest.fixture(scope="function")
def client(mock_settings) -> StructurizrClient:
    """Provide a client instance with the mock settings."""
    return StructurizrClient(settings=mock_settings)


def test_init(mock_settings):
    """Expect proper initialization from arguments."""
    client = StructurizrClient(settings=mock_settings)
    assert client.url == "https://api.structurizr.com"
    assert client.workspace_id == 19
    assert client.api_key == "7f4e4edc-f61c-4ff2-97c9-ea4bc2a7c98c"
    assert client.api_secret == "ae140655-da7c-4a8d-9467-5a7d9792fca0"
    assert client.user == "astley@localhost"
    assert client.agent == "structurizr-python/1.0.0"
    assert str(client.workspace_archive_location) == "."


def test_repr(client):
    """Expect the correct client string representation."""
    assert (
        repr(client)
        == "StructurizrClient(url=https://api.structurizr.com, workspace_id=19)"
    )


@pytest.mark.parametrize(
    "content, expected", [("", "d41d8cd98f00b204e9800998ecf8427e")]
)
def test_md5(client, content, expected):
    """
    Expect the correct md5 hashes.

    Notes:
        These hashes are verified by external tools.
    """
    assert client._md5(content) == expected


def test_create_archive_filename(client):
    """Expect a specific format for the archive file name."""
    path = client._create_archive_filename()
    timestamp = datetime.utcnow()
    time_component = (
        f"{timestamp.year:04d}{timestamp.month:02d}{timestamp.day:02d}"
        f"{timestamp.hour:02d}"
    )
    assert path.match(f"structurizr-19-{time_component}*.json.gz")


def test_archive_workspace(client, mocker):
    """Expect that a filename is generated and JSON content is written to a file."""
    mocked_filename = mocker.patch.object(
        client,
        "_create_archive_filename",
        return_value=Path("structurizr-19-time.json.gz"),
    )
    mocked_open = mocker.mock_open(mock=mocker.Mock(spec_set=GzipFile))
    mocker.patch("gzip.open", mocked_open)
    client._archive_workspace('{"mock_key":"mock_value"}')
    mocked_filename.assert_called_once()
    mocked_open.assert_called_once_with(Path("structurizr-19-time.json.gz"), mode="wt")
    mocked_handle = mocked_open()
    mocked_handle.write.assert_called_once_with('{"mock_key":"mock_value"}')


def test_suppressing_archive(mock_settings, mocker):
    """Test that when the archive location is None then no archive is written."""
    old_settings = mock_settings._asdict()
    old_settings["workspace_archive_location"] = None
    new_mock_settings = MockSettings(**old_settings)
    client = StructurizrClient(settings=new_mock_settings)

    mocked_open = mocker.mock_open(mock=mocker.Mock(spec_set=GzipFile))
    mocker.patch("gzip.open", mocked_open)

    client._archive_workspace('{"mock_key":"mock_value"}')
    assert not mocked_open.called


def test_httpx_response_raw_path_behaviour():
    """Make sure that `Response.raw_path` continues to do what we need.

    As the httpx library is evolving rapidly, this is a defensive test to make sure
    that `Response.raw_path` continues to behave as we need for StructurizrClient, in
    particular not HTTP-escaping parameters, but still ASCII-encoding the URL.
    """
    url = URL("http://example.com:8080/api/test?q=motörhead")
    assert url.raw_path.decode("ascii") == "/api/test?q=mot%C3%B6rhead"


def test_add_headers_authentication(client: StructurizrClient, mocker):
    """Validate the headers are added correctly, including authentication."""
    mocker.patch.object(client, "_number_once", return_value="1529225966174")
    request = client._client.build_request("GET", client._workspace_url)
    headers = client._add_headers(request)
    assert headers["Nonce"] == "1529225966174"
    assert headers["X-Authorization"] == (
        "7f4e4edc-f61c-4ff2-97c9-ea4bc2a7c98c:"
        "ZmJhNTVkMDM2NGEwN2I5YjRhMDgwZWNhMjA0ODIzZD"
        "kyMTg3YzliMzVhMjBlNmM4ZjAxMDAwOGU4OGJlODEwMQ=="
    )
    assert "Content-MD5" not in headers
    assert "Content-Type" not in headers

    # Check the additional headers needed for PUTs
    request = client._client.build_request("PUT", client._workspace_url)
    headers = client._add_headers(request, content="Hello", content_type="World")
    assert headers["Content-MD5"] == "OGIxYTk5NTNjNDYxMTI5NmE4MjdhYmY4YzQ3ODA0ZDc="
    assert headers["Content-Type"] == "World"


def test_get_workspace_handles_error_responses(
    client: StructurizrClient, mocker: MockerFixture
):
    """Test that response code other than 200 raise an exception."""
    mocker.patch.object(client._client, "send", return_value=Response(403))
    with pytest.raises(
        StructurizrClientException,
        match="Failed .* workspace 19.\nResponse 403 - Forbidden",
    ):
        client.get_workspace()


def test_put_workspace_handles_error_responses(
    client: StructurizrClient, mocker: MockerFixture
):
    """Test that response code other than 200 raise an exception."""
    mocker.patch.object(client._client, "send", return_value=Response(403))
    workspace = Workspace(name="Workspace 1", description="", id=19)
    with pytest.raises(
        StructurizrClientException,
        match="Failed .* workspace 19.\nResponse 403 - Forbidden",
    ):
        client.put_workspace(workspace)


def test_locking_and_unlocking(client: StructurizrClient, mocker: MockerFixture):
    """Ensure that using the client in a with block locks and unlocks."""
    requests: List[Request] = []

    def fake_send(request: Request):
        nonlocal requests
        requests.append(request)
        return Response(
            200,
            content='{"success": true, "message": "OK"}'.encode("ascii"),
            request=request,
        )

    mocker.patch.object(client._client, "send", new=fake_send)
    with client:
        pass

    assert len(requests) == 2
    assert requests[0].method == "PUT"
    assert requests[0].url.path == "/workspace/19/lock"
    assert requests[1].method == "DELETE"
    assert requests[1].url.path == "/workspace/19/lock"


def test_locking_and_unlocking_on_free_plan(
    client: StructurizrClient, mocker: MockerFixture
):
    """Ensure that lock failures on free plans are handled correctly."""
    requests: List[Request] = []

    def fake_send(request: Request):
        nonlocal requests
        requests.append(request)
        return Response(
            200,
            content='{"success": false, "message": "Free plans cannot lock"}'.encode(
                "ascii"
            ),
            request=request,
        )

    mocker.patch.object(client._client, "send", new=fake_send)
    with client:
        pass

    assert len(requests) == 2
    assert requests[0].method == "PUT"
    assert requests[0].url.path == "/workspace/19/lock"
    assert requests[1].method == "DELETE"
    assert requests[1].url.path == "/workspace/19/lock"


def test_locking_and_unlocking_with_context_manager(
    client: StructurizrClient, mocker: MockerFixture
):
    """Check new-style locking using .lock()."""
    requests: List[Request] = []

    def fake_send(request: Request):
        nonlocal requests
        requests.append(request)
        return Response(
            200,
            content='{"success": true, "message": "OK"}'.encode("ascii"),
            request=request,
        )

    mocker.patch.object(client._client, "send", new=fake_send)
    with client.lock():
        pass

    assert len(requests) == 2
    assert requests[0].method == "PUT"
    assert requests[0].url.path == "/workspace/19/lock"
    assert requests[1].method == "DELETE"
    assert requests[1].url.path == "/workspace/19/lock"


def test_failed_lock_raises_exception(client: StructurizrClient, mocker: MockerFixture):
    """Check failing to lock raises an exception.

    Trying to lock a workspace which is already locked by someone else actually
    returns a 200 status, but with success as false in the message.
    """

    def fake_send(request: Request):
        msg = '{"success": false, "message": "The workspace is already locked"}'
        return Response(
            200,
            content=msg.encode("ascii"),
            request=request,
        )

    mocker.patch.object(client._client, "send", new=fake_send)
    with pytest.raises(StructurizrClientException, match="Failed to lock"):
        with client.lock():
            pass


def test_failed_unlock_raises_exception(
    client: StructurizrClient, mocker: MockerFixture
):
    """Check failing to unlock raises an exception.

    Not quite sure how this could occur, but check the handling anyway.
    """

    def fake_send(request: Request):
        if request.method == "PUT":
            return Response(
                200,
                content='{"success": true, "message": "OK"}'.encode("ascii"),
                request=request,
            )
        else:
            return Response(
                200,
                content='{"success": false, "message": "Not OK"}'.encode("ascii"),
                request=request,
            )

    mocker.patch.object(client._client, "send", new=fake_send)
    with pytest.raises(StructurizrClientException, match="Failed to unlock"):
        with client.lock():
            pass


def test_failed_lock_bad_http_code(client: StructurizrClient, mocker: MockerFixture):
    """Check getting a non-200 HTTP response raises an HTTPX exception.

    Trying to lock a workspace which is already locked by someone else actually
    returns a 200 status, but with success as false in the message.
    """

    def fake_send(request: Request):
        msg = "Server failure"
        return Response(
            500,
            content=msg.encode("ascii"),
            request=request,
        )

    mocker.patch.object(client._client, "send", new=fake_send)
    with pytest.raises(httpx.HTTPStatusError):
        with client.lock():
            pass


def test_failed_lock_on_free_plan_doesnt_attempt_unlock(
    client: StructurizrClient, mocker: MockerFixture
):
    """Check that if lock failed because on free plan then unlock isn't called."""
    requests: List[Request] = []

    def fake_send(request: Request):
        nonlocal requests
        requests.append(request)
        return Response(
            200,
            content='{"success": false, "message": "Cannot lock on free plan"}'.encode(
                "ascii"
            ),
            request=request,
        )

    mocker.patch.object(client._client, "send", new=fake_send)
    with client.lock():
        pass

    assert len(requests) == 1
