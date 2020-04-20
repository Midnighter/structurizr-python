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


from typing import TYPE_CHECKING, Iterable, List

from pydantic import Field

from .deployment_element import DeploymentElement, DeploymentElementIO


if TYPE_CHECKING:
    from .container import Container, ContainerIO
    from .http_health_check import HTTPHealthCheck, HTTPHealthCheckIO


__all__ = ("ContainerInstance", "ContainerInstanceIO")


DEFAULT_HEALTH_CHECK_INTERVAL_IN_SECONDS = 60
DEFAULT_HEALTH_CHECK_TIMEOUT_IN_MILLISECONDS = 0


class ContainerInstanceIO(DeploymentElementIO):
    """
    Represents a container instance which can be added to a deployment node.

    Attributes:

    """

    container: "ContainerIO"
    container_id: str
    instance_id: int
    health_checks: List["HTTPHealthCheckIO"] = Field([], alias="healthChecks")


class ContainerInstance(DeploymentElement):
    """
    Represents a container instance which can be added to a deployment node.

    Attributes:

    """

    def __init__(
        self,
        *,
        container: "Container",
        container_id: str,
        instance_id: int,
        health_checks: Iterable["HTTPHealthCheck"] = (),
        **kwargs
    ) -> None:
        """Initialize a container instance."""
        super().__init__(**kwargs)
        self.container = container
        self.container_id = container_id
        self.instance_id = instance_id
        self.health_checks = set(health_checks)
