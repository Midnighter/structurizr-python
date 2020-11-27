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


"""Provide a container model."""

from typing import TYPE_CHECKING, Iterable, List, Optional

from pydantic import Field

from .component import Component, ComponentIO
from .static_structure_element import StaticStructureElement, StaticStructureElementIO
from .tags import Tags


if TYPE_CHECKING:  # pragma: no cover
    from .software_system import SoftwareSystem


__all__ = ("Container", "ContainerIO")


class ContainerIO(StaticStructureElementIO):
    """
    Represent a container.

    A container is something that can execute code or host data.

    Attributes:
        id: The ID of this container in the model.
        name: The name of this container.
        description: A short description of this container.
        technology: The technology associated with this container
                    (e.g. Apache Tomcat).
        tags: A comma separated list of tags associated with this container.
        components: The set of components within this container.
        properties: A set of arbitrary name-value properties.
        relationships: The set of relationships from this container to
                       other elements.

    """

    technology: Optional[str] = ""
    components: List[ComponentIO] = Field(default=())


class Container(StaticStructureElement):
    """
    Represent a container.

    A container is something that can execute code or host data.

    Attributes:
        id: The ID of this container in the model.
        name: The name of this container.
        description: A short description of this container.
        technology: The technology associated with this container
                    (e.g. Apache Tomcat).
        tags: A comma separated list of tags associated with this container.
        components: The set of components within this container.
        properties: A set of arbitrary name-value properties.
        relationships: The set of relationships from this container to
                       other elements.

    """

    def __init__(
        self,
        *,
        parent: Optional["SoftwareSystem"] = None,
        technology: str = "",
        components: Iterable[Component] = (),
        **kwargs,
    ):
        """
        Initialize a container model.

        Args:
            parent:
            technology:
            code_elements:
            size:
            **kwargs:

        """
        super().__init__(**kwargs)
        self.parent = parent
        self.technology = technology
        self._components = set(components)

        self.tags.add(Tags.CONTAINER)

    @property
    def components(self) -> Iterable[Component]:
        """Return read-only list of child components."""
        return list(self._components)

    @property
    def child_elements(self) -> Iterable[Component]:
        """Return child elements (from `Element.children`)."""
        return self.components

    @classmethod
    def hydrate(
        cls,
        container_io: ContainerIO,
        software_system: "SoftwareSystem",
    ) -> "Container":
        """Hydrate a new Container instance from its IO."""
        container = cls(
            **cls.hydrate_arguments(container_io),
            parent=software_system,
            technology=container_io.technology,
        )

        for component_io in container_io.components:
            component = Component.hydrate(component_io, container=container)
            container += component

        return container

    def add_component(self, **kwargs) -> Component:
        """Add a new component to this container."""
        component = Component(**kwargs)
        self += component
        return component

    def __iadd__(self, component: Component) -> "Container":
        """Add a newly constructed component to this container."""
        # TODO: once we move past python 3.6 change to proper return type via
        # __future__.annotations
        if component in self.components:
            return self

        if self.get_component_with_name(component.name):
            raise ValueError(
                f"Component with name {component.name} already exists in {self}."
            )

        if component.parent is None:
            component.parent = self
        elif component.parent is not self:
            raise ValueError(
                f"Component with name {component.name} already has parent "
                f"{component.parent}. Cannot add to {self}."
            )
        self._components.add(component)
        if self.has_model:
            model = self.model
            model += component
        return self

    def get_component_with_name(self, name: str) -> Component:
        """Return a matching `Component` or None if not found."""
        for component in self.components:
            if component.name == name:
                return component
        return None
