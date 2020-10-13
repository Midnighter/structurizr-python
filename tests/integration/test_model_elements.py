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


"""Ensure that elements are correctly handled by the model."""


import pytest

from structurizr.model import Person, SoftwareSystem
from structurizr.model.model import Model


@pytest.fixture(scope="function")
def model() -> Model:
    """Manufacture an empty model for test cases."""
    return Model()


@pytest.mark.parametrize(
    "attributes",
    [{"name": "User"}],
)
def test_add_person_from_args(attributes: dict, model: Model):
    """Expect that a person can be added to the model."""
    person = model.add_person(**attributes)
    assert person.id == "1"
    assert len(model.people) == 1
    for attr, expected in attributes.items():
        assert getattr(person, attr) == expected


@pytest.mark.parametrize(
    "attributes",
    [{"name": "User"}],
)
def test_add_person(attributes: dict, model: Model):
    """Expect that a person can be added to the model."""
    person = Person(**attributes)
    model.add_person(person)
    assert person.id == "1"
    assert len(model.people) == 1
    for attr, expected in attributes.items():
        assert getattr(person, attr) == expected


@pytest.mark.parametrize(
    "attributes",
    [{"name": "SkyNet"}],
)
def test_add_software_system_from_args(attributes: dict, model: Model):
    """Expect that a software system can be added to the model."""
    software_system = model.add_software_system(**attributes)
    assert software_system.id == "1"
    assert len(model.software_systems) == 1
    for attr, expected in attributes.items():
        assert getattr(software_system, attr) == expected


@pytest.mark.parametrize(
    "attributes",
    [{"name": "SkyNet"}],
)
def test_add_software_system(attributes: dict, model: Model):
    """Expect that a software system can be added to the model."""
    software_system = SoftwareSystem(**attributes)
    model.add_software_system(software_system)
    assert software_system.id == "1"
    assert len(model.software_systems) == 1
    for attr, expected in attributes.items():
        assert getattr(software_system, attr) == expected
