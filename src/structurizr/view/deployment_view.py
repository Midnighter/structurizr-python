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


"""Provide a component view.

Used to show the mapping of container instances to deployment nodes.
"""

from typing import Iterable, Optional, Union

from ..mixin.model_ref_mixin import ModelRefMixin
from ..model.container_instance import ContainerInstance
from ..model.deployment_node import DeploymentNode
from ..model.infrastructure_node import InfrastructureNode
from ..model.relationship import Relationship
from ..model.software_system_instance import SoftwareSystemInstance
from .animation import Animation
from .view import View


__all__ = ("DeploymentView", "DeploymentViewIO")


class DeploymentViewIO:
    pass


class DeploymentView(ModelRefMixin, View):
    def __init__(
        self,
        *,
        environment: Optional[str] = None,
        animations: Optional[Iterable[Animation]] = None,
        **kwargs,
    ) -> None:
        """Initialize a deployment view."""
        super().__init__(**kwargs)
        self._environment = environment
        self._animations = [] if animations is None else list(animations)

    @property
    def environment(self):
        """Get the name of the environment that this view is for.

        E.g. "Development", "Live", etc.
        """
        return self._environment

    def add_default_elements(self):
        """Add the default set of elements to this view."""
        self.add_all_deployment_nodes()

    def add_all_deployment_nodes(self):
        """Add all of the top-level deployment nodes to this view.

        If the environment is set in this view, then only nodes from the same
        environment will be added.
        """
        for deployment_node in self.model.deployment_nodes:
            if deployment_node.parent is None:
                if (
                    self.environment is None
                    or self.environment == deployment_node.environment
                ):
                    self.add(deployment_node)

    def add(
        self, item: Union[DeploymentNode, Relationship], add_relationships: bool = True
    ):
        """Add a deployment node or relationship to this view."""
        if isinstance(item, DeploymentNode):
            if self._add_node_children(item, add_relationships):
                parent = item.parent
                while parent is not None:
                    self._add_element(parent, add_relationships)
                    parent = parent.parent
        else:
            pass  # TODO

    def remove(
        self,
        item: Union[
            DeploymentNode,
            InfrastructureNode,
            ContainerInstance,
            SoftwareSystemInstance,
        ],
    ):
        """Remove the given item from this view."""
        pass  # TODO

    def _add_node_children(
        self, deployment_node: DeploymentNode, add_relationships: bool
    ):
        has_elements_or_relationships = False
        for instance in deployment_node.software_system_instances:
            self._add_element(instance, add_relationships)
            has_elements_or_relationships = True

        for instance in deployment_node.container_instances:
            container = instance.container
            if self.software_system is None or container.parent is self.software_system:
                self._add_element(instance, add_relationships)
                has_elements_or_relationships = True

        for node in deployment_node.infrastructure_nodes:
            self._add_element(node, add_relationships)
            has_elements_or_relationships = True

        for child in deployment_node.children:
            has_elements_or_relationships |= self._add_node_children(
                child, add_relationships
            )

        if has_elements_or_relationships:
            self._add_element(deployment_node, add_relationships)

        return has_elements_or_relationships

    @property
    def name(self):
        """Get the (computed) name of this view."""
        name = (
            "Deployment"
            if self.software_system is None
            else f"{self.software_system.name} - Deployment"
        )
        if self.environment:
            name = f"{name} - {self.environment}"
        return name

    # def can_be_removed(element: Element)

    # def add_animation(element_instances)

    # def add_animation_step(elements)

    # def _find_deployment_node(element: Element)

    @property
    def animations(self) -> Iterable[Animation]:
        pass  # TODO
