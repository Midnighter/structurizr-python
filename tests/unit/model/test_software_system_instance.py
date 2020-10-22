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


"""Ensure the expected behaviour of the software_system element."""


import pytest

from structurizr.model.http_health_check import HTTPHealthCheck, HTTPHealthCheckIO
from structurizr.model.software_system_instance import (
    SoftwareSystemInstance,
    SoftwareSystemInstanceIO,
)


class MockModel:
    """Implement a mock model for testing."""

    def __init__(self):
        """Create an mock software_system for testing."""
        self.mock_system = MockSystem()

    def __iadd__(self, instance: SoftwareSystemInstance):
        """Simulate the model assigning IDs to new elements."""
        if not instance.id:
            instance.id = "id"
        instance.set_model(self)
        return self

    def get_element(self, id: str):
        """Simulate fetching the software_system by ID."""
        return self.mock_system


class MockSystem:
    """Implement a mock system for testing."""

    def __init__(self):
        """Create a new mock."""
        self.id = "19"
        self.name = "Mock System"


@pytest.fixture(scope="function")
def model_with_system() -> MockModel:
    """Provide a mock model for test cases to use."""
    return MockModel()


@pytest.mark.parametrize(
    "attributes",
    [
        pytest.param({}, marks=pytest.mark.raises(exception=TypeError)),
        {
            "environment": "Development",
            "software_system": MockSystem(),
            "instance_id": "17",
            "properties": {"a": "b"},
        },
    ],
)
def test_software_system_instance_init(attributes):
    """Expect proper initialization from arguments."""
    instance = SoftwareSystemInstance(**attributes)
    for attr, expected in attributes.items():
        assert getattr(instance, attr) == expected


def test_software_system_instance_hydration_retrieves_software_system_from_id(
    model_with_system,
):
    """Check that the software_system instance is retrieved on hydration."""
    io = SoftwareSystemInstanceIO(
        software_system_id="19", instance_id=3, environment="Live"
    )

    instance = SoftwareSystemInstance.hydrate(io, model_with_system)

    assert instance.instance_id == 3
    assert instance.environment == "Live"
    assert instance.software_system is model_with_system.mock_system
    assert instance.software_system_id == "19"


def test_software_system_instance_name_is_software_system_name(model_with_system):
    """Ensure software_system instance takes its name from its software system."""
    io = SoftwareSystemInstanceIO(
        software_system_id="19", instance_id=3, environment="Live"
    )

    instance = SoftwareSystemInstance.hydrate(io, model_with_system)

    assert instance.name == "Mock System"


def test_software_system_instance_hyrdates_http_health_checks(model_with_system):
    """Check that health checks are hydrated into the SoftwareSystemInstance."""
    health_check_io = HTTPHealthCheckIO(name="name", url="http://a.b.com")
    io = SoftwareSystemInstanceIO(
        software_system_id="19",
        instance_id=3,
        environment="Live",
        health_checks=[health_check_io],
    )

    instance = SoftwareSystemInstance.hydrate(io, model_with_system)

    assert len(instance.health_checks) == 1
    assert list(instance.health_checks)[0].name == "name"


def test_software_system_instance_serialization(model_with_system):
    """Test that system instances serialise properly."""
    health_check = HTTPHealthCheck(name="health", url="http://a.b.com")
    instance = SoftwareSystemInstance(
        software_system=model_with_system.mock_system,
        instance_id=7,
        health_checks=[health_check],
    )

    io = SoftwareSystemInstanceIO.from_orm(instance)

    assert io.software_system_id == "19"
    assert io.instance_id == 7
    assert len(io.health_checks) == 1
    assert io.health_checks[0].name == "health"
