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

from typing import TYPE_CHECKING, Iterable, List, Optional, Union

from pydantic import Field

from .container import Container
from .container_instance import ContainerInstance, ContainerInstanceIO
from .deployment_element import DeploymentElement, DeploymentElementIO
from .element import Element
from .infrastructure_node import InfrastructureNode, InfrastructureNodeIO
from .relationship import Relationship
from .software_system import SoftwareSystem
from .software_system_instance import SoftwareSystemInstance, SoftwareSystemInstanceIO
from .tags import Tags


if TYPE_CHECKING:  # pragma: no cover
    from .model import Model

__all__ = ("DeploymentNode", "DeploymentNodeIO")


class DeploymentNodeIO(DeploymentElementIO):
    """
    Represent a deployment node.

    Attributes:
        id: The ID of this deployment node in the model.
        name: The name of this node.
        description: A short description of this node.
        environment (str):
        tags: A comma separated list of tags associated with this node.
        children: The deployment nodes that are direct children of this node.
        properties: A set of arbitrary name-value properties.
        relationships: The set of relationships from this node to
                       other elements.
        url (pydantic.HttpUrl):
    """

    class Config:
        """Pydantic configuration for DeploymentNodeIO."""

        # Prevent infinite recursion for `children` - see
        # https://github.com/samuelcolvin/pydantic/issues/524
        validate_assignment = "limited"

    technology: str = ""
    instances: int = 1
    children: List["DeploymentNodeIO"] = Field(default=())
    container_instances: List[ContainerInstanceIO] = Field(
        default=(), alias="containerInstances"
    )
    software_system_instances: List[SoftwareSystemInstanceIO] = Field(
        default=(), alias="softwareSystemInstances"
    )
    infrastructure_nodes: List[InfrastructureNodeIO] = Field(
        default=(), alias="infrastructureNodes"
    )


DeploymentNodeIO.update_forward_refs()


class DeploymentNode(DeploymentElement):
    """
    Represent a deployment node.

    Attributes:
        id: The ID of this deployment node in the model.
        name: The name of this node.
        description: A short description of this node.
        environment (str): The environment this node lives in.
        tags: A comma separated list of tags associated with this node.
        children: The deployment nodes that are direct children of this node.
        properties: A set of arbitrary name-value properties.
        relationships: The set of relationships from this node to
                       other elements.
        url (pydantic.HttpUrl):
    """

    def __init__(
        self,
        *,
        parent: Optional["DeploymentNode"] = None,
        technology: str = "",
        instances: int = 1,
        children: Iterable["DeploymentNode"] = (),
        container_instances: Iterable[ContainerInstance] = (),
        software_system_instances: Iterable[SoftwareSystemInstance] = (),
        infrastructure_nodes: Iterable[InfrastructureNode] = (),
        **kwargs,
    ) -> None:
        """Initialize a deployment node."""
        super().__init__(**kwargs)
        self.parent = parent
        self.technology = technology
        self.instances = instances
        self._children = set(children)
        self._container_instances = set(container_instances)
        self._software_system_instances = set(software_system_instances)
        self._infrastructure_nodes = set(infrastructure_nodes)
        self.tags.add(Tags.DEPLOYMENT_NODE)

    @property
    def children(self) -> Iterable["DeploymentNode"]:
        """Return read-only list of child nodes."""
        return list(self._children)

    @property
    def child_elements(self) -> Iterable[Element]:
        """Return child elements (from `Element.children`)."""
        return (
            self.children
            + self.container_instances
            + self.software_system_instances
            + self.infrastructure_nodes
        )

    @property
    def container_instances(self) -> Iterable[ContainerInstance]:
        """Return read-only list of container instances."""
        return list(self._container_instances)

    @property
    def software_system_instances(self) -> Iterable[SoftwareSystemInstance]:
        """Return read-only list of software system instances."""
        return list(self._software_system_instances)

    @property
    def infrastructure_nodes(self) -> Iterable[InfrastructureNode]:
        """Return read-only list of infrastructure nodes."""
        return list(self._infrastructure_nodes)

    def add_deployment_node(
        self, name: str, description: str = "", technology: str = "", **kwargs
    ) -> "DeploymentNode":
        """
        Add a new child deployment node to this node.

        Args:
            name(str): Name of the deployment node
            description(str): Optional description
            technology(str): Optional technologies
            **kwargs: additional keyword arguments for instantiating a `DeploymentNode`
        """
        node = DeploymentNode(
            name=name,
            description=description,
            technology=technology,
            environment=self.environment,
            **kwargs,
        )
        self._add_child_deployment_node(node)
        return node

    def add_container(
        self, container: Container, *, replicate_relationships: bool = True
    ) -> ContainerInstance:
        """
        Create a new instance of a container in this deployment node.

        Args:
            container(Container): the Container to add an instance of.
            replicate_relationships: True if relationships should be replicated between
                                     the element instances in the same deployment
                                     environment, False otherwise.
        """
        instance_id = (
            max(
                [
                    c.instance_id
                    for c in self.container_instances
                    if c.container is container
                ],
                default=0,
            )
            + 1
        )
        instance = ContainerInstance(
            container=container,
            instance_id=instance_id,
            environment=self.environment,
            parent=self,
        )
        self._container_instances.add(instance)
        model = self.model
        model += instance
        if replicate_relationships:
            instance.replicate_element_relationships()
        return instance

    def add_software_system(
        self, software_system: SoftwareSystem, *, replicate_relationships: bool = True
    ) -> SoftwareSystemInstance:
        """
        Create a new instance of a software system in this deployment node.

        Args:
            software_system(SoftwareSystem): the SoftwareSystem to add an instance of.
            replicate_relationships: True if relationships should be replicated between
                                     the element instances in the same deployment
                                     environment, False otherwise.
        """
        instance_id = (
            max(
                [
                    s.instance_id
                    for s in self.software_system_instances
                    if s.software_system is software_system
                ],
                default=0,
            )
            + 1
        )
        instance = SoftwareSystemInstance(
            software_system=software_system,
            instance_id=instance_id,
            environment=self.environment,
            parent=self,
        )
        self._software_system_instances.add(instance)
        model = self.model
        model += instance
        if replicate_relationships:
            instance.replicate_element_relationships()
        return instance

    def add_infrastructure_node(self, name: str, **kwargs) -> InfrastructureNode:
        """Create a new infrastructure node under this node."""
        infra_node = InfrastructureNode(name=name, parent=self, **kwargs)
        self._add_infrastructure_node(infra_node)
        return infra_node

    def __iadd__(
        self,
        child: Union[Container, "DeploymentNode", InfrastructureNode, SoftwareSystem],
    ) -> "DeploymentNode":
        """Add a sub-node, container, system or infra node to this node."""
        if isinstance(child, SoftwareSystem):
            self.add_software_system(child)
        elif isinstance(child, Container):
            self.add_container(child)
        elif isinstance(child, InfrastructureNode):
            self._add_infrastructure_node(child)
        else:
            self._add_child_deployment_node(child)
        return self

    def uses(
        self,
        destination: "DeploymentNode",
        description: str = "Uses",
        technology: str = "",
        **kwargs,
    ) -> Optional["Relationship"]:
        """Add a relationship between this and another deployment node."""
        return self.model.add_relationship(
            source=self,
            destination=destination,
            description=description,
            technology=technology,
            **kwargs,
        )

    def _add_infrastructure_node(self, infra_node: InfrastructureNode):
        """Add a new infrastructure node."""
        self._infrastructure_nodes.add(infra_node)
        model = self.model
        model += infra_node

    def _add_child_deployment_node(self, node: "DeploymentNode"):
        """Add a newly constructed child deployment node to this node."""
        if node in self._children:
            return self

        if any(node.name == child.name for child in self.children):
            raise ValueError(
                f"A deployment node with the name '{node.name}' already "
                f"exists in node '{self.name}'."
            )

        if node.parent is None:
            node.parent = self
        elif node.parent is not self:
            raise ValueError(
                f"DeploymentNode with name '{node.name}' already has parent "
                f"{node.parent}. Cannot add to {self}."
            )

        if node.environment != self.environment:
            raise ValueError(
                f"DeploymentNode {node.name} cannot be in a different environment "
                f"({node.environment}) from its parent ({self.environment})."
            )

        self._children.add(node)
        if self.has_model:
            model = self.model
            model += node

    @classmethod
    def hydrate(
        cls,
        deployment_node_io: DeploymentNodeIO,
        model: "Model",
        parent: "DeploymentNode" = None,
    ) -> "DeploymentNode":
        """Hydrate a new DeploymentNode instance from its IO."""
        node = cls(
            **cls.hydrate_arguments(deployment_node_io),
            parent=parent,
        )

        for child_io in deployment_node_io.children:
            child_node = DeploymentNode.hydrate(child_io, model=model, parent=node)
            node += child_node

        for instance_io in deployment_node_io.container_instances:
            container = model.get_element(instance_io.container_id)
            instance = ContainerInstance.hydrate(
                instance_io, container=container, parent=node
            )
            node._container_instances.add(instance)

        for instance_io in deployment_node_io.software_system_instances:
            system = model.get_element(instance_io.software_system_id)
            instance = SoftwareSystemInstance.hydrate(
                instance_io, system=system, parent=node
            )
            node._software_system_instances.add(instance)

        for infra_node_io in deployment_node_io.infrastructure_nodes:
            infra_node = InfrastructureNode.hydrate(infra_node_io, parent=node)
            node._infrastructure_nodes.add(infra_node)

        return node
