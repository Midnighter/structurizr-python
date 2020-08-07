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


"""Provide a container view."""


from typing import Union

from pydantic import Field

from ..model import Container, Element, Person, SoftwareSystem
from .static_view import StaticView, StaticViewIO


__all__ = ("ContainerView", "ContainerViewIO")


class ContainerViewIO(StaticViewIO):
    """
    Represent the container view from the C4 model.

    Attributes:
        external_software_system_boundary_visible (bool): Determines whether software
        system boundaries should be visible for "external" containers (those outside
        the software system in scope).

    """

    external_software_system_boundary_visible: bool = Field(
        default=True, alias="externalSoftwareSystemBoundariesVisible"
    )


class ContainerView(StaticView):
    """
    Represent the container view from the C4 model.
``
    Attributes:
        external_software_system_boundary_visible (bool):

    """

    def __init__(
        self, *, external_software_system_boundary_visible: bool = True, **kwargs
    ) -> None:
        """Initialize a container view."""
        super().__init__(**kwargs)
        self.external_software_system_boundary_visible = (
            external_software_system_boundary_visible
        )

    def add(
        self,
        static_element: Union[Person, SoftwareSystem, Container],
        add_relationships: bool = True,
    ) -> None:
        """
        Add the given person, software system, or container to this view.

        Args:
            static_element (Person, SoftwareSystem or Container): The static element
                to add to this view.
            add_relationships (bool, optional): Whether to include all of the static
                element's relationships with other elements (default `True`).

        """
        return self._add_element(static_element, add_relationships=True)

    def add_all_elements(self) -> None:
        """Add all people, software systems, and containers to this view."""
        self.add_all_people()
        self.add_all_software_systems()
        self.add_all_containers()

    def add_all_containers(self) -> None:
        for container in self.software_system.containers:
            self.add(container)

    def add_nearest_neighbours(self, element: Element, _=None) -> None:
        super().add_nearest_neighbours(element, SoftwareSystem)
        super().add_nearest_neighbours(element, Person)
        super().add_nearest_neighbours(element, Container)

    @classmethod
    def hydrate(cls, container_view_io: ContainerViewIO) -> "ContainerView":
        """"""
        return cls(
            external_software_system_boundary_visible=(
                container_view_io.external_software_system_boundary_visible
            ),
            description=container_view_io.description,
            key=container_view_io.key,
            # TODO: Need an instance here or get an instance from the model by
            #  reference.
            # software_system=container_view_io.software_system,
        )
