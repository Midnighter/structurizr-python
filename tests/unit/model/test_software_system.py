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


"""Ensure the expected behaviour of the software system element."""


import pytest

from structurizr.model.container import Container
from structurizr.model.software_system import SoftwareSystem, SoftwareSystemIO


class MockModel:
    """Implement a mock model for testing."""

    def __init__(self):
        """Set up an empty system for testing."""
        self.empty_system = SoftwareSystem(name="Sys")
        self.empty_system.set_model(self)

    def __iadd__(self, container):
        """Simulate the model assigning IDs to new elements."""
        if not container.id:
            container.id = "id"
        container.set_model(self)
        return self


@pytest.fixture(scope="function")
def model_with_system() -> MockModel:
    """Provide a model and empty SoftwareSystem on demand for test cases to use."""
    return MockModel()


@pytest.mark.parametrize(
    "attributes",
    [
        pytest.param({}, marks=pytest.mark.raises(exception=TypeError)),
        {"name": "Banking System"},
    ],
)
def test_software_system_init(attributes):
    """Expect proper initialization from arguments."""
    system = SoftwareSystem(**attributes)
    for attr, expected in attributes.items():
        assert getattr(system, attr) == expected


def test_add_container_accepts_additional_args(model_with_system: MockModel):
    """Test keyword arguments (e.g. id) are allowed when adding a new container."""
    empty_system = model_with_system.empty_system
    container = empty_system.add_container("container", "description", id="id1")
    assert container.id == "id1"


def test_add_container_technology_is_optional(model_with_system: MockModel):
    """Ensure that you don't have to specify the technology."""
    empty_system = model_with_system.empty_system
    container = empty_system.add_container(name="Container", description="Description")
    assert container.technology == ""


def test_software_system_add_container_adds_to_container_list(
    model_with_system: MockModel,
):
    """Ensure that add_container() adds the container and sets up other properties."""
    empty_system = model_with_system.empty_system
    container = empty_system.add_container(name="Container", description="Description")
    assert container in empty_system.containers
    assert container.id != ""
    assert container.model is model_with_system
    assert container.parent is empty_system


def test_software_system_add_constructed_container(model_with_system: MockModel):
    """Verify behaviour when adding a newly constructed Container."""
    empty_system = model_with_system.empty_system
    container = Container(name="Container")
    empty_system += container
    assert container in empty_system.containers
    assert container.id != ""
    assert container.model is model_with_system
    assert container.parent is empty_system


def test_software_system_adding_container_twice_is_ok(model_with_system: MockModel):
    """Defensive check that adding the same container twice is OK."""
    empty_system = model_with_system.empty_system
    container = Container(name="Container")
    empty_system += container
    empty_system += container
    assert len(empty_system.containers) == 1


def test_software_system_adding_container_with_same_name_fails(
    model_with_system: MockModel,
):
    """Check that adding a container with the same name as an existing one fails."""
    empty_system = model_with_system.empty_system
    empty_system.add_container(name="Container", description="Description")
    with pytest.raises(ValueError, match="Container with name .* already exists"):
        empty_system.add_container(name="Container", description="Description2")
    with pytest.raises(ValueError, match="Container with name .* already exists"):
        empty_system += Container(name="Container", description="Description2")


def test_software_system_adding_container_with_existing_parent_fails(
    model_with_system: MockModel,
):
    """Check that adding a container with a (different) parent fails."""
    empty_system = model_with_system.empty_system
    system2 = SoftwareSystem(name="System 2", description="Description")
    system2.set_model(empty_system.model)

    container = empty_system.add_container(name="Container", description="Description")
    with pytest.raises(ValueError, match="Container with name .* already has parent"):
        system2 += container


def test_software_system_get_container_with_name(model_with_system: MockModel):
    """Test getting containers by name."""
    empty_system = model_with_system.empty_system
    container = empty_system.add_container(name="Test", description="Description")
    assert empty_system.get_container_with_name("Test") is container
    assert empty_system.get_container_with_name("FooBar") is None


def test_software_system_serialisation(model_with_system: MockModel):
    """Test systems are deserialised correctly."""
    empty_system = model_with_system.empty_system
    empty_system.add_container(name="Test", description="Description")

    system_io = SoftwareSystemIO.from_orm(empty_system)

    new_system = SoftwareSystem.hydrate(system_io, model_with_system)
    assert new_system.name == "Sys"
    assert len(new_system.containers) == 1
    container = next(iter(new_system.containers))
    assert container.name == "Test"
    assert container.parent is new_system
