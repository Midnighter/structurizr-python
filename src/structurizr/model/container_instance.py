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


"""Provide a container instance model."""


from typing import TYPE_CHECKING

from pydantic import Field

from .container import Container
from .static_structure_element_instance import (
    StaticStructureElementInstance,
    StaticStructureElementInstanceIO,
)
from .tags import Tags


if TYPE_CHECKING:  # pragma: no cover
    from .deployment_node import DeploymentNode


__all__ = ("ContainerInstance", "ContainerInstanceIO")


class ContainerInstanceIO(StaticStructureElementInstanceIO):
    """Represents a container instance which can be added to a deployment node."""

    container_id: str = Field(alias="containerId")


class ContainerInstance(StaticStructureElementInstance):
    """Represents a container instance which can be added to a deployment node."""

    def __init__(self, *, container: Container, **kwargs) -> None:
        """Initialize a container instance."""
        super().__init__(element=container, **kwargs)
        self.tags.add(Tags.CONTAINER_INSTANCE)

    @property
    def container(self) -> Container:
        """Return the container for this instance."""
        return self.element

    @property
    def container_id(self) -> str:
        """Return the ID of the container for this instance."""
        return self.container.id

    @classmethod
    def hydrate(
        cls,
        container_instance_io: ContainerInstanceIO,
        container: Container,
        parent: "DeploymentNode",
    ) -> "ContainerInstance":
        """Hydrate a new ContainerInstance instance from its IO.

        This will also automatically register with the model.
        """
        instance = cls(
            **cls.hydrate_arguments(container_instance_io),
            container=container,
            parent=parent,
        )
        return instance
