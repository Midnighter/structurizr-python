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


"""Provide a deployment view.

Used to show the mapping of container instances to deployment nodes.
"""

from typing import Iterable, List, Optional, Union

from ..mixin.model_ref_mixin import ModelRefMixin
from ..model.container_instance import ContainerInstance
from ..model.deployment_element import DeploymentElement
from ..model.deployment_node import DeploymentNode
from ..model.infrastructure_node import InfrastructureNode
from ..model.relationship import Relationship
from ..model.software_system_instance import SoftwareSystemInstance
from ..model.static_structure_element import StaticStructureElement
from .animation import Animation, AnimationIO
from .view import View, ViewIO


__all__ = ("DeploymentView", "DeploymentViewIO")


class DeploymentViewIO(ViewIO):
    """
    Represent a deployment view.

    Attributes:
        environment: the name of the environment that this deployment view is for
                     (e.g. "Development", "Live", etc.)
        animations: the set of animation steps (optional)
    """

    environment: Optional[str] = None
    animations: List[AnimationIO] = []


class DeploymentView(ModelRefMixin, View):
    """Represent a deployment view.

    Deployment views are used to show the mapping of container instances to deployment
    nodes.
    """

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
        for deployment_node in self.model.deployment_nodes:  # This returns top-level
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
            self._add_relationship(item)

    def __iadd__(self, item: Union[DeploymentNode, Relationship]) -> "DeploymentView":
        """Add a deployment node or relationship to this view."""
        self.add(item)
        return self

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
        if isinstance(item, DeploymentNode):
            child_items = (
                item.container_instances
                + item.software_system_instances
                + item.infrastructure_nodes
                + item.children
            )
            for child in child_items:
                self.remove(child)
        self._remove_element(item)

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

    def add_animation(
        self, *element_instances: Union[StaticStructureElement, InfrastructureNode]
    ):
        """Add an animation step, with the given elements and infrastructure nodes."""
        if len(element_instances) == 0:
            raise ValueError(
                "One or more software system/container instances and/or "
                + "infrastructure nodes must be specified"
            )

        element_ids_in_previous_steps = set()
        for step in self.animations:
            element_ids_in_previous_steps = element_ids_in_previous_steps.union(
                step.elements
            )

        element_ids_in_this_step = set()
        relationship_ids_in_this_step = set()

        for element in element_instances:
            if (
                self.is_element_in_view(element)
                and element.id not in element_ids_in_previous_steps
            ):
                element_ids_in_previous_steps.add(element.id)
                element_ids_in_this_step.add(element.id)

                deployment_node = self._find_deployment_node(element)
                while deployment_node is not None:
                    if deployment_node.id not in element_ids_in_previous_steps:
                        element_ids_in_previous_steps.add(deployment_node.id)
                        element_ids_in_this_step.add(deployment_node.id)
                    deployment_node = deployment_node.parent

        if element_ids_in_this_step == set():
            raise ValueError("None of the specified instances exist in this view.")

        for relationship_view in self.relationship_views:
            relationship = relationship_view.relationship
            if (
                relationship.source.id in element_ids_in_this_step
                and relationship.destination.id in element_ids_in_previous_steps
            ) or (
                relationship.destination.id in element_ids_in_this_step
                and relationship.source.id in element_ids_in_previous_steps
            ):
                relationship_ids_in_this_step.add(relationship.id)

        self._animations.append(
            Animation(
                order=len(self._animations) + 1,
                elements=element_ids_in_this_step,
                relationships=relationship_ids_in_this_step,
            )
        )

    def _find_deployment_node(self, element: DeploymentElement) -> DeploymentNode:
        all_deployment_nodes = [
            e for e in self.model.get_elements() if isinstance(e, DeploymentNode)
        ]
        for node in all_deployment_nodes:
            if (
                element in node.container_instances
                or element in node.software_system_instances
                or element in node.infrastructure_nodes
            ):
                return node
        return None

    @property
    def animations(self) -> Iterable[Animation]:
        """Return the animations for this view."""
        return list(self._animations)

    @classmethod
    def hydrate(cls, deployment_view_io: DeploymentViewIO) -> "DeploymentView":
        """Hydrate a new DeploymentView instance from its IO."""
        return cls(
            environment=deployment_view_io.environment,
            animations=map(Animation.hydrate, deployment_view_io.animations),
            **cls.hydrate_arguments(deployment_view_io),
        )
