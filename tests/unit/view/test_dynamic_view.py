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
    view2 = DynamicView(description="Description", software_system=system)
    assert view2.element is system
    view3 = DynamicView(description="Description", container=container)
    assert view3.element is container
    with pytest.raises(ValueError, match="You cannot specify"):
        DynamicView(
            description="Description", software_system=system, container=container
        )


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

    assert empty_view.add(system1, "Sends requests to", system2).relationship is rel1
    assert not empty_view.add(system1, "Sends requests to", system2).response
    assert (
        empty_view.add(system2, "Invokes", system3, technology="REST").relationship
        is rel2
    )
    assert (
        empty_view.add(system2, "Invokes", system3, technology="SOAP").relationship
        is rel3
    )


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

    view = empty_view.add(system2, "Sends response back to", system1)
    assert view.relationship is rel1
    assert view.response
    assert view.description == "Sends response back to"

    view = empty_view.add(system3, "Replies back to", system2, technology="SOAP")
    assert view.relationship is rel3
    assert view.response
    assert view.description == "Replies back to"


def test_adding_relationships_failure_cases(empty_view: DynamicView):
    """Test common failure cases for adding relationships."""
    model = empty_view.model
    system1 = model.add_software_system(name="System 1", id="sys1")
    system2 = model.add_software_system(name="System 2", id="sys2")
    model.add_relationship(
        source=system1,
        destination=system2,
        description="Sends requests to",
        technology="REST",
    )

    with pytest.raises(
        ValueError, match="A relationship between System 1 and System 2"
    ):
        empty_view.add(system1, "Bogus description", system2)
    with pytest.raises(ValueError, match="with technology 'Bogus'"):
        empty_view.add(system1, "Sends requests to", system2, technology="Bogus")
    with pytest.raises(ValueError, match="with technology 'Bogus'"):
        empty_view.add(system2, "Sends response back to", system1, technology="Bogus")


@pytest.mark.xfail(sctrict=True)
def test_trying_to_add_element_outside_scope(empty_view: DynamicView):
    """Ensure adding relationships beyond this scope fails."""
    assert 1 == 0  # TODO


def test_basic_sequencing(empty_view: DynamicView):
    """Check the simplest form of incrementing order sequence."""
    model = empty_view.model
    system1 = model.add_software_system(name="System 1", id="sys1")
    system2 = model.add_software_system(name="System 2", id="sys2")
    system3 = model.add_software_system(name="System 3", id="sys3")
    system1.uses(system2)
    system2.uses(system3)

    rel1 = empty_view.add(system1, "Uses", system2)
    rel2 = empty_view.add(system2, "Uses", system3)
    rel3 = empty_view.add(system3, "Replies to", system2)
    rel4 = empty_view.add(system2, "Replies to", system1)

    assert rel1.order == "1"
    assert rel2.order == "2"
    assert rel3.order == "3"
    assert rel4.order == "4"

def test_hydration(empty_model: Model):
    """Check dehydrating and hydrating."""
    system = empty_model.add_software_system(name="system", id="sys1")

    view = DynamicView(key="dyn1", description="Description", software_system=system)
    view.set_model(empty_model)

    io = DynamicViewIO.from_orm(view)
    d = io.dict()
    assert d["elementId"] == "sys1"

    view2 = DynamicView.hydrate(io, element=system)
    assert view2.key == "dyn1"
    assert view2.description == "Description"
    assert view2.element is system
