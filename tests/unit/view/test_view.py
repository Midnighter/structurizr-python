# Copyright (c) 2020
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


"""Ensure the expected behaviour of View."""

from structurizr.model import Model
from structurizr.view.paper_size import PaperSize
from structurizr.view.view import View, ViewIO


class DerivedView(View):
    """Mock class for testing."""

    pass


def test_find_element_view():
    """Test behaviour of find_element_view."""
    model = Model()
    sys1 = model.add_software_system(name="System 1")
    sys2 = model.add_software_system(name="System 2")

    view = DerivedView(software_system=sys1, description="")
    view._add_element(sys1, False)

    assert view.find_element_view(element=sys1).element is sys1
    assert view.find_element_view(element=sys2) is None


def test_find_relationship_view():
    """Test behaviour of find_element_view."""
    model = Model()
    sys1 = model.add_software_system(name="System 1")
    sys2 = model.add_software_system(name="System 2")
    rel1 = sys1.uses(sys2, "Uses")
    rel2 = sys2.uses(sys1, "Also uses")
    rel3 = sys2.uses(sys1, "Returns")

    view = DerivedView(software_system=sys1, description="")
    view._add_element(sys1, False)
    view._add_element(sys2, False)
    view._add_relationship(rel1).description = "Override"
    view._add_relationship(rel3).response = True

    assert view.find_relationship_view(relationship=rel1).relationship is rel1
    assert view.find_relationship_view(relationship=rel2) is None
    assert view.find_relationship_view(description="Override").relationship is rel1
    assert view.find_relationship_view(description="Uses") is None
    assert view.find_relationship_view(description="Returns").relationship is rel3
    assert view.find_relationship_view(response=True).relationship is rel3
    assert view.find_relationship_view(response=False).relationship is rel1


def test_is_element_in_view():
    """Test check for an element being in the view."""
    model = Model()
    sys1 = model.add_software_system(name="System 1")
    sys2 = model.add_software_system(name="System 2")

    view = DerivedView(software_system=sys1, description="")
    view._add_element(sys1, False)

    assert view.is_element_in_view(sys1)
    assert not view.is_element_in_view(sys2)


def test_add_relationship_doesnt_duplicate():
    """Test that adding a relationships twice doesn't duplicate it."""
    model = Model()
    sys1 = model.add_software_system(name="System 1")
    sys2 = model.add_software_system(name="System 2")
    rel = sys1.uses(sys2)

    view = DerivedView(software_system=sys1, description="")
    view._add_element(sys1, False)
    view._add_element(sys2, False)

    rel_view1 = view._add_relationship(rel)
    assert len(view.relationship_views) == 1
    rel_view2 = view._add_relationship(rel)
    assert len(view.relationship_views) == 1
    assert rel_view2 is rel_view1


def test_add_relationship_for_element_not_in_view():
    """Ensures relationships for elements outside the view are ignored."""
    model = Model()
    sys1 = model.add_software_system(name="System 1")
    sys2 = model.add_software_system(name="System 2")
    rel = sys1.uses(sys2)

    view = DerivedView(software_system=sys1, description="")
    view._add_element(sys1, False)

    # This relationship should be ignored as sys2 isn't in the view
    rel_view1 = view._add_relationship(rel)
    assert rel_view1 is None
    assert view.relationship_views == set()


def test_adding_all_relationships():
    """Test adding all relationships for elements in the view."""
    model = Model()
    sys1 = model.add_software_system(name="System 1")
    sys2 = model.add_software_system(name="System 2")
    sys3 = model.add_software_system(name="System 3")
    rel1 = sys1.uses(sys2)
    rel2 = sys3.uses(sys1)

    view = DerivedView(software_system=sys1, description="")
    view._add_element(sys1, False)
    view._add_element(sys2, False)
    view._add_element(sys3, False)
    assert view.relationship_views == set()

    view._add_relationships(sys1)
    assert len(view.relationship_views) == 2
    assert rel1 in [vr.relationship for vr in view.relationship_views]
    assert rel2 in [vr.relationship for vr in view.relationship_views]


def test_missing_json_description_allowed():
    """
    Ensure that missing descriptions in the JSON form are supported.

    Raised as https://github.com/Midnighter/structurizr-python/issues/40, it is
    permitted through the Structurizr UI to create views with a blank description,
    which then gets ommitted from the workspace JSON, so this needs to be allowed by
    the Pydantic validation also.
    """

    json = """
    {
        "key": "System1-SystemContext"
    }
    """
    io = ViewIO.parse_raw(json)
    assert io is not None


def test_copy_layout():
    """Ensure that layout is copied over, including sub-views."""
    model = Model()
    sys1 = model.add_software_system(name="System 1")
    sys2 = model.add_software_system(name="System 2")
    rel1 = sys1.uses(sys2)

    view1 = DerivedView(software_system=sys1, description="")
    view1._add_element(sys1, False).paper_size = PaperSize.A1_Portrait
    view1._add_element(sys2, False).paper_size = PaperSize.A2_Portrait
    view1._add_relationship(rel1).paper_size = PaperSize.A3_Portrait
    view1.paper_size = PaperSize.A4_Portrait

    view2 = DerivedView(software_system=sys1, description="")
    view2._add_element(sys1, False).paper_size = PaperSize.A1_Portrait
    view2._add_element(sys2, False).paper_size = PaperSize.A2_Portrait
    view2._add_relationship(rel1).paper_size = PaperSize.A3_Portrait
    view2.copy_layout_information_from(view1)

    assert view2.paper_size == PaperSize.A4_Portrait
    assert view2.find_element_view(element=sys1).paper_size == PaperSize.A1_Portrait
    rv = view2.find_relationship_view(description="Uses")
    assert rv.paper_size == PaperSize.A3_Portrait
