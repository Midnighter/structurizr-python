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

"""Ensure the correct behaviour of DynamicView."""


import pytest

from structurizr.model import Container, Model, SoftwareSystem
from structurizr.view.dynamic_view import DynamicView, DynamicViewIO


@pytest.fixture(scope="function")
def empty_model() -> Model:
    """Provide an empty Model on demand for test cases to use."""
    yield Model()


@pytest.fixture(scope="function")
def empty_view(empty_model) -> DynamicView:
    """Provide an empty DynamicView on demand for test cases to use."""
    view = DynamicView(key="dyn1", description="Dynamic view")
    view.set_model(empty_model)
    yield view


def test_create_new_dynamic_view(empty_model: Model):
    """Test basic construction."""
    view = DynamicView(description="Test view")
    assert view.description == "Test view"
    view.set_model(empty_model)
    assert view.model is empty_model


def test_constructor_param_validation():
    """Test validation of constructor parameters."""
    system = SoftwareSystem(name="sys1")
    container = Container(name="con1", parent=system)

    view1 = DynamicView(description="Description")
    assert view1.element is None
    view2 = DynamicView(description="Description", element=system)
    assert view2.element is system
    view3 = DynamicView(description="Description", element=container)
    assert view3.element is container


def test_specifying_software_system_explicitly_fails(empty_model: Model):
    """Check enforcement of passing software_system through element argument."""
    model = empty_model
    system1 = model.add_software_system(name="System 1", id="sys1")
    with pytest.raises(ValueError):
        DynamicView(software_system=system1, description="test")


def test_adding_relationships_finds_correct_relationship(empty_view: DynamicView):
    """Check logic for matching which relationship to use when adding."""
    model = empty_view.model
    system1 = model.add_software_system(name="System 1", id="sys1")
    system2 = model.add_software_system(name="System 2", id="sys2")
    system3 = model.add_software_system(name="System 3", id="sys3")
    rel1 = model.add_relationship(
        source=system1, destination=system2, description="Sends requests to"
    )
    rel2 = model.add_relationship(
        source=system2, destination=system3, description="Invokes", technology="REST"
    )
    rel3 = model.add_relationship(
        source=system2, destination=system3, description="Invokes", technology="SOAP"
    )
    rel4 = model.add_relationship(
        source=system1, destination=system3, description="Depends on"
    )

    assert empty_view.add(system1, system2, "Sends requests to").relationship is rel1
    assert not empty_view.add(system1, system2, "Sends requests to").response
    assert (
        empty_view.add(system2, system3, "Invokes", technology="REST").relationship
        is rel2
    )
    assert (
        empty_view.add(system2, system3, "Invokes", technology="SOAP").relationship
        is rel3
    )
    view = empty_view.add(system1, system3)
    assert view.relationship is rel4
    assert view.description == "Depends on"


def test_matching_where_descriptions_differ(empty_view: DynamicView):
    """Check case where description is different from than on the relationship."""
    model = empty_view.model
    system1 = model.add_software_system(name="System 1")
    system2 = model.add_software_system(name="System 2")
    rel = system1.uses(system2)

    view = empty_view.add(system1, system2, "New description")
    assert view.relationship is rel
    assert view.description == "New description"


def test_matching_on_response_relationship(empty_view: DynamicView):
    """Check it correctly finds relationships for responses."""
    model = empty_view.model
    system1 = model.add_software_system(name="System 1", id="sys1")
    system2 = model.add_software_system(name="System 2", id="sys2")
    system3 = model.add_software_system(name="System 3", id="sys3")
    rel1 = model.add_relationship(
        source=system1, destination=system2, description="Sends requests to"
    )
    model.add_relationship(
        source=system2, destination=system3, description="Invokes", technology="REST"
    )
    rel3 = model.add_relationship(
        source=system2, destination=system3, description="Invokes", technology="SOAP"
    )

    view = empty_view.add(system2, system1, "Sends response back to")
    assert view.relationship is rel1
    assert view.response
    assert view.description == "Sends response back to"

    view = empty_view.add(system3, system2, "Replies back to", technology="SOAP")
    assert view.relationship is rel3
    assert view.response
    assert view.description == "Replies back to"


def test_adding_relationships_failure_cases(empty_view: DynamicView):
    """Test common failure cases for adding relationships."""
    model = empty_view.model
    system1 = model.add_software_system(name="System 1", id="sys1")
    system2 = model.add_software_system(name="System 2", id="sys2")
    system3 = model.add_software_system(name="System 3", id="sys3")
    model.add_relationship(
        source=system1,
        destination=system2,
        description="Sends requests to",
        technology="REST",
    )

    with pytest.raises(ValueError, match="between System 1 and System 3 does not"):
        empty_view.add(system1, system3)
    with pytest.raises(ValueError, match="with technology 'Bogus'"):
        empty_view.add(system1, system2, "Sends requests to", technology="Bogus")
    with pytest.raises(ValueError, match="with technology 'Bogus'"):
        empty_view.add(system2, system1, "Sends response back to", technology="Bogus")


def test_can_add_people_to_view(empty_model: Model):
    """Make sure people can be added."""
    model = empty_model
    system1 = model.add_software_system(name="System 1", id="sys1")
    person1 = model.add_person(name="Person 1")
    rel = person1.uses(system1)

    view = DynamicView(description="test")
    view.set_model(model)

    relationship_view = view.add(person1, system1)
    assert relationship_view.relationship is rel


def test_adding_systems_to_system_scoped_view(empty_model: Model):
    """Check adding systems to unscoped view."""
    model = empty_model
    system1 = model.add_software_system(name="System 1")
    system2 = model.add_software_system(name="System 2")
    container1 = system1.add_container(name="Container 1")
    rel = system2.uses(container1)

    view = DynamicView(description="test", element=system1)
    view.set_model(model)

    relationship_view = view.add(system2, container1)
    assert relationship_view.relationship is rel


def test_trying_to_add_element_outside_scope(empty_model: Model):
    """Ensure adding relationships beyond this scope fails."""
    model = empty_model
    system1 = model.add_software_system(name="System 1", id="sys1")
    container1 = system1.add_container(name="Container 1")
    container2 = system1.add_container(name="Container 2")
    container1.add_component(name="Component 1")
    component2 = container1.add_component(name="Component 2")
    deploy1 = model.add_deployment_node(name="Deploy 1")

    # Unspecified scope can only take systems and people
    view = DynamicView(description="test")
    with pytest.raises(ValueError, match="Only people and software systems"):
        view.add(container1, container2)
    with pytest.raises(ValueError, match="Only people and software systems"):
        view.add(component2, component2)
    with pytest.raises(ValueError, match="Only people, software systems"):
        view.add(deploy1, system1)

    # Software system scope
    view = DynamicView(element=system1, description="test")
    with pytest.raises(ValueError, match="Components can't be added"):
        view.add(component2, component2)
    with pytest.raises(ValueError, match="is already the scope"):
        view.add(system1, container1)

    # Container scope
    view = DynamicView(element=container1, description="test")
    with pytest.raises(ValueError, match="is already the scope"):
        view.add(container1, container2)
    with pytest.raises(ValueError, match="is already the scope"):
        view.add(system1, container2)


def test_trying_to_add_element_with_existing_parent_or_child_fails(empty_model: Model):
    """Ensure adding relationships beyond this scope fails."""
    model = empty_model
    system1 = model.add_software_system(name="System 1", id="sys1")
    container1 = system1.add_container(name="Container 1")
    container2 = system1.add_container(name="Container 2")
    component1 = container1.add_component(name="Component 1")
    component2 = container2.add_component(name="Component 2")
    component1.uses(component2)
    component1.uses(container2)

    # Can't add if parent is already there
    view = DynamicView(element=container1, description="test")
    view.set_model(empty_model)
    view.add(component1, container2)
    with pytest.raises(ValueError, match="The parent of Component 2"):
        view.add(component1, component2)

    # Can't add if a child is already there
    view = DynamicView(element=container1, description="test")
    view.set_model(empty_model)
    view.add(component1, component2)
    with pytest.raises(ValueError, match="A child of Container 2"):
        view.add(component1, container2)


def test_basic_sequencing(empty_view: DynamicView):
    """Check the simplest form of incrementing order sequence."""
    model = empty_view.model
    system1 = model.add_software_system(name="System 1", id="sys1")
    system2 = model.add_software_system(name="System 2", id="sys2")
    system3 = model.add_software_system(name="System 3", id="sys3")
    system1.uses(system2)
    system2.uses(system3)

    rel1 = empty_view.add(system1, system2)
    rel2 = empty_view.add(system2, system3)
    rel3 = empty_view.add(system3, system2, "Replies to")
    rel4 = empty_view.add(system2, system1, "Replies to")

    assert rel1.order == "1"
    assert rel2.order == "2"
    assert rel3.order == "3"
    assert rel4.order == "4"


def test_subsequences(empty_view: DynamicView):
    """Test subsequences."""
    model = empty_view.model
    a = model.add_person(name="A")
    b = model.add_software_system(name="B")
    c = model.add_software_system(name="C")
    d = model.add_software_system(name="D")
    a.uses(b)
    b.uses(c, "Authenticates with")
    b.uses(d, "Retrieves data from")

    r1 = empty_view.add(a, b, "Loads web page from")
    with empty_view.subsequence():
        r2 = empty_view.add(b, c, "Authenticates with")
        r3 = empty_view.add(b, d, "Retrieves data from")
    r4 = empty_view.add(b, a, "Shows results to")
    assert r1.order == "1"
    assert r2.order == "1.1"
    assert r3.order == "1.2"
    assert r4.order == "2"


def test_parallel_sequencing(empty_view: DynamicView):
    """Test parallel sequencing.

    Note that this test is constructed to match the example in the documentation
    for `DynamicView.parallel_sequence()`.
    """
    model = empty_view.model
    a = model.add_software_system(name="A", id="a")
    b = model.add_software_system(name="B", id="b")
    c = model.add_software_system(name="C", id="c")
    d = model.add_software_system(name="D", id="d")
    e = model.add_software_system(name="E", id="e")
    f = model.add_software_system(name="F", id="f")
    a.uses(b)
    b.uses(c)
    b.uses(d)
    c.uses(e)
    d.uses(e)
    e.uses(f)

    r1 = empty_view.add(a, b)
    with empty_view.parallel_sequence():
        r2 = empty_view.add(b, c)
        r3 = empty_view.add(c, e)
    with empty_view.parallel_sequence(continue_numbering=True):
        r4 = empty_view.add(b, d)
        r5 = empty_view.add(d, e)
    r6 = empty_view.add(e, f)

    assert r1.order == "1"
    assert r2.order == "2"
    assert r3.order == "3"
    assert r4.order == "2"
    assert r5.order == "3"
    assert r6.order == "4"


def test_hydration(empty_model: Model):
    """Check dehydrating and hydrating."""
    system = empty_model.add_software_system(name="system", id="sys1")

    view = DynamicView(key="dyn1", description="Description", element=system)
    view.set_model(empty_model)

    io = DynamicViewIO.from_orm(view)
    d = io.dict()
    assert d["elementId"] == "sys1"

    view2 = DynamicView.hydrate(io, element=system)
    assert view2.key == "dyn1"
    assert view2.description == "Description"
    assert view2.element is system


def test_relationships_are_ordered(empty_model: Model):
    """Check that relationships are ordered for DynamicView."""
    system1 = empty_model.add_software_system(name="System 1")
    container1 = system1.add_container(name="Container 1")
    container2 = system1.add_container(name="Container 2")
    container1.uses(container2)

    view = DynamicView(key="dyn1", description="test", element=system1)
    view.set_model(empty_model)

    # Test using 10 items, so we can check 1 < 2 < 10 (i.e. not string ordering)
    for i in range(10):
        view.add(container1, container2, description=f"rel {i}")

    relationship_views = list(view.relationship_views)

    assert len(relationship_views) == 10
    for i in range(10):
        assert relationship_views[i].order == str(i + 1)


def test_relationships_with_subsequences_are_ordered(empty_model: Model):
    """Test ordering works with subsequences."""
    system1 = empty_model.add_software_system(name="System 1")
    container1 = system1.add_container(name="Container 1")
    container2 = system1.add_container(name="Container 2")
    container1.uses(container2)

    view = DynamicView(key="dyn1", description="test", element=system1)
    view.set_model(empty_model)

    view.add(container1, container2, description="test 1")
    with view.subsequence():
        view.add(container1, container2, description="test 1.1")
        view.add(container1, container2, description="test 1.2")
    for i in range(2, 11):
        view.add(container1, container2, description=f"test {i}")

    relationship_views = list(view.relationship_views)

    assert relationship_views[0].order == "1"
    assert relationship_views[1].order == "1.1"
    assert relationship_views[2].order == "1.2"
    assert relationship_views[3].order == "2"
    assert relationship_views[11].order == "10"
