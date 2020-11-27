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


from typing import Iterable, List, Set

from pydantic import Field

from .container import Container, ContainerIO
from .location import Location
from .static_structure_element import StaticStructureElement, StaticStructureElementIO
from .tags import Tags


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
        """Initialise a new SoftwareSystem."""
        super().__init__(**kwargs)
        self.location = location
        self._containers: Set[Container] = set()

        # TODO: canonical_name
        # TODO: parent

        self.tags.add(Tags.ELEMENT)
        self.tags.add(Tags.SOFTWARE_SYSTEM)

    @property
    def containers(self) -> Iterable[Container]:
        """Return read-only list of child containers."""
        return list(self._containers)

    @property
    def child_elements(self) -> Iterable[Container]:
        """Return child elements (from `Element.children`)."""
        return self.containers

    def add_container(
        self, name: str, description: str = "", technology: str = "", **kwargs
    ) -> Container:
        """Construct a new `Container` and add to this system and its model."""
        container = Container(
            name=name, description=description, technology=technology, **kwargs
        )
        self += container
        return container

    def __iadd__(self, container: Container) -> "SoftwareSystem":
        """Add a new container to this system and register with its model."""
        # TODO: once we move past python 3.6 change to proper return type via
        # __future__.annotations
        if container in self._containers:
            return self

        if self.get_container_with_name(container.name):
            raise ValueError(
                f"Container with name {container.name} already exists for {self}."
            )

        if container.parent is None:
            container.parent = self
        elif container.parent is not self:
            raise ValueError(
                f"Container with name {container.name} already has parent "
                f"{container.parent}. Cannot add to {self}."
            )
        self._containers.add(container)
        if self.has_model:
            model = self.model
            model += container
        return self

    def get_container_with_name(self, name: str) -> Container:
        """Return the container with the given name, or None."""
        return next((c for c in self._containers if c.name == name), None)

    @classmethod
    def hydrate(cls, software_system_io: SoftwareSystemIO) -> "SoftwareSystem":
        """Create a new SoftwareSystem instance and hydrate it from its IO."""
        software_system = cls(
            **cls.hydrate_arguments(software_system_io),
            location=software_system_io.location,
        )

        for container_io in software_system_io.containers:
            software_system += Container.hydrate(
                container_io,
                software_system=software_system,
            )

        return software_system
