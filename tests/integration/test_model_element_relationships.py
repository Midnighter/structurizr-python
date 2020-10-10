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

"""
Ensure that relationships in Elements and in the Model are consistent.

See https://github.com/Midnighter/structurizr-python/issues/31.
"""

from pathlib import Path

import pytest

from structurizr import Workspace
from structurizr.model import Model


DEFINITIONS = Path(__file__).parent / "data" / "workspace_definition"


@pytest.mark.xfail(strict=True)
def test_adding_relationship_to_element_adds_to_model():
    """
    Make sure that when a relationship is added via Element.add_relationship it also
    gets added to the model and to the other element.
    """
    model = Model()
    sys1 = model.add_software_system(name="sys1")
    sys2 = model.add_software_system(name="sys2")

    r = sys1.add_relationship(source=sys1, destination=sys2, description="uses")
    assert list(sys1.relationships) == [r]
    assert list(sys1.get_relationships()) == [r]  # Currently will fail
    assert list(model.get_relationships()) == [r]  # Currently will fail
    assert list(sys2.relationships) == []  # relationships only contains outbound
    assert list(sys2.get_relationships()) == [r]  # Currently will fail


def test_adding_relationship_to_model_adds_to_element():
    """
    Make sure that when a relationship is added via Element.add_relationship it also
    gets added to the model and to the other element.
    """
    model = Model()
    sys1 = model.add_software_system(name="sys1")
    sys2 = model.add_software_system(name="sys2")

    r = model.add_relationship(source=sys1, destination=sys2, description="uses")
    assert list(sys1.relationships) == [r]
    assert list(sys1.get_relationships()) == [r]
    assert list(model.get_relationships()) == [r]
    assert list(sys2.relationships) == []  # relationships only contains outbound
    assert list(sys2.get_relationships()) == [r]


def test_adding_relationship_via_uses_adds_to_elements():
    """
    Make sure that when a relationship is added via StaticStructureElement.uses
    then it is reflected in the Elements.
    """
    model = Model()
    sys1 = model.add_software_system(name="sys1")
    sys2 = model.add_software_system(name="sys2")

    r = sys1.uses(sys2, "uses")
    assert list(sys1.relationships) == [r]
    assert list(sys1.get_relationships()) == [r]
    assert list(model.get_relationships()) == [r]
    assert list(sys2.relationships) == []  # relationships only contains outbound
    assert list(sys2.get_relationships()) == [r]


@pytest.mark.parametrize(
    "filename",
    ["BigBank.json"],
)
def test_relationships_after_deserialisation_are_consistent(filename):
    """Make sure that relationships are consistent between the Model and the Element after deserialisation."""
    path = DEFINITIONS / filename
    workspace = Workspace.load(path)
    model = workspace.model
    atm = model.get_software_system_with_id("9")
    mainframe = model.get_software_system_with_id("4")
    customer = model.get_element("1")

    assert len(atm.relationships) == 1
    assert (
        len(list(atm.get_relationships())) == 2
    )  # One to mainframe, one from personal banking customer
    assert len(list(atm.get_afferent_relationships())) == 1
    assert list(atm.get_afferent_relationships())[0].source is customer
    assert len(list(atm.get_efferent_relationships())) == 1
    assert list(atm.get_efferent_relationships())[0].destination is mainframe
