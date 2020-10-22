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
from typing import Iterable, List, Optional

from pydantic import Field, HttpUrl

from .deployment_element import DEFAULT_DEPLOYMENT_ENVIRONMENT, DeploymentElement
from .http_health_check import HTTPHealthCheck, HTTPHealthCheckIO
from .model_item import ModelItem, ModelItemIO
from .relationship import Relationship, RelationshipIO
from .static_structure_element import StaticStructureElement


__all__ = ("StaticStructureElementInstance", "StaticStructureElementInstanceIO")


class StaticStructureElementInstanceIO(ModelItemIO, ABC):
    """
    Define a superclass for instances of container and software system.

    Implementation note:
    In this case, the IO does not reflect the same inheritance hierarchy
    as the main class.  This is because instances do not have the `name` field
    and so we cannot extend `ElementIO` which enforces that `name` is populated.
    See http://github.com/structurizr/json/blob/master/structurizr.yaml.
    """

    description: str = Field(default="")
    url: Optional[HttpUrl] = Field(default=None)
    relationships: List[RelationshipIO] = Field(default=())

    environment: Optional[str] = DEFAULT_DEPLOYMENT_ENVIRONMENT
    instance_id: int = Field(alias="instanceId")
    health_checks: List[HTTPHealthCheckIO] = Field(default=(), alias="healthChecks")


class StaticStructureElementInstance(DeploymentElement, ABC):
    """Define a superclass for all deployment instances."""

    def __init__(
        self,
        *,
        element: StaticStructureElement,
        instance_id: int,
        health_checks: Iterable["HTTPHealthCheck"] = (),
        **kwargs
    ) -> None:
        """Initialize a StaticStructureElementInstance."""
        # The name of the instance comes from element it contains - see
        # StaticStructureElementInstance.getName() in the Java API.
        super().__init__(name=element.name, **kwargs)
        self.instance_id = instance_id
        self.health_checks = set(health_checks)

    @classmethod
    def hydrate_arguments(cls, instance_io: StaticStructureElementInstanceIO) -> dict:
        """Build constructor arguments from IO."""

        # See note in DeploymentInstanceIO on why we're not using super() here.
        return {
            **ModelItem.hydrate_arguments(instance_io),
            "description": instance_io.description,
            "url": instance_io.url,
            "relationships": map(Relationship.hydrate, instance_io.relationships),
            "environment": instance_io.environment,
            "instance_id": instance_io.instance_id,
            "health_checks": map(HTTPHealthCheck.hydrate, instance_io.health_checks),
        }
