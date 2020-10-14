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

from structurizr.model import Component, Container, ContainerIO


class MockModel:
    """Implement a mock model for testing."""

    def __init__(self):
        """Create an empty container for testing."""
        self.empty_container = Container(name="Container", description="Description")
        self.empty_container.set_model(self)

    def add(self, component):
        """Simulate the model assigning IDs to new elements."""
        if not component.id:
            component.id = "id"
        component.set_model(self)


@pytest.fixture(scope="function")
def model_with_container() -> MockModel:
    """Provide a model with an empty Container on demand for test cases to use."""
    return MockModel()


@pytest.mark.parametrize(
    "attributes",
    [
        pytest.param({}, marks=pytest.mark.raises(exception=TypeError)),
        {"name": "Mobile App", "technology": "tech1"},
    ],
)
def test_container_init(attributes):
    """Expect proper initialization from arguments."""
    container = Container(**attributes)
    for attr, expected in attributes.items():
        assert getattr(container, attr) == expected


def test_container_add_component_adds_to_component_list(
    model_with_container: MockModel,
):
    """Verify add_component() adds the new component to Container.components."""
    empty_container = model_with_container.empty_container
    component = empty_container.add_component(name="Component")
    assert component in empty_container.components
    assert component.id != ""
    assert component.model is model_with_container
    assert component.parent is empty_container


def test_container_add_constructed_component(model_with_container: MockModel):
    """Verify behaviour when adding a newly constructed Container."""
    empty_container = model_with_container.empty_container
    component = Component(name="Component")
    empty_container += component
    assert component in empty_container.components
    assert component.id != ""
    assert component.model is model_with_container
    assert component.parent is empty_container


def test_container_adding_component_twice_is_ok(model_with_container: MockModel):
    """Defensive check that adding the same component twice is OK."""
    empty_container = model_with_container.empty_container
    component = Component(name="Component")
    empty_container += component
    empty_container += component
    assert len(empty_container.components) == 1


def test_container_adding_component_with_same_name_fails(
    model_with_container: MockModel,
):
    """Check that adding a component with the same name as an existing one fails."""
    empty_container = model_with_container.empty_container
    empty_container.add_component(name="Component")
    with pytest.raises(ValueError, match="Component with name .* already exists"):
        empty_container.add_component(name="Component")
    with pytest.raises(ValueError, match="Component with name .* already exists"):
        empty_container += Component(name="Component")


def test_adding_component_with_existing_parent_fails(model_with_container: MockModel):
    """Check that adding a component with a different parent fails."""
    empty_container = model_with_container.empty_container
    container2 = Container(name="Container 2", description="Description")
    component = empty_container.add_component(name="Component")
    with pytest.raises(ValueError, match="Component with name .* already has parent"):
        container2 += component


def test_serialisation_of_child_components(model_with_container: MockModel):
    """Make sure that components are serialised even though read-only."""
    container = Container(name="Container", description="Description")
    container.set_model(model_with_container)
    container.add_component(name="Component")
    io = ContainerIO.from_orm(container)

    assert len(io.components) == 1
    assert io.components[0].name == "Component"
