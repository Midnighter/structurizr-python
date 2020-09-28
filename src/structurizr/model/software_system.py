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


from typing import TYPE_CHECKING, List, Set

from pydantic import Field

from .container import Container, ContainerIO
from .location import Location
from .static_structure_element import StaticStructureElement, StaticStructureElementIO
from .tags import Tags


if TYPE_CHECKING:
    from .model import Model


__all__ = ("SoftwareSystem", "SoftwareSystemIO")


class SoftwareSystemIO(StaticStructureElementIO):
    """
    Represent a software system in the C4 model.

    Attributes:
        location (Location): The location of this software system.
        containers (set of Container): The containers within this software system.

    """

    location: Location = Field(
        default=Location.Unspecified,
        description="The location of this software system.",
    )
    containers: List[ContainerIO] = Field(
        default=(), description="The containers within this software system."
    )


class SoftwareSystem(StaticStructureElement):
    """
    Represent a software system in the C4 model.

    Attributes:
        location (Location): The location of this software system.
        containers (set of Container): The containers within this software system.

    """

    def __init__(self, *, location: Location = Location.Unspecified, **kwargs) -> None:
        """"""
        super().__init__(**kwargs)
        self.location = location
        self.containers: Set[Container] = set()

        # TODO: canonical_name
        # TODO: parent

        self.tags.add(Tags.ELEMENT)
        self.tags.add(Tags.SOFTWARE_SYSTEM)

    def add(self, container: Container):
        self.containers.add(container)

    def add_container(
        self, name: str, description: str, technology: str = "", **kwargs
    ) -> Container:
        return self.get_model().add_container(
            parent=self,
            name=name,
            description=description,
            technology=technology,
            **kwargs,
        )

    @classmethod
    def hydrate(
        cls, software_system_io: SoftwareSystemIO, model: "Model"
    ) -> "SoftwareSystem":
        """"""
        software_system = cls(
            **cls.hydrate_arguments(software_system_io),
            location=software_system_io.location,
        )

        for container_io in software_system_io.containers:
            container = Container.hydrate(
                container_io,
                software_system=software_system,
                model=model,
            )
            model.add_container(container, parent=software_system)

        return software_system
