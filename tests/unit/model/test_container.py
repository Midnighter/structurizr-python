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

from structurizr.model import Component, Container, Model


_model = (
    Model()
)  # Have to create outside the fixture so it doesn't get garbage-collected.


@pytest.fixture(scope="function")
def empty_container() -> Container:
    """Provide an empty Container on demand for test cases to use."""
    system = _model.add_software_system(name="Sys")
    return system.add_container(name="Container", description="Description")


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


def test_container_add_component_adds_to_component_list(empty_container: Container):
    """Verify add_component() adds the new component to Container.components."""
    component = empty_container.add_component(name="Component")
    assert component in empty_container.components
    assert component.id != ""
    assert component.model is _model
    assert component.parent is empty_container


def test_container_add_constructed_component(empty_container: Container):
    """Verify behaviour when adding a newly constructed Container."""
    component = Component(name="Component")
    empty_container += component
    assert component in empty_container.components
    assert component.id != ""
    assert component.model is _model
    assert component.parent is empty_container


def test_container_adding_component_twice_is_ok(empty_container: Container):
    """Defensive check that adding the same component twice is OK."""
    component = Component(name="Component")
    empty_container += component
    empty_container += component
    assert len(empty_container.components) == 1


def test_container_adding_component_with_same_name_fails(empty_container: Container):
    """Check that adding a component with the same name as an existing one fails."""
    empty_container.add_component(name="Component")
    with pytest.raises(ValueError, match="Component with name .* already exists"):
        empty_container.add_component(name="Component")
    with pytest.raises(ValueError, match="Component with name .* already exists"):
        empty_container += Component(name="Component")


def test_adding_component_with_existing_parent_fails(empty_container: Container):
    """Check that adding a component with a different parent fails."""
    container2 = empty_container.parent.add_container(
        name="Container 2", description="Description"
    )
    component = empty_container.add_component(name="Component")
    with pytest.raises(ValueError, match="Component with name .* already has parent"):
        container2 += component
