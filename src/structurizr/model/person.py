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


from pydantic import Field

from .location import Location
from .static_structure_element import StaticStructureElement, StaticStructureElementIO


__all__ = ("PersonIO", "Person")


class PersonIO(StaticStructureElementIO):
    """
    Represent a person in the C4 model.

    Attributes:
        location (Location): The location of this person.

    """

    location: Location = Field(
        Location.Unspecified, description="The location of this person."
    )


class Person(StaticStructureElement):
    """
    Represent a person in the C4 model.

    Attributes:
        location (Location): The location of this person.

    """

    location: Location = Field(
        Location.Unspecified, description="The location of this person."
    )

    def __init__(self, *, location: Location = Location.Unspecified, **kwargs) -> None:
        """"""
        super().__init__(**kwargs)
        self.location = location

    @classmethod
    def hydrate(cls, person_io: PersonIO) -> "Person":
        """"""
        return cls(name=person_io.name, description=person_io.description)

    def interacts_with(self):
        # TODO
        pass
