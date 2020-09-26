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
def model() -> Model:
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


def test_get_tags_when_there_are_no_tags(model: Model):
    element = model.add_software_system(name="Name", description="Description")
    assert list(element.tags) == ["Element", "Software System"]


def test_get_tags_returns_the_list_of_tags_when_there_are_some_tags(model: Model):
    # Based on the equivalent Java test, but also checks tag ordering is preserved
    # See https://github.com/Midnighter/structurizr-python/issues/22
    element = model.add_software_system(name="Name", description="Description")
    element.tags.update(["tag3", "tag2", "tag1"])  # Deliberately unsorted
    assert list(element.tags) == ["Element", "Software System", "tag3", "tag2", "tag1"]


def test_tag_order_is_preserved_to_and_from_io(model: Model):
    element = model.add_software_system(name="Name", description="Description")
    element.tags.update(["tag3", "tag2", "tag1"])  # Deliberately unsorted

    elementIO = SoftwareSystemIO.from_orm(element)
    assert elementIO.tags == ["Element", "Software System", "tag3", "tag2", "tag1"]
    element2 = SoftwareSystem.hydrate(elementIO, model)
    assert list(element2.tags) == ["Element", "Software System", "tag3", "tag2", "tag1"]
