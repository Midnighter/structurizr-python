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


"""Provide a softwrae system instance model."""


from typing import TYPE_CHECKING

from pydantic import Field

from .software_system import SoftwareSystem
from .static_structure_element_instance import (
    StaticStructureElementInstance,
    StaticStructureElementInstanceIO,
)
from .tags import Tags


if TYPE_CHECKING:  # pragma: no cover
    from .deployment_node import DeploymentNode


__all__ = ("SoftwareSystemInstance", "SoftwareSystemInstanceIO")


class SoftwareSystemInstanceIO(StaticStructureElementInstanceIO):
    """Represents a software system instance which can be added to a deployment node."""

    software_system_id: str = Field(alias="softwareSystemId")


class SoftwareSystemInstance(StaticStructureElementInstance):
    """Represents a software system instance which can be added to a deployment node."""

    def __init__(self, *, software_system: SoftwareSystem, **kwargs) -> None:
        """Initialize a software system instance."""
        super().__init__(element=software_system, **kwargs)
        self.tags.add(Tags.SOFTWARE_SYSTEM_INSTANCE)

    @property
    def software_system(self) -> SoftwareSystem:
        """Return the software system for this instance."""
        return self.element

    @property
    def software_system_id(self) -> str:
        """Return the ID of the software system for this instance."""
        return self.software_system.id

    @classmethod
    def hydrate(
        cls,
        system_instance_io: SoftwareSystemInstanceIO,
        system: SoftwareSystem,
        parent: "DeploymentNode",
    ) -> "SoftwareSystemInstance":
        """Hydrate a new SoftwareSystemInstance instance from its IO."""
        instance = cls(
            **cls.hydrate_arguments(system_instance_io),
            software_system=system,
            parent=parent,
        )
        return instance
