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


from typing import Any, Set

from pydantic import Field

from .location import Location
from .static_structure_element import StaticStructureElement


__all__ = ("SoftwareSystem",)


class SoftwareSystem(StaticStructureElement):
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
    containers: Set[Any] = Field(
        set(), description="The containers within this software system."
    )
