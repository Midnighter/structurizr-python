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

from structurizr.model.container_instance import ContainerInstance, ContainerInstanceIO
from structurizr.model.http_health_check import HTTPHealthCheck, HTTPHealthCheckIO
from structurizr.model.tags import Tags


class MockModel:
    """Implement a mock model for testing."""

    def __init__(self):
        """Create an mock container for testing."""
        self.mock_container = MockContainer()

    def __iadd__(self, instance: ContainerInstance):
        """Simulate the model assigning IDs to new elements."""
        if not instance.id:
            instance.id = "id"
        instance.set_model(self)
        return self

    def get_element(self, id: str):
        """Simulate fetching the container by ID."""
        return self.mock_container


class MockContainer:
    """Implement a mock container for testing."""

    def __init__(self):
        """Create a new mock."""
        self.id = "19"
        self.name = "Mock Container"


@pytest.fixture(scope="function")
def model_with_container() -> MockModel:
    """Provide a mock model for test cases to use."""
    return MockModel()


@pytest.mark.parametrize(
    "attributes",
    [
        pytest.param({}, marks=pytest.mark.raises(exception=TypeError)),
        {
            "environment": "Development",
            "container": MockContainer(),
            "instance_id": "17",
            "properties": {"a": "b"},
        },
    ],
)
def test_container_instance_init(attributes):
    """Expect proper initialization from arguments."""
    instance = ContainerInstance(**attributes)
    for attr, expected in attributes.items():
        assert getattr(instance, attr) == expected


def test_container_instance_tags(model_with_container):
    """Check default tags."""
    instance = ContainerInstance(
        container=model_with_container.mock_container, instance_id="11"
    )
    assert Tags.ELEMENT in instance.tags
    assert Tags.CONTAINER_INSTANCE in instance.tags


def test_container_instance_hydration_retrieves_container_from_id(model_with_container):
    """Check that the container instance is retrieved from the model on hydration."""
    io = ContainerInstanceIO(container_id="19", instance_id=3, environment="Live")

    instance = ContainerInstance.hydrate(io, model_with_container)

    assert instance.instance_id == 3
    assert instance.environment == "Live"
    assert instance.container is model_with_container.mock_container
    assert instance.container_id == "19"


def test_container_instance_name_is_container_name(model_with_container):
    """Ensure container instance takes its name from its container."""
    io = ContainerInstanceIO(container_id="19", instance_id=3, environment="Live")

    instance = ContainerInstance.hydrate(io, model_with_container)

    assert instance.name == "Mock Container"


def test_container_instance_hyrdates_http_health_checks(model_with_container):
    """Check that health checks are hydrated into the ContainerInstance."""
    health_check_io = HTTPHealthCheckIO(name="name", url="http://a.b.com")
    io = ContainerInstanceIO(
        container_id="19",
        instance_id=3,
        environment="Live",
        health_checks=[health_check_io],
    )

    instance = ContainerInstance.hydrate(io, model_with_container)

    assert len(instance.health_checks) == 1
    assert list(instance.health_checks)[0].name == "name"


def test_container_instance_serialization(model_with_container):
    """Test that container instances serialise properly."""
    health_check = HTTPHealthCheck(name="health", url="http://a.b.com")
    instance = ContainerInstance(
        container=model_with_container.mock_container,
        instance_id=7,
        health_checks=[health_check],
    )

    io = ContainerInstanceIO.from_orm(instance)

    assert io.container_id == "19"
    assert io.instance_id == 7
    assert len(io.health_checks) == 1
    assert io.health_checks[0].name == "health"
