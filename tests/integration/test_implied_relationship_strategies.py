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

"""Test the various strategies for adding implied relationships."""

import pytest

from structurizr.model import InteractionStyle, Model
from structurizr.model.implied_relationship_strategies import (
    create_implied_relationships_unless_any_exist as create_unless_any_exist,
)
from structurizr.model.implied_relationship_strategies import (
    create_implied_relationships_unless_same_exists as create_unless_same_exists,
)
from structurizr.model.implied_relationship_strategies import (
    ignore_implied_relationship_strategy as ignore,
)


def test_by_default_model_doesnt_create_implied_relationships():
    """Check if not set on Model, no implied relationships are added."""
    model = Model()
    assert model.implied_relationship_strategy is None

    system1 = model.add_software_system(name="system1")
    container1 = system1.add_container(name="container1", description="test")
    system2 = model.add_software_system(name="system2")
    container2 = system2.add_container(name="container2", description="test")

    rel = container1.uses(container2, "Uses")

    assert len(list(container1.get_relationships())) == 1
    assert len(list(system1.get_relationships())) == 0
    assert set(container1.get_relationships()) == {rel}
    assert set(system1.get_relationships()) == set()


def test_ignore_implied_relationship_strategy():
    """Check that by default no implied relationships are added."""
    model = Model(implied_relationship_strategy=ignore)
    system1 = model.add_software_system(name="system1")
    container1 = system1.add_container(name="container1", description="test")
    system2 = model.add_software_system(name="system2")
    container2 = system2.add_container(name="container2", description="test")

    rel = container1.uses(container2, "Uses")

    assert len(list(container1.get_relationships())) == 1
    assert len(list(system1.get_relationships())) == 0
    assert set(container1.get_relationships()) == {rel}
    assert set(system1.get_relationships()) == set()


def test_create_implied_relationships_unless_any_exist():
    """Check logic of create_implied_relationships_unless_any_exist."""
    model = Model(implied_relationship_strategy=create_unless_any_exist)
    system1 = model.add_software_system(name="system1")
    container1 = system1.add_container(name="container1", description="test")
    component1 = container1.add_component(name="component1", description="test")
    system2 = model.add_software_system(name="system2")
    container2 = system2.add_container(name="container2", description="test")
    component2 = container2.add_component(name="component2", description="test")

    component1.uses(component2, "Uses")

    # We should now have every *1 element related to every *2 element
    assert len(list(component1.get_relationships())) == 3
    assert len(list(container1.get_relationships())) == 3
    assert len(list(system1.get_relationships())) == 3
    assert any(rel.destination is component2 for rel in component1.get_relationships())
    assert any(rel.destination is container2 for rel in component1.get_relationships())
    assert any(rel.destination is system2 for rel in component1.get_relationships())
    assert any(rel.destination is component2 for rel in container1.get_relationships())
    assert any(rel.destination is container2 for rel in container1.get_relationships())
    assert any(rel.destination is system2 for rel in container1.get_relationships())
    assert any(rel.destination is component2 for rel in system1.get_relationships())
    assert any(rel.destination is container2 for rel in system1.get_relationships())
    assert any(rel.destination is system2 for rel in system1.get_relationships())

    # Now add another relationship, which shouldn't copy upwards as some already exist
    container1.uses(container2, "Uses differently")
    assert len(list(container1.get_relationships())) == 4  # 3 from before plus new one
    assert len(list(system1.get_relationships())) == 3  # Same as before


def test_create_implied_relationships_unless_same_exists():
    """Check logic of create_implied_relationships_unless_same_exists."""
    model = Model(implied_relationship_strategy=create_unless_same_exists)

    system1 = model.add_software_system(name="system1")
    container1 = system1.add_container(name="container1", description="test")
    system2 = model.add_software_system(name="system2")

    system1.uses(system2, "Reads from")
    assert len(list(system1.get_relationships())) == 1
    container1.uses(system2, "Reads from")
    assert len(list(system1.get_relationships())) == 1
    container1.uses(system2, "Writes to")
    assert len(list(system1.get_relationships())) == 2


def test_suppressing_implied_relationships():
    """Ensure you can explicitly suppress the current strategy."""
    model = Model(implied_relationship_strategy=create_unless_any_exist)
    system1 = model.add_software_system(name="system1")
    container1 = system1.add_container(name="container1", description="test")
    system2 = model.add_software_system(name="system2")
    container2 = system2.add_container(name="container2", description="test")

    rel = container1.uses(container2, "Uses", create_implied_relationships=False)

    assert len(list(container1.get_relationships())) == 1
    assert len(list(system1.get_relationships())) == 0
    assert set(container1.get_relationships()) == {rel}
    assert set(system1.get_relationships()) == set()


@pytest.mark.parametrize(
    "strategy",
    [
        create_unless_any_exist,
        create_unless_same_exists,
    ],
)
def test_self_references_are_not_implied(strategy):
    """Ensure references from an element to itself don't get implied to parents."""
    model = Model(implied_relationship_strategy=strategy)
    system1 = model.add_software_system(name="system1")
    container1 = system1.add_container(name="container1", description="test")

    container1.uses(container1, "Uses")

    assert len(list(container1.get_relationships())) == 1
    assert len(list(system1.get_relationships())) == 0


def test_cloning_to_implied_relationship_copies_attributes_across():
    """Make sure that attributes carry over to implied relationships."""
    model = Model(implied_relationship_strategy=create_unless_any_exist)
    system1 = model.add_software_system(name="system1")
    container1 = system1.add_container(name="container1", description="test")
    system2 = model.add_software_system(name="system2")
    container2 = system2.add_container(name="container2", description="test")

    rel = container1.uses(
        container2,
        "Uses",
        technology="tech1",
        interaction_style=InteractionStyle.Asynchronous,
        tags="tag1,tag2",
        properties={"prop1": "val1"},
    )

    new_rel = next(system1.get_relationships())

    assert new_rel.description == "Uses"
    assert new_rel.technology == "tech1"
    assert new_rel.tags == rel.tags
    assert new_rel.properties == rel.properties
