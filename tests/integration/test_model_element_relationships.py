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

import pytest

from structurizr.model import Model


@pytest.mark.skip(reason="To be fixed - issue #31")
def test_adding_relationship_to_element_adds_to_model():
    """
    Make sure that when a relationship is added via Element.add_relationship it also
    gets added to the model and to the other element.
    """
    model = Model()
    sys1 = model.add_software_system(name="sys1")
    sys2 = model.add_software_system(name="sys2")

    sys1.add_relationship(source=sys1, destination=sys2, description="uses")
    assert len(sys1.relationships) == 1
    assert len(list(sys1.get_relationships())) == 1  # Currently will fail
    assert len(model.get_relationships()) == 1  # Currently will fail
    assert len(sys2.relationships) == 1  # Currently will fail
    assert len(list(sys2.get_relationships())) == 1  # Currently will fail


@pytest.mark.skip(reason="To be fixed - issue #31")
def test_adding_relationship_via_uses_adds_to_elements():
    """
    Make sure that when a relationship is added via StaticStructureElement.uses
    then it is reflected in the Elements.
    """
    model = Model()
    sys1 = model.add_software_system(name="sys1")
    sys2 = model.add_software_system(name="sys2")

    sys1.uses(sys2, "uses")
    assert len(sys1.relationships) == 1
    assert len(list(sys1.get_relationships())) == 1
    assert len(model.get_relationships()) == 1
    assert len(sys2.relationships) == 1  # Currently will fail
    assert len(list(sys2.get_relationships())) == 1
