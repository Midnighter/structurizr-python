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


"""Ensure the expected behaviour of GroupableElement."""

from structurizr.mixin.childless_mixin import ChildlessMixin
from structurizr.model.groupable_element import GroupableElement, GroupableElementIO


class ConcreteElement(ChildlessMixin, GroupableElement):
    """Implement a concrete `GroupableElement` class for testing purposes."""

    pass


def test_group_in_json():
    """Test the group field is output to JSON."""
    element = ConcreteElement(name="Name", group="Group 1")
    io = GroupableElementIO.from_orm(element)
    assert '"group": "Group 1"' in io.json()


def test_group_omitted_from_json_if_empty():
    """Test the group field is not output if empty."""
    element = ConcreteElement(name="Name")
    io = GroupableElementIO.from_orm(element)
    assert '"group"' not in io.json()


def test_hydration():
    """Test hydration picks up the group field."""
    element = ConcreteElement(name="Name", group="Group 1")
    io = GroupableElementIO.from_orm(element)
    d = GroupableElement.hydrate_arguments(io)
    assert d["group"] == "Group 1"
