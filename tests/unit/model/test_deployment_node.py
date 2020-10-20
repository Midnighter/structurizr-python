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

from structurizr.model.deployment_node import DeploymentNode, DeploymentNodeIO


class MockModel:
    """Implement a mock model for testing."""

    def __init__(self):
        """Initialize the mock, creating an empty node for tests."""
        self.empty_node = DeploymentNode(name="Empty")
        self.empty_node.set_model(self)

    def __iadd__(self, node):
        """Simulate the model assigning IDs to new elements."""
        if not node.id:
            node.id = "id"
        node.set_model(self)
        return self


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
