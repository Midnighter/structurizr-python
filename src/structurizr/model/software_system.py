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


"""Provide a software system element model."""


from typing import Any, List, Optional, Set

from pydantic import Field

from .location import Location
from .static_structure_element import StaticStructureElement, StaticStructureElementIO


__all__ = ("SoftwareSystem", "SoftwareSystemIO")


class SoftwareSystemIO(StaticStructureElementIO):
    """
    Represent a software system in the C4 model.

    Attributes:
        location (Location): The location of this software system.
        containers (set of Container): The containers within this software system.

    """

    location: Location = Field(
        Location.Unspecified, description="The location of this software system."
    )
    # TODO
    containers: List[Any] = Field(
        [], description="The containers within this software system."
    )


class SoftwareSystem(StaticStructureElement):
    """
    Represent a software system in the C4 model.

    Attributes:
        location (Location): The location of this software system.
        containers (set of Container): The containers within this software system.

    """

    def __init__(
        self,
        *,
        location: Location = Location.Unspecified,
        containers: Optional[Set[Any]] = None,
        **kwargs
    ) -> None:
        """"""
        super().__init__(**kwargs)
        self.location = location
        self.containers = set() if containers is None else containers

    @classmethod
    def hydrate(cls, software_system_io: SoftwareSystemIO) -> "SoftwareSystem":
        """"""
        return cls(
            name=software_system_io.name, description=software_system_io.description
        )
