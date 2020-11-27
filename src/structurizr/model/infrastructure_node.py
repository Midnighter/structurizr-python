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


"""Provide an infrastructure node model."""

from typing import TYPE_CHECKING, Optional

from ..mixin.childless_mixin import ChildlessMixin
from .deployment_element import DeploymentElement, DeploymentElementIO
from .tags import Tags


if TYPE_CHECKING:  # pragma: no cover
    from .deployment_node import DeploymentNode


__all__ = ("InfrastructureNode", "InfrastructureNodeIO")


class InfrastructureNodeIO(DeploymentElementIO):
    """
    Represent an infrastructure node.

    An infrastructure node is something like:
       * Load balancer
       * Firewall
       * DNS service
       * etc
    """

    technology: Optional[str] = ""


class InfrastructureNode(ChildlessMixin, DeploymentElement):
    """
    Represent an infrastructure node.

    An infrastructure node is something like:
       * Load balancer
       * Firewall
       * DNS service
       * etc
    """

    def __init__(
        self,
        *,
        technology: str = "",
        parent: "DeploymentNode" = None,
        **kwargs,
    ):
        """Initialize an infrastructure node model."""
        super().__init__(**kwargs)
        self.technology = technology
        self.tags.add(Tags.INFRASTRUCTURE_NODE)
        self.parent = parent

    @classmethod
    def hydrate(
        cls,
        node_io: InfrastructureNodeIO,
        parent: "DeploymentNode",
    ) -> "InfrastructureNode":
        """Hydrate a new InfrastructureNode instance from its IO."""
        node = cls(
            **cls.hydrate_arguments(node_io),
            technology=node_io.technology,
            parent=parent,
        )
        return node
