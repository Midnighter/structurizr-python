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


"""Provide a deployment node model."""


from typing import Iterable

from .deployment_element import DeploymentElement, DeploymentElementIO


__all__ = ("DeploymentNode", "DeploymentNodeIO")


class DeploymentNodeIO(DeploymentElementIO):
    """
    Represent a deployment node.

    Attributes:

    """

    parent: "DeploymentNodeIO"
    technology: str = ""
    instances: int = 1


class DeploymentNode(DeploymentElement):
    """
    Represent a deployment node.

    Attributes:

    """

    def __init__(
        self,
        *,
        parent: "DeploymentNode",
        technology: str = "",
        instances: int = 1,
        children: Iterable["DeploymentNode"] = (),
        container_instances: Iterable["DeploymentNode"] = (),
        **kwargs
    ) -> None:
        """Initialize a deployment node."""
        super().__init__(**kwargs)
        self.parent = parent
        self.technology = technology
        self.instances = instances
        self.children = set(children)
        self.container_instances = set(container_instances)
