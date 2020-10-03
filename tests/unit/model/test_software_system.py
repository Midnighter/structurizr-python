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

from structurizr.model.model import Model
from structurizr.model.container import Container
from structurizr.model.software_system import SoftwareSystem


@pytest.fixture(scope="function")
def empty_model() -> Model:
    """Provide an empty Model on demand for test cases to use."""
    return Model()


@pytest.fixture(scope="function")
def empty_system() -> SoftwareSystem:
    """Provide an empty SoftwareSystem on demand for test cases to use."""
    return Model().add_software_system("Sys")


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


def test_add_container_accepts_additional_args():
    """Test keyword arguments (e.g. id) are allowed when adding a new container."""
    model = Model()
    system = model.add_software_system(name="Banking System")
    container = system.add_container("container", "description", id="id1")
    assert container.id == "id1"


def test_add_container_technology_is_optional(empty_model: Model):
    """Ensure that you don't have to specify the technology."""
    system = empty_model.add_software_system(name="sys")
    container = system.add_container(name="Container", description="Description")
    assert container.technology == ""

    
@pytest.mark.xfail(strict=True)
def test_software_system_add_container_adds_to_container_list(empty_system: SoftwareSystem):
    """Ensure that add_container() adds the new container to SoftwareSystem.containers and sets up other properties."""
    container = empty_system.add_container(name="Container", description="Description")
    assert container in empty_system.containers
    assert container.id != ""
    assert container.model is empty_system.model
    assert container.parent is empty_system


@pytest.mark.xfail(strict=True)
def test_software_system_add_constructed_container(empty_system: SoftwareSystem):
    """Verify behaviour when adding a newly constructed Container rather than calling add_container()."""
    container = Container(name="Container")
    empty_system += container
    assert container in empty_system.containers
    assert container.id != ""
    assert container.model is empty_system.model
    assert container.parent is empty_system


@pytest.mark.xfail(strict=True)
def test_software_system_adding_container_twice_is_ok(empty_system: SoftwareSystem):
    """Defensive check that adding the same container twice is OK."""
    container = Container(name="Container")
    empty_system += container
    empty_system += container
    assert len(empty_system.containers) == 1


@pytest.mark.xfail(strict=True)
def test_software_system_adding_container_with_same_name_fails(empty_system: SoftwareSystem):
    """Defensive check that adding a container with the same name as an existing one fails."""
    empty_system.add_container(name="Container")
    with pytest.raises(ValueError, match="Container with name .* already exists"):
        empty_system.add_container(name="Container")
    with pytest.raises(ValueError, match="Container with name .* already exists"):
        empty_system += Container(name="Container")


@pytest.mark.xfail(strict=True)
def test_software_system_adding_container_with_existing_parent_fails(empty_system: SoftwareSystem):
    """Defensive check that if a container already has a (different) parent then it can't be added."""
    system2 = empty_system.model.add_software_system(name="System 2", description="Description")
    container = empty_system.add_container(name="Container")
    with pytest.raises(ValueError, match="Container with name .* already has parent"):
        system2 += container
