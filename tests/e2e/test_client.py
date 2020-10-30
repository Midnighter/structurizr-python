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


import os

import pytest

from structurizr import StructurizrClient, StructurizrClientSettings, Workspace


if not (
    os.getenv("SECRET_WORKSPACE_ID")
    and os.getenv("SECRET_API_KEY")
    and os.getenv("SECRET_API_SECRET")
):
    pytest.skip(
        "The e2e tests require setting the secret environment variables with the "
        "workspace credentials.",
        allow_module_level=True,
    )


@pytest.fixture(scope="module")
def archive_location(tmp_path_factory):
    """Provide a path for archive files for test cases."""
    location = tmp_path_factory.mktemp("structurizr")
    return str(location)


@pytest.fixture(scope="module")
def settings(archive_location):
    """Provide the settings with values taken from the environment."""
    return StructurizrClientSettings(
        workspace_id=os.getenv("SECRET_WORKSPACE_ID"),
        api_key=os.getenv("SECRET_API_KEY"),
        api_secret=os.getenv("SECRET_API_SECRET"),
        workspace_archive_location=archive_location,
    )


def test_empty_workspace_without_encryption(settings):
    """Test basic upload and download of an empty workspace."""
    workspace = Workspace(
        id=settings.workspace_id,
        name="e2e-tests - without encryption",
        description="A test workspace for the structurizr-python client.",
    )
    with StructurizrClient(settings=settings) as client:
        client.put_workspace(workspace)
        remote_ws = client.get_workspace()
    assert remote_ws.name == workspace.name
    assert remote_ws.description == workspace.description


def test_interact_with_workspace_without_encryption(settings):
    """Test basic upload and download of a populated workspace."""
    # Set up a toy workspace.
    workspace = Workspace(
        id=settings.workspace_id,
        name="e2e-tests - without encryption",
        description="A test workspace for the structurizr-python client.",
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
    archived_ws: Workspace = Workspace.load(archives[0])
    assert archived_ws.id == 20081
    assert archived_ws.name == "structurizr-python e2e-tests - without encryption"
    assert len(archived_ws.model.software_systems) == 1


def test_lock_workspace(settings):
    """Check locking a workspace."""
    client = StructurizrClient(settings=settings)
    client.unlock_workspace()
    assert client.lock_workspace()
    client.close()


def test_unlock_workspace(settings):
    """Check unlocking a workspace."""
    client = StructurizrClient(settings=settings)
    client.lock_workspace()
    assert client.unlock_workspace()
    client.close()
