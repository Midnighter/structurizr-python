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

import pytest

from structurizr.api.structurizr_client import StructurizrClient


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
def client(mock_settings):
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


def test_add_headers_authentication(client: StructurizrClient, mocker):
    """Validate the headers are added correctly, including authentication."""
    mocker.patch.object(
        client,
        "_number_once",
        return_value="1529225966174"
    )
    request = client._client.build_request("GET", client._workspace_url)
    headers = client._add_headers(request)
    assert headers['Nonce'] == "1529225966174"
    assert headers['X-Authorization'] == (
        '7f4e4edc-f61c-4ff2-97c9-ea4bc2a7c98c:'
        'ZmJhNTVkMDM2NGEwN2I5YjRhMDgwZWNhMjA0ODIzZD'
        'kyMTg3YzliMzVhMjBlNmM4ZjAxMDAwOGU4OGJlODEwMQ=='
    )
    assert 'Content-MD5' not in headers
    assert 'Content-Type' not in headers

    # Check the additional headers needed for PUTs
    request = client._client.build_request("PUT", client._workspace_url)
    headers = client._add_headers(request, content="Hello", content_type="World")
    assert headers['Content-MD5'] == 'OGIxYTk5NTNjNDYxMTI5NmE4MjdhYmY4YzQ3ODA0ZDc='
    assert headers['Content-Type'] == 'World'
