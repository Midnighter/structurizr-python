# Copyright (c) 2020, Moritz E. Beber.
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


"""Ensure the expected behaviour of the model element."""


import pytest

from structurizr.mixin.childless_mixin import ChildlessMixin
from structurizr.model.element import Element


class ConcreteElement(ChildlessMixin, Element):
    """Implement a concrete `Element` class for testing purposes."""

    pass


class MockModel:
    """Implement a mock model for reference testing."""

    def add_relationship(self, relationship, create_implied_relationships):
        """Provide mock implementation."""
        return relationship


@pytest.mark.parametrize(
    "attributes",
    [
        pytest.param({}, marks=pytest.mark.raises(exception=TypeError)),
        {"name": "Important Element"},
    ],
)
def test_element_init(attributes):
    """Expect proper initialization from arguments."""
    element = ConcreteElement(**attributes)
    for attr, expected in attributes.items():
        assert getattr(element, attr) == expected


def test_model_reference():
    """Expect that setting the model creates a reference."""
    model = MockModel()
    element = ConcreteElement(name="Element")
    element.set_model(model)
    assert element.get_model() is model


def test_element_child_elements_default():
    """Ensure that by default, element has no children."""
    element = ConcreteElement(name="Element")
    assert element.child_elements == []


def test_element_can_only_add_relationship_to_source():
    """Make sure that nothing adds a relationship to the wrong element."""
    element1 = ConcreteElement(name="elt1")
    element2 = ConcreteElement(name="elt1")
    with pytest.raises(
        ValueError,
        match="Cannot add relationship .* to element .* that is not its source",
    ):
        element1.add_relationship(source=element2)


def test_element_add_relationship_can_omit_source():
    """Expect that creating a relationship uses the default source."""
    element1 = ConcreteElement(name="elt1")
    element2 = ConcreteElement(name="elt1")
    model = MockModel()
    element1.set_model(model)
    relationship = element1.add_relationship(destination=element2)
    assert relationship.source is element1


def test_element_add_relationship_twice_is_ok():
    """Ensure that adding the same relationship twice is fine."""
    element1 = ConcreteElement(name="elt1")
    element2 = ConcreteElement(name="elt1")
    model = MockModel()
    element1.set_model(model)
    relationship = element1.add_relationship(destination=element2)
    element1.add_relationship(relationship)
    assert element1.relationships == {relationship}
