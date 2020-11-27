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


"""Ensure the expected behaviour of DeploymentView."""

import pytest

from structurizr import Workspace
from structurizr.model import SoftwareSystem
from structurizr.view.deployment_view import DeploymentView


@pytest.fixture(scope="function")
def empty_workspace() -> Workspace:
    """Provide an empty Workspace on demand for test cases to use."""
    return Workspace(name="Name", description="Description")


def test_deployment_view_name_generation():
    """Test various forms of name are generated correctly."""
    deployment_view = DeploymentView(key="deployment", description="Description")
    assert deployment_view.name == "Deployment"

    deployment_view = DeploymentView(
        key="deployment", description="Description", environment="Live"
    )
    assert deployment_view.name == "Deployment - Live"

    software_system = SoftwareSystem(name="Software System")
    deployment_view = DeploymentView(
        key="deployment", description="Description", software_system=software_system
    )
    assert deployment_view.name == "Software System - Deployment"

    software_system = SoftwareSystem(name="Software System")
    deployment_view = DeploymentView(
        key="deployment",
        description="Description",
        software_system=software_system,
        environment="Live",
    )
    assert deployment_view.name == "Software System - Deployment - Live"


def test_deployment_view_add_all_deployment_nodes_no_top_level_nodes(
    empty_workspace: Workspace,
):
    """Test that if there are no top-level nodes then nothing is added."""
    deployment_view = empty_workspace.views.create_deployment_view(
        key="deployment", description="Description"
    )

    deployment_view.add_all_deployment_nodes()
    assert len(deployment_view.element_views) == 0


def test_deployment_view_add_all_deployment_nodes_no_container_instances(
    empty_workspace: Workspace,
):
    """Test that if there are no container instances then no nodes are added."""
    deployment_view = empty_workspace.views.create_deployment_view(
        key="deployment", description="Description"
    )
    empty_workspace.model.add_deployment_node(
        "Deployment Node", "Description", "Technology"
    )

    deployment_view.add_all_deployment_nodes()
    assert len(deployment_view.element_views) == 0


def test_deployment_view_add_all_deployment_nodes_wrong_enviroment(
    empty_workspace: Workspace,
):
    """Test that if the environment doesn't match then nodes aren't added."""
    software_system = empty_workspace.model.add_software_system("Software System")
    container = software_system.add_container("Container")
    deployment_node = empty_workspace.model.add_deployment_node("Deployment Node")
    deployment_node.add_container(container)

    deployment_view = empty_workspace.views.create_deployment_view(
        software_system=software_system,
        key="deployment",
        description="Description",
        environment="Live",
    )
    deployment_view.add_all_deployment_nodes()
    assert len(deployment_view.element_views) == 0


def test_deployment_view_add_all_deployment_nodes_with_container_instances(
    empty_workspace: Workspace,
):
    """Test adding child deployment nodes with container instances."""
    model = empty_workspace.model

    software_system = model.add_software_system("Software System")
    container = software_system.add_container("Container")
    deployment_node = model.add_deployment_node("Deployment Node")
    container_instance = deployment_node.add_container(container)

    deployment_view = empty_workspace.views.create_deployment_view(
        software_system=software_system,
        key="deployment",
        description="Description",
    )
    deployment_view.add_all_deployment_nodes()
    element_views = deployment_view.element_views
    assert len(element_views) == 2
    assert any([x.element is deployment_node for x in element_views])
    assert any([x.element is container_instance for x in element_views])


def test_deployment_view_add_all_deployment_nodes_with_child_container_instances(
    empty_workspace: Workspace,
):
    """Test adding child deployment nodes with container instances."""
    model = empty_workspace.model

    software_system = model.add_software_system("Software System")
    container = software_system.add_container("Container")
    parent_deployment_node = model.add_deployment_node("Deployment Node")
    child_deployment_node = parent_deployment_node.add_deployment_node("Child")
    container_instance = child_deployment_node.add_container(container)

    deployment_view = empty_workspace.views.create_deployment_view(
        software_system=software_system,
        key="deployment",
        description="Description",
    )
    deployment_view.add_all_deployment_nodes()
    element_views = deployment_view.element_views
    assert len(element_views) == 3
    assert any([x.element is parent_deployment_node for x in element_views])
    assert any([x.element is child_deployment_node for x in element_views])
    assert any([x.element is container_instance for x in element_views])


def test_deployment_view_add_all_deployment_nodes_only_adds_for_software_system(
    empty_workspace: Workspace,
):
    """Test adding all only adds for the in-scope software system."""
    model = empty_workspace.model

    software_system1 = model.add_software_system("Software System 1")
    container1 = software_system1.add_container("container 1")
    deployment_node1 = model.add_deployment_node("Deployment Node 1")
    containter_instance1 = deployment_node1.add_container(container1)

    software_system2 = model.add_software_system("Software System 2")
    container2 = software_system2.add_container("container 2")
    deployment_node2 = model.add_deployment_node("Deployment Node 2")
    deployment_node2.add_container(container2)

    # Two containers from different software systems on the same deployment node
    deployment_node1.add_container(container2)

    deployment_view = empty_workspace.views.create_deployment_view(
        software_system=software_system1, key="deployment", description="Description"
    )
    deployment_view.add_all_deployment_nodes()

    element_views = deployment_view.element_views
    assert len(element_views) == 2
    assert any([x.element is deployment_node1 for x in element_views])
    assert any([x.element is containter_instance1 for x in element_views])


def test_deployment_view_add_deployment_node_adds_parent(empty_workspace: Workspace):
    """Test adding a child deployment node adds the parent too."""
    model = empty_workspace.model
    software_system = model.add_software_system("Software System")
    container = software_system.add_container("Container")
    parent_deployment_node = model.add_deployment_node("Deployment Node")
    child_deployment_node = parent_deployment_node.add_deployment_node("Child")
    container_instance = child_deployment_node.add_container(container)

    deployment_view = empty_workspace.views.create_deployment_view(
        software_system=software_system, key="deployment", description="Description"
    )
    deployment_view.add(child_deployment_node)
    element_views = deployment_view.element_views
    assert len(element_views) == 3
    assert any([x.element is parent_deployment_node for x in element_views])
    assert any([x.element is child_deployment_node for x in element_views])
    assert any([x.element is container_instance for x in element_views])


# TODO: Animations

# TODO: Removing
