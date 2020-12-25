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
from structurizr.view.view import View


class DerivedView(View):
    """Mock class for testing."""

    pass


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
