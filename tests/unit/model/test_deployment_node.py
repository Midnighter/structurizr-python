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


"""Ensure the expected behaviour of the container element."""


import pytest

from structurizr.model import Container, SoftwareSystem
from structurizr.model.deployment_node import DeploymentNode, DeploymentNodeIO
from structurizr.model.infrastructure_node import InfrastructureNode


class MockModel:
    """Implement a mock model for testing."""

    def __init__(self):
        """Initialize the mock, creating an empty node for tests."""
        self.empty_node = DeploymentNode(name="Empty", environment="Live")
        self.empty_node.set_model(self)
        self.mock_element = MockElement("element")

    def __iadd__(self, node):
        """Simulate the model assigning IDs to new elements."""
        if not node.id:
            node.id = "id"
        node.set_model(self)
        return self

    def get_element(self, id: str):
        """Simulate getting an element by ID."""
        assert id == self.mock_element.id
        return self.mock_element

    def get_elements(self):
        """Simulate get_elements."""
        return []


class MockElement:
    """Implement a mock element for testing."""

    def __init__(self, name: str):
        """Initialise the mock."""
        self.name = name
        self.id = name


@pytest.fixture(scope="function")
def model_with_node() -> MockModel:
    """Provide an new empty model on demand for test cases to use."""
    return MockModel()


@pytest.mark.parametrize(
    "attributes",
    [
        pytest.param({}, marks=pytest.mark.raises(exception=TypeError)),
        {"name": "Node1", "technology": "tech1"},
    ],
)
def test_deployment_node_init(attributes):
    """Expect proper initialization from arguments."""
    node = DeploymentNode(**attributes)
    for attr, expected in attributes.items():
        assert getattr(node, attr) == expected


def test_deployment_node_adds_to_children(model_with_node):
    """Test adding a child node to an existing one."""
    top_node = model_with_node.empty_node
    child = top_node.add_deployment_node(name="child")

    assert child is not None
    assert child.model == model_with_node
    assert child.parent == top_node
    assert child in top_node.children


def test_deployment_node_adding_same_child_twice_is_ok(model_with_node):
    """Test adding the same child twice is just ignored."""
    top_node = model_with_node.empty_node
    child = top_node.add_deployment_node(name="child")
    top_node += child
    assert len(top_node.children) == 1


def test_deployment_node_add_child_with_existing_parent(model_with_node: MockModel):
    """Check that adding a node with an existing parent fails."""
    top_node = model_with_node.empty_node
    other_parent = DeploymentNode(name="OtherParent")
    with pytest.raises(ValueError, match="DeploymentNode .* already has parent."):
        top_node += DeploymentNode(name="child", parent=other_parent)


def test_deployment_node_cant_have_two_children_with_the_same_name(model_with_node):
    """Make sure you can't have two children with the same name in the same node."""
    top_node = model_with_node.empty_node
    top_node.add_deployment_node(name="child")
    with pytest.raises(
        ValueError,
        match="A deployment node with the name 'child' already exists in node 'Empty'.",
    ):
        top_node.add_deployment_node(name="child")


def test_deployment_node_serialization_of_recursive_nodes(model_with_node):
    """Check that nodes within nodes are handled with (de)serialisation."""
    top_node = model_with_node.empty_node
    top_node.add_deployment_node(name="child")

    io = DeploymentNodeIO.from_orm(top_node)
    assert len(io.children) == 1
    assert io.children[0].name == "child"

    new_top_node = DeploymentNode.hydrate(io, model_with_node)
    assert len(new_top_node.children) == 1
    new_child = new_top_node.children[0]
    assert new_child.name == "child"
    assert new_child.parent is new_top_node
    assert new_child.model is model_with_node


def test_deployment_node_add_container(model_with_node):
    """Test adding a container to a node to create an instance."""
    node = model_with_node.empty_node
    container = MockElement("element")

    instance = node.add_container(container, replicate_relationships=False)

    assert instance.container is container
    assert instance.environment == "Live"
    assert instance.model is model_with_node
    assert instance.parent is node
    assert instance in node.container_instances
    assert instance.instance_id == 1


def test_deployment_node_add_with_iadd(model_with_node: MockModel):
    """Test adding things to a node using += rather than add_container."""
    node = model_with_node.empty_node
    system = SoftwareSystem(name="system")
    model_with_node += system
    container = Container(name="container")
    system += container
    child_node = DeploymentNode(name="child")
    infra_node = InfrastructureNode(name="infra")

    node += child_node
    assert child_node in node.children

    node += system
    assert node.software_system_instances[0].software_system is system

    child_node += container
    assert child_node.container_instances[0].container is container

    child_node += infra_node
    assert infra_node in child_node.infrastructure_nodes


def test_deployment_node_serialising_container(model_with_node):
    """Test serialisation and deserialisation includes container instances."""
    node = model_with_node.empty_node
    container = model_with_node.mock_element
    node.add_container(container, replicate_relationships=False)

    io = DeploymentNodeIO.from_orm(node)

    assert len(io.container_instances) == 1
    assert io.container_instances[0].id == "id"

    node2 = DeploymentNode.hydrate(io, model_with_node)

    assert len(node2.container_instances) == 1
    instance = node2.container_instances[0]
    assert instance.instance_id == 1
    assert instance.container is container
    assert instance.model is model_with_node
    assert instance.parent is node2


def test_deployment_node_add_software_system(model_with_node):
    """Test adding a software system to a node to create an instance."""
    node = model_with_node.empty_node
    system = MockElement("element")

    instance = node.add_software_system(system, replicate_relationships=False)

    assert instance.software_system is system
    assert instance.environment == "Live"
    assert instance.model is model_with_node
    assert instance.parent is node
    assert instance in node.software_system_instances
    assert instance.instance_id == 1


def test_deployment_node_serialising_software_system(model_with_node):
    """Test serialisation and deserialisation includes container instances."""
    node = model_with_node.empty_node
    system = model_with_node.mock_element
    node.add_software_system(system, replicate_relationships=False)

    io = DeploymentNodeIO.from_orm(node)

    assert len(io.software_system_instances) == 1
    assert io.software_system_instances[0].id == "id"

    node2 = DeploymentNode.hydrate(io, model_with_node)

    assert len(node2.software_system_instances) == 1
    instance = node2.software_system_instances[0]
    assert instance.instance_id == 1
    assert instance.software_system is system
    assert instance.model is model_with_node
    assert instance.parent is node2


def test_deployment_node_add_infrastructure_node(model_with_node):
    """Test adding an infrastructure node to a deployment node."""
    node = model_with_node.empty_node

    infra_node = node.add_infrastructure_node("infraNode")

    assert infra_node.name == "infraNode"
    assert infra_node.model is model_with_node
    assert infra_node.parent is node
    assert infra_node in node.infrastructure_nodes


def test_deployment_node_serialising_infrastructure_nodes(model_with_node):
    """Test serialisation and deserialisation includes infrastructure nodes."""
    node = model_with_node.empty_node
    node.add_infrastructure_node("infraNode")

    io = DeploymentNodeIO.from_orm(node)

    assert len(io.infrastructure_nodes) == 1
    assert io.infrastructure_nodes[0].id == "id"
    assert io.infrastructure_nodes[0].name == "infraNode"

    node2 = DeploymentNode.hydrate(io, model_with_node)

    assert len(node2.infrastructure_nodes) == 1
    infra_node = node2.infrastructure_nodes[0]
    assert infra_node.name == "infraNode"
    assert infra_node.model is model_with_node
    assert infra_node.parent is node2
