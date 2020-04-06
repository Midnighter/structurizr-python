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

import pytest

from structurizr.api.structurizr_client import StructurizrClient


MockSettings = namedtuple(
    "MockSettings", "url workspace_id api_key api_secret user agent"
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
