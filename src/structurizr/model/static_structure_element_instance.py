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


"""Provide a superclass for container and software system instances."""


from abc import ABC
from typing import TYPE_CHECKING, Iterable, List, Optional, Set

from pydantic import Field

from ..mixin.childless_mixin import ChildlessMixin
from .deployment_element import DeploymentElement, DeploymentElementIO
from .http_health_check import HTTPHealthCheck, HTTPHealthCheckIO
from .static_structure_element import StaticStructureElement


if TYPE_CHECKING:  # pragma: no cover
    from .deployment_node import DeploymentNode

__all__ = ("StaticStructureElementInstance", "StaticStructureElementInstanceIO")


class StaticStructureElementInstanceIO(DeploymentElementIO, ABC):
    """Define a superclass for instances of container and software system."""

    name: Optional[str] = ""  # Name is not serialisable for instances

    instance_id: int = Field(alias="instanceId")
    health_checks: List[HTTPHealthCheckIO] = Field(default=(), alias="healthChecks")


class StaticStructureElementInstance(ChildlessMixin, DeploymentElement, ABC):
    """Define a superclass for all deployment instances."""

    def __init__(
        self,
        *,
        element: StaticStructureElement,
        instance_id: int,
        health_checks: Iterable["HTTPHealthCheck"] = (),
        parent: "DeploymentNode" = None,
        **kwargs
    ) -> None:
        """Initialize a StaticStructureElementInstance."""
        # The name of the instance comes from element it contains - see
        # StaticStructureElementInstance.getName() in the Java API.
        kwargs["name"] = element.name
        super().__init__(**kwargs)
        self.element = element
        self.instance_id = instance_id
        self.health_checks = set(health_checks)
        self.parent = parent

    def replicate_element_relationships(self):
        """
        Replicate relationships from the element of this instance.

        This looks at the relationships to and from the element of this instance and
        sets up the equivalent relationships between the corresponding instances in
        the same environment.
        """
        # Find all the element instances in the same deployment environment
        element_instances: Set[StaticStructureElementInstance] = {
            e
            for e in self.model.get_elements()
            if isinstance(e, StaticStructureElementInstance)
            and e.environment == self.environment
        }

        for other_element_instance in element_instances:
            other_element = other_element_instance.element

            for relationship in self.element.relationships:
                if relationship.destination is other_element:
                    self.add_relationship(
                        destination=other_element_instance,
                        description=relationship.description,
                        technology=relationship.technology,
                        interaction_style=relationship.interaction_style,
                        linked_relationship_id=relationship.id,
                    ).tags.clear()
            for relationship in other_element.relationships:
                if relationship.destination is self.element:
                    other_element_instance.add_relationship(
                        destination=self,
                        description=relationship.description,
                        technology=relationship.technology,
                        interaction_style=relationship.interaction_style,
                        linked_relationship_id=relationship.id,
                    ).tags.clear()

    @classmethod
    def hydrate_arguments(cls, instance_io: StaticStructureElementInstanceIO) -> dict:
        """Build constructor arguments from IO."""

        return {
            **super().hydrate_arguments(instance_io),
            "instance_id": instance_io.instance_id,
            "health_checks": map(HTTPHealthCheck.hydrate, instance_io.health_checks),
        }
