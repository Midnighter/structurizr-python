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

from structurizr.model import Model


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
