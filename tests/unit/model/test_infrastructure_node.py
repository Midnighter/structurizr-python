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

from structurizr.model.infrastructure_node import (
    InfrastructureNode,
    InfrastructureNodeIO,
)
from structurizr.model.tags import Tags


class MockModel:
    """Implement a mock model for testing."""

    def __init__(self):
        """Initialize the mock."""
        pass

    def __iadd__(self, node):
        """Simulate the model assigning IDs to new elements."""
        if not node.id:
            node.id = "id"
        node.set_model(self)
        return self


@pytest.fixture(scope="function")
def empty_model() -> MockModel:
    """Provide an new empty model on demand for test cases to use."""
    return MockModel()


@pytest.mark.parametrize(
    "attributes",
    [
        pytest.param({}, marks=pytest.mark.raises(exception=TypeError)),
        {"name": "Node1", "technology": "tech1"},
    ],
)
def test_infrastructure_node_init(attributes):
    """Expect proper initialization from arguments."""
    node = InfrastructureNode(**attributes)
    for attr, expected in attributes.items():
        assert getattr(node, attr) == expected


def test_infrastructure_node_tags():
    """Check default tags."""
    node = InfrastructureNode(name="Node")
    assert Tags.ELEMENT in node.tags
    assert Tags.INFRASTRUCTURE_NODE in node.tags


def test_infrastructure_node_hydration():
    """Check hydrating an infrastructure node from its IO."""
    io = InfrastructureNodeIO(name="node1", technology="tech")
    parent = object()

    node = InfrastructureNode.hydrate(io, parent=parent)

    assert node.name == "node1"
    assert node.technology == "tech"
    assert node.parent is parent
