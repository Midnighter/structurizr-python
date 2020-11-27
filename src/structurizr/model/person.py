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


"""Provide a person model."""


from typing import Optional

from pydantic import Field

from ..mixin.childless_mixin import ChildlessMixin
from .location import Location
from .relationship import Relationship
from .static_structure_element import StaticStructureElement, StaticStructureElementIO
from .tags import Tags


__all__ = ("PersonIO", "Person")


class PersonIO(StaticStructureElementIO):
    """
    Represent a person in the C4 model.

    Attributes:
        location (Location): The location of this person.

    """

    location: Location = Field(
        default=Location.Unspecified, description="The location of this person."
    )


class Person(ChildlessMixin, StaticStructureElement):
    """
    Represent a person in the C4 model.

    Attributes:
        location (Location): The location of this person.

    """

    def __init__(self, *, location: Location = Location.Unspecified, **kwargs) -> None:
        """Initialise a Person."""
        super().__init__(**kwargs)
        self.location = location

        self.tags.add(Tags.PERSON)

    @classmethod
    def hydrate(cls, person_io: PersonIO) -> "Person":
        """Create a new person and hydrate from its IO."""
        person = cls(
            **cls.hydrate_arguments(person_io),
            location=person_io.location,
        )
        return person

    def interacts_with(
        self, destination: "Person", description: str, **kwargs
    ) -> Optional[Relationship]:
        """Create a relationship with the given other Person."""
        return self.uses(destination=destination, description=description, **kwargs)
