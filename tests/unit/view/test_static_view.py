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


"""Ensure the expected behaviour of StaticView."""


from structurizr.model import Model, Person, SoftwareSystem
from structurizr.view.static_view import StaticView


class DerivedView(StaticView):
    """Mock class for testing."""

    def add_all_elements(self) -> None:
        """Stub method because base is abstract."""
        pass


def test_add_nearest_neighbours():
    """Test basic behaviour of add_nearest_neighbours."""
    model = Model()
    sys1 = model.add_software_system(name="System 1")
    sys2 = model.add_software_system(name="System 2")
    person = model.add_person(name="Person 1")
    sys1.uses(sys2)
    person.uses(sys1)

    # Check neighbours from outbound relationships
    view = DerivedView(software_system=sys1, description="")
    view.add_nearest_neighbours(sys1, SoftwareSystem)
    assert any((elt_view.element is sys1 for elt_view in view.element_views))
    assert any((elt_view.element is sys2 for elt_view in view.element_views))
    assert not any((elt_view.element is person for elt_view in view.element_views))
    assert len(view.relationship_views) == 1

    # Check neighbours from inbound relationships
    view = DerivedView(software_system=sys1, description="")
    view.add_nearest_neighbours(sys2, SoftwareSystem)
    assert any((elt_view.element is sys1 for elt_view in view.element_views))
    assert any((elt_view.element is sys2 for elt_view in view.element_views))
    assert not any((elt_view.element is person for elt_view in view.element_views))
    assert len(view.relationship_views) == 1


def test_add_nearest_neighbours_doesnt_dupe_relationships():
    """Test relationships aren't duplicated if neighbours added more than once.

    See https://github.com/Midnighter/structurizr-python/issues/63.
    """
    model = Model()
    sys1 = model.add_software_system(name="System 1")
    sys2 = model.add_software_system(name="System 2")
    sys1.uses(sys2)
    view = DerivedView(software_system=sys1, description="")
    view.add_nearest_neighbours(sys1, SoftwareSystem)
    assert len(view.relationship_views) == 1

    # The next line should not add any new relationships
    view.add_nearest_neighbours(sys1, Person)
    assert len(view.relationship_views) == 1
