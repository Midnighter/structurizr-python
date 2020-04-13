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


"""Ensure a consistent public package interface."""


import gzip
from collections import namedtuple

import pytest

from structurizr import StructurizrClient, StructurizrClientSettings, Workspace


MockSettings = namedtuple(
    "MockSettings", "url workspace_id api_key api_secret user agent"
)


@pytest.fixture(scope="module")
def archive_location(tmp_path_factory):
    location = tmp_path_factory.mktemp("structurizr")
    return str(location)


@pytest.fixture(scope="module")
def settings(archive_location):
    """Provide the settings for the official Structurizr test workspace."""
    return StructurizrClientSettings(
        workspace_id=20081,
        api_key="81ace434-94a1-486f-a786-37bbeaa44e08",
        api_secret="a8673e21-7b6f-4f52-be65-adb7248be86b",
        workspace_archive_location=archive_location,
    )


def test_interact_with_workspace_without_encryption(settings):
    # Set up a toy workspace.
    workspace = Workspace(
        id=settings.workspace_id,
        name="structurizr-python e2e-tests - without encryption",
        description="A test workspace for the Structurizr Python client.",
    )
    system = workspace.model.add_software_system(
        name="Software System", description="Description"
    )
    person = workspace.model.add_person(name="Person", description="Description")
    person.uses(system, "")
    context_view = workspace.views.create_system_context_view(
        software_system=system, key="SystemContext", description="Description"
    )
    context_view.add_all_elements()
    # Upload the workspace and immediately retrieve it again.
    with StructurizrClient(settings=settings) as client:
        client.put_workspace(workspace)
        remote_ws = client.get_workspace()
    # Verify the remote workspace.
    assert remote_ws.model.get_software_system_with_name("Software System") is not None
    assert remote_ws.model.get_person_with_name("Person") is not None
    assert len(remote_ws.model.relationships) == 1
    assert len(remote_ws.views.get_system_context_views()) == 1
    # Verify the generated archive.
    archives = list(settings.workspace_archive_location.glob("*.json.gz"))
    assert len(archives) == 1
    with gzip.open(archives[0], mode="rt") as handle:
        archived_ws: Workspace = Workspace.parse_raw(handle.read())
    assert archived_ws.id == 20081
    assert archived_ws.name == "structurizr-python e2e-tests - without encryption"
    assert len(archived_ws.model.software_systems) == 1


def test_lock_workspace(settings):
    client = StructurizrClient(settings=settings)
    client.unlock_workspace()
    assert client.lock_workspace()
    client.close()


def test_unlock_workspace(settings):
    client = StructurizrClient(settings=settings)
    client.lock_workspace()
    assert client.unlock_workspace()
    client.close()
