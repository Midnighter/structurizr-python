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

from typing import TYPE_CHECKING, Iterable, List

from pydantic import Field

from .container_instance import ContainerInstance, ContainerInstanceIO
from .deployment_element import DeploymentElement, DeploymentElementIO


if TYPE_CHECKING:
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


DeploymentNodeIO.update_forward_refs()


class DeploymentNode(DeploymentElement):
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

    def __init__(
        self,
        *,
        parent: "DeploymentNode" = None,
        technology: str = "",
        instances: int = 1,
        children: Iterable["DeploymentNode"] = (),
        container_instances: Iterable[ContainerInstance] = (),
        **kwargs,
    ) -> None:
        """Initialize a deployment node."""
        super().__init__(**kwargs)
        self.parent = parent
        self.technology = technology
        self.instances = instances
        self._children = set(children)
        self._container_instances = set(container_instances)

    @property
    def children(self) -> Iterable["DeploymentNode"]:
        """Return read-only list of child nodes."""
        return list(self._children)

    @property
    def container_instances(self) -> Iterable[ContainerInstance]:
        """Return read-only list of container instances."""
        return list(self._container_instances)

    def add_deployment_node(self, **kwargs) -> "DeploymentNode":
        """Add a new child deployment node to this node."""
        node = DeploymentNode(**kwargs)
        self += node
        return node

    def __iadd__(self, node: "DeploymentNode") -> "DeploymentNode":
        """Add a newly constructed chile deployment node to this node."""
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
        self._children.add(node)
        model = self.model
        model += node
        return self

    @classmethod
    def hydrate(
        cls,
        deployment_node_io: DeploymentNodeIO,
        model: "Model",
        parent: "DeploymentNode" = None,
    ) -> "DeploymentNode":
        """Hydrate a new DeploymentNode instance from its IO.

        This will also automatically register with the model.
        """
        node = cls(
            parent=parent,
            **cls.hydrate_arguments(deployment_node_io),
        )
        model += node

        for child_io in deployment_node_io.children:
            child_node = DeploymentNode.hydrate(child_io, model=model, parent=node)
            node += child_node

        return node
