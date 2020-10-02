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

from structurizr.model import Component, Container, Model, SoftwareSystem


_model = Model()
_system = _model.add_software_system(name="Sys")


@pytest.fixture(scope="function")
def empty_container() -> Container:
    """Provide an empty Container on demand for test cases to use."""
    return _system.add_container(name="Container", description="Description")


@pytest.mark.parametrize(
    "attributes",
    [
        pytest.param({}, marks=pytest.mark.raises(exception=TypeError)),
        {"name": "Mobile App", "parent": _system, "technology": "tech1"},
    ],
)
def test_container_init(attributes):
    """Expect proper initialization from arguments."""
    container = Container(**attributes)
    for attr, expected in attributes.items():
        assert getattr(container, attr) == expected


def test_container_add_component_adds_to_component_list(empty_container: Container):
    """Ensure that add_component() adds the new component to Container.components and sets up other properties."""
    component = empty_container.add_component(name="Component")
    assert component in empty_container.components
    assert component.id != ""
    assert component.model is _model
    assert component.parent is empty_container


@pytest.mark.xfail(strict=True)
def test_container_add_constructed_component(empty_container: Container):
    """Verify behaviour when adding a newly constructed Container rather than calling add_container()."""
    component = Component(name="Component")
    empty_container.add(component)
    assert component in empty_container.components
    assert component.id != ""  # Currently failing
    assert component.model is _model  # Currently failing
    assert component.parent is empty_container  # Currently failing


def test_container_adding_component_twice_is_ok(empty_container: Container):
    """Defensive check that adding the same component twice is OK."""
    component = Component(name="Component")
    empty_container.add(component)
    empty_container.add(component)
    assert len(empty_container.components) == 1


@pytest.mark.xfail(strict=True)
def test_container_adding_component_with_same_name_fails(empty_container: Container):
    """Defensive check that adding a component with the same name as an existing one fails."""
    empty_container.add_component(name="Component")
    with pytest.raises(ValueError, match="Component with name .* already exists"):
        empty_container.add_component(name="Component")
    with pytest.raises(ValueError, match="Component with name .* already exists"):
        empty_container.add(Component(name="Component"))  # Doesn't currently raise


@pytest.mark.xfail(strict=True)
def test_adding_component_with_existing_parent_fails(empty_container: Container):
    """Defensive check that if a component already has a (different) parent then it can't be added."""
    container2 = _system.add_container(name="Container 2", description="Description")
    component = empty_container.add_component(name="Component")
    with pytest.raises(ValueError):
        container2.add(component)  # Doesn't currently raise
