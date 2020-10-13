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


"""Ensure the expected behaviour of the model item base class."""


import pytest

from structurizr.model import Model, SoftwareSystem, SoftwareSystemIO
from structurizr.model.model_item import ModelItem


@pytest.fixture(scope="function")
def empty_model() -> Model:
    """Provide an empty Model on demand for test cases to use."""
    return Model()


class ConcreteModelItem(ModelItem):
    """Implement a concrete `ModelItem` class for testing purposes."""

    pass


@pytest.mark.parametrize(
    "attributes",
    [{}],
)
def test_model_item_init(attributes):
    """Expect proper initialization from arguments."""
    model_item = ConcreteModelItem(**attributes)
    for attr, expected in attributes.items():
        assert getattr(model_item, attr) == expected


def test_default_element_tags_order(empty_model: Model):
    """
    Test that the default tags get added in the right order.

    Based on test_getTags_WhenThereAreNoTags() from the Java API.
    """
    element = empty_model.add_software_system(name="Name", description="Description")
    assert list(element.tags) == ["Element", "Software System"]


def test_default_and_custom_tags(empty_model: Model):
    """
    Test that tags are in the order that they were added.

    Based on test_getTags_ReturnsTheListOfTags_WhenThereAreSomeTags from the Java API.

    See https://github.com/Midnighter/structurizr-python/issues/22
    """
    element = empty_model.add_software_system(name="Name", description="Description")
    element.tags.update(["tag3", "tag2", "tag1"])  # Deliberately not ascending
    assert list(element.tags) == ["Element", "Software System", "tag3", "tag2", "tag1"]


def test_tag_order_is_preserved_to_and_from_io(empty_model: Model):
    """Test that when serializing via IO classes or back, tag ordering is preserved."""
    element = empty_model.add_software_system(name="Name", description="Description")
    element.tags.update(["tag3", "tag2", "tag1"])  # Deliberately not ascending

    element_io = SoftwareSystemIO.from_orm(element)
    assert element_io.tags == ["Element", "Software System", "tag3", "tag2", "tag1"]
    assert element_io.dict()["tags"] == "Element,Software System,tag3,tag2,tag1"
    element2 = SoftwareSystem.hydrate(element_io, empty_model)
    assert list(element2.tags) == ["Element", "Software System", "tag3", "tag2", "tag1"]
