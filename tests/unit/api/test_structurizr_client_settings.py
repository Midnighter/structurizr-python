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


"""Ensure the expected behaviour of the Structurizr client settings."""


import pytest
from pydantic import ValidationError

from structurizr.api.structurizr_client_settings import StructurizrClientSettings


@pytest.fixture(scope="module")
def archive_location(tmp_path_factory):
    """Return a temporary path to use in tests."""
    location = tmp_path_factory.mktemp("structurizr")
    return str(location)


@pytest.fixture(scope="function")
def mock_structurizr_env(monkeypatch, archive_location):
    """Reversibly modify the environment."""
    monkeypatch.setenv("STRUCTURIZR_URL", "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    monkeypatch.setenv("STRUCTURIZR_WORKSPACE_ID", "19")
    monkeypatch.setenv("STRUCTURIZR_API_KEY", "7f4e4edc-f61c-4ff2-97c9-ea4bc2a7c98c")
    monkeypatch.setenv("STRUCTURIZR_API_SECRET", "ae140655-da7c-4a8d-9467-5a7d9792fca0")
    monkeypatch.setenv("STRUCTURIZR_USER", "astley@localhost")
    monkeypatch.setenv("STRUCTURIZR_AGENT", "structurizr-python/1.0.0")
    monkeypatch.setenv("STRUCTURIZR_WORKSPACE_ARCHIVE_LOCATION", archive_location)


@pytest.fixture(scope="function")
def dotenv(tmpdir, monkeypatch, archive_location):
    """Create a `.env` file for client settings."""
    path = tmpdir.mkdir("dotenv")
    env_file = path.join(".env")
    env_file.write(
        "STRUCTURIZR_URL=https://www.youtube.com/watch?v=dQw4w9WgXcQ\n"
        "STRUCTURIZR_WORKSPACE_ID=19\n"
        "STRUCTURIZR_API_KEY=7f4e4edc-f61c-4ff2-97c9-ea4bc2a7c98c\n"
        "STRUCTURIZR_API_SECRET=ae140655-da7c-4a8d-9467-5a7d9792fca0\n"
        "STRUCTURIZR_USER=astley@localhost\n"
        "STRUCTURIZR_AGENT=structurizr-python/1.0.0\n"
        f"STRUCTURIZR_WORKSPACE_ARCHIVE_LOCATION={archive_location}\n"
    )
    monkeypatch.chdir(path)


@pytest.mark.parametrize(
    "attributes",
    [
        pytest.param(
            {},
            marks=pytest.mark.raises(
                exception=ValidationError, message="workspace_id\n  field required"
            ),
        ),
        pytest.param(
            {},
            marks=pytest.mark.raises(
                exception=ValidationError, message="api_key\n  field required"
            ),
        ),
        pytest.param(
            {},
            marks=pytest.mark.raises(
                exception=ValidationError, message="api_secret\n  field required"
            ),
        ),
        pytest.param(
            {"workspace_id": "something"},
            marks=pytest.mark.raises(
                exception=ValidationError,
                message="workspace_id\n  value is not a valid integer",
            ),
        ),
        pytest.param(
            {"api_key": "2"},
            marks=pytest.mark.raises(
                exception=ValidationError,
                message="api_key\n  value is not a valid uuid",
            ),
        ),
        pytest.param(
            {"api_secret": "2"},
            marks=pytest.mark.raises(
                exception=ValidationError,
                message="api_secret\n  value is not a valid uuid",
            ),
        ),
        {
            "workspace_id": 1,
            "api_key": "7f4e4edc-f61c-4ff2-97c9-ea4bc2a7c98c",
            "api_secret": "ae140655-da7c-4a8d-9467-5a7d9792fca0",
        },
        pytest.param(
            {"url": "proper-url?"},
            marks=pytest.mark.raises(
                exception=ValidationError,
                message="url\n  invalid",
            ),
        ),
        {
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "workspace_id": 19,
            "api_key": "7f4e4edc-f61c-4ff2-97c9-ea4bc2a7c98c",
            "api_secret": "ae140655-da7c-4a8d-9467-5a7d9792fca0",
        },
        {
            "workspace_id": 19,
            "api_key": "7f4e4edc-f61c-4ff2-97c9-ea4bc2a7c98c",
            "api_secret": "ae140655-da7c-4a8d-9467-5a7d9792fca0",
            "user": "astley@localhost",
        },
        {
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "workspace_id": 19,
            "api_key": "7f4e4edc-f61c-4ff2-97c9-ea4bc2a7c98c",
            "api_secret": "ae140655-da7c-4a8d-9467-5a7d9792fca0",
            "agent": "structurizr-python/1.0.0",
        },
        {
            "workspace_id": 19,
            "api_key": "7f4e4edc-f61c-4ff2-97c9-ea4bc2a7c98c",
            "api_secret": "ae140655-da7c-4a8d-9467-5a7d9792fca0",
            "workspace_archive_location": ".",
        },
        {
            "workspace_id": 19,
            "api_key": "7f4e4edc-f61c-4ff2-97c9-ea4bc2a7c98c",
            "api_secret": "ae140655-da7c-4a8d-9467-5a7d9792fca0",
            "workspace_archive_location": None,
        },
    ],
)
def test_init_from_arguments(attributes: dict):
    """Expect proper initialization from arguments."""
    settings = StructurizrClientSettings(**attributes)
    for attr, expected in attributes.items():
        value = getattr(settings, attr)
        if attr in ("api_key", "api_secret", "workspace_archive_location"):
            value = None if value is None else str(value)
        assert value == expected


def test_init_from_environment(mock_structurizr_env, archive_location):
    """Expect proper initialization from environment variables."""
    settings = StructurizrClientSettings()
    assert settings.url == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    assert settings.workspace_id == 19
    assert str(settings.api_key) == "7f4e4edc-f61c-4ff2-97c9-ea4bc2a7c98c"
    assert str(settings.api_secret) == "ae140655-da7c-4a8d-9467-5a7d9792fca0"
    assert settings.user == "astley@localhost"
    assert settings.agent == "structurizr-python/1.0.0"
    assert str(settings.workspace_archive_location) == archive_location


def test_init_from_dotenv(dotenv, archive_location):
    """Expect proper initialization from a `.env` file."""
    settings = StructurizrClientSettings()
    assert settings.url == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    assert settings.workspace_id == 19
    assert str(settings.api_key) == "7f4e4edc-f61c-4ff2-97c9-ea4bc2a7c98c"
    assert str(settings.api_secret) == "ae140655-da7c-4a8d-9467-5a7d9792fca0"
    assert settings.user == "astley@localhost"
    assert settings.agent == "structurizr-python/1.0.0"
    assert str(settings.workspace_archive_location) == archive_location
