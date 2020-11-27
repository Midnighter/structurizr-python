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


"""Ensure the expected behaviour of the model."""


import pytest

from structurizr.model import Component, Container, Model, Person, SoftwareSystem
from structurizr.model.deployment_node import DeploymentNode


@pytest.fixture(scope="function")
def empty_model() -> Model:
    """Provide an empty Model on demand for test cases to use."""
    return Model()


def test_model_get_relationship_by_id(empty_model: Model):
    """Test retrieving relationships by their IDs."""
    sys1 = empty_model.add_software_system(name="sys1")
    sys2 = empty_model.add_software_system(name="sys2")
    relationship = empty_model.add_relationship(source=sys1, destination=sys2, id="r1")
    assert empty_model.get_relationship("r1") is relationship


def test_model_add_relationship_twice_ignored(empty_model: Model):
    """Ensure that adding an existing relationship to the Model makes no difference."""
    sys1 = empty_model.add_software_system(name="sys1")
    sys2 = empty_model.add_software_system(name="sys2")
    relationship = empty_model.add_relationship(source=sys1, destination=sys2)
    assert set(empty_model.get_relationships()) == {relationship}
    empty_model.add_relationship(relationship)
    assert set(empty_model.get_relationships()) == {relationship}


def test_model_cannot_add_relationship_with_same_id_as_existing(empty_model: Model):
    """Ensure you can't add two relationships with the same ID."""
    sys1 = empty_model.add_software_system(name="sys1")
    sys2 = empty_model.add_software_system(name="sys2")
    empty_model.add_relationship(source=sys1, destination=sys2, id="r1")
    with pytest.raises(
        ValueError, match="Relationship.* has the same ID as Relationship.*"
    ):
        empty_model.add_relationship(source=sys1, destination=sys2, id="r1")


def test_model_cannot_add_relationship_with_same_id_as_element(empty_model: Model):
    """Ensure you can't add a relationship with the same ID as an element."""
    sys1 = empty_model.add_software_system(name="sys1")
    sys2 = empty_model.add_software_system(name="sys2")
    with pytest.raises(
        ValueError, match="Relationship.* has the same ID as SoftwareSystem.*"
    ):
        empty_model.add_relationship(source=sys1, destination=sys2, id=sys1.id)


def test_model_add_component_must_have_parent(empty_model: Model):
    """Ensure that Model rejects adding Components that aren't within a Container."""
    component = Component(name="c1")
    with pytest.raises(ValueError, match="Element with name .* has no parent"):
        empty_model += component


def test_model_add_container_must_have_parent(empty_model: Model):
    """Ensure Model rejects adding Containers that aren't within a SoftwareSystem."""
    container = Container(name="c1")
    with pytest.raises(ValueError, match="Element with name .* has no parent"):
        empty_model += container


def test_model_add_top_level_deployment_node(empty_model: Model):
    """Make sure top-level deployment nodes are reflected in Model.deployent_nodes."""
    node = empty_model.add_deployment_node(name="node1")
    assert node is not None
    assert node in empty_model.deployment_nodes
    assert node in empty_model.get_elements()


def test_model_cant_add_two_deployment_nodes_with_same_name(empty_model: Model):
    """Make sure that deployment nodes at the top level can't have the same name.

    Unless they're in different environments.
    """
    empty_model.add_deployment_node(name="node1", environment="Live")
    empty_model.add_deployment_node(name="node1", environment="Dev")  # Different env
    with pytest.raises(
        ValueError,
        match="A deployment node with the name 'node1' already "
        "exists in environment 'Live' of the model.",
    ):
        empty_model.add_deployment_node(name="node1", environment="Live")


def test_model_add_lower_level_deployment_node(empty_model: Model):
    """Make sure child deployment nodes are not reflected in Model.deployent_nodes."""
    node1 = empty_model.add_deployment_node(name="node1")
    node2 = DeploymentNode(name="node2", parent=node1)
    empty_model += node2
    assert node2 not in empty_model.deployment_nodes
    assert node2 in empty_model.get_elements()


def test_model_add_person_with_plusequals(empty_model: Model):
    """Check that adding a Person to a Model with += works."""
    bob = Person(name="Bob")
    empty_model += bob
    assert bob in empty_model.people
    assert bob.id != ""


def test_model_add_software_system_with_plusequals(empty_model: Model):
    """Check that adding a SoftwareSystem to a Model with += works."""
    sys = SoftwareSystem(name="Sys")
    empty_model += sys
    assert sys in empty_model.software_systems
    assert sys.id != ""


def test_model_can_add_elements_with_plusequals(
    empty_model: Model,
):
    """Ensure passing something other than a Person or SoftwareSystem to += works."""
    sys = SoftwareSystem(name="Sys")
    c = Container(name="C")
    c.parent = sys
    empty_model += c
    assert c in empty_model.get_elements()


def test_model_cannot_add_two_people_with_same_name(empty_model: Model):
    """Ensure duplicate people are not allowed."""
    empty_model.add_person(name="Bob")
    with pytest.raises(
        ValueError, match="A person with the name 'Bob' already exists in the model."
    ):
        empty_model.add_person(name="Bob")


def test_model_cannot_add_two_software_systems_with_same_name(empty_model: Model):
    """Ensure duplicate software systems are not allowed."""
    empty_model.add_software_system(name="Bob")
    with pytest.raises(
        ValueError,
        match="A software system with the name 'Bob' already exists in the model.",
    ):
        empty_model.add_software_system(name="Bob")


def test_model_get_software_system_bad_id(empty_model: Model):
    """Test that trying to get a system by a non-system ID returns None."""
    system = empty_model.add_software_system(name="System")
    container = system.add_container(name="Container")

    assert empty_model.get_software_system_with_id(container.id) is None


def test_model_add_element_twice_is_ignored(empty_model: Model):
    """Test you can't add an element with the same ID as an existing one."""
    system1 = empty_model.add_software_system(name="System")
    empty_model += system1
    assert empty_model.software_systems == {system1}


def test_model_add_element_with_existing_id_raises_error(empty_model: Model):
    """Test you can't add an element with the same ID as an existing one."""
    system1 = empty_model.add_software_system(name="System")
    system2 = SoftwareSystem(name="System2", id=system1.id)

    with pytest.raises(ValueError, match="The element .* has an existing ID"):
        empty_model += system2


def test_model_automatically_adds_child_elements(empty_model: Model):
    """Check that adding a parent element to the model also adds its children."""
    system = SoftwareSystem(name="System")
    container = system.add_container(name="Container")

    assert not container.has_model
    empty_model += system
    assert container.has_model
