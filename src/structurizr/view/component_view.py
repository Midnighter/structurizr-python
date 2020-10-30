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


"""Provide a component view."""


from typing import Union

from pydantic import Field

from ..model import Component, Container, Element, Person, SoftwareSystem
from .static_view import StaticView, StaticViewIO


__all__ = ("ComponentView", "ComponentViewIO")


class ComponentViewIO(StaticViewIO):
    """
    Represent the component view from the C4 model.

    Attributes:
        external_software_system_boundary_visible (bool): Determines whether software
        system boundaries should be visible for "external" components (those outside
        the software system in scope).

    """

    external_software_system_boundary_visible: bool = Field(
        default=True,
        alias="externalSoftwareSystemBoundariesVisible",
    )
    container_id: str = Field(..., alias="containerId")


class ComponentView(StaticView):
    """
    Represent the component view from the C4 model.

    Attributes:
        external_software_system_boundary_visible (bool):

    """

    def __init__(
        self,
        *,
        container: Container,
        external_software_system_boundary_visible: bool = True,
        **kwargs,
    ) -> None:
        """Initialize a component view."""
        super().__init__(software_system=container.parent, **kwargs)
        self.container = container
        self.container_id = container.id
        self.external_software_system_boundary_visible = (
            external_software_system_boundary_visible
        )

    @classmethod
    def hydrate(
        cls,
        component_view_io: ComponentViewIO,
        container: Container,
    ) -> "ComponentView":
        """Hydrate a new ComponentView instance from its IO."""
        return cls(
            **cls.hydrate_arguments(component_view_io),
            container=container,
            external_software_system_boundary_visible=(
                component_view_io.external_software_system_boundary_visible
            ),
        )

    @property
    def name(self):
        """Return the (computed) name of this view."""
        return f"{self.software_system.name} - {self.container.name} - Components"

    def add(
        self,
        element: Union[SoftwareSystem, Container, Component],
    ) -> None:
        """
        Add the given software system, container or component to this view.

        Args:
            element (SoftwareSystem, Container or Component): The static element
                to add to this view.

        """
        return self._add_element(element, add_relationships=True)

    def remove(self, element):
        """Remove an individual element from this view."""
        self._remove_element(element)

    def add_all_elements(self) -> None:
        """Add all people, software systems, containers and components to this view."""
        self.add_all_people()
        self.add_all_software_systems()
        self.add_all_containers()
        self.add_all_components()

    def add_all_containers(self) -> None:
        """Add all other containers in the software system to this view."""
        for container in self.software_system.containers:
            self.add(container)

    def add_all_components(self) -> None:
        """Add all components in the container to this view."""
        for component in self.container.components:
            self.add(component)

    def add_nearest_neighbours(self, element: Element, _=None) -> None:
        """Add neighbouring people, software systems, containers and components."""
        super().add_nearest_neighbours(element, SoftwareSystem)
        super().add_nearest_neighbours(element, Person)
        super().add_nearest_neighbours(element, Container)
        super().add_nearest_neighbours(element, Component)
