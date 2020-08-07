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


"""Provide a software architecture model."""


import logging
from typing import Iterable, List, Optional, ValuesView

from pydantic import Field

from structurizr.model.deployment_node import DeploymentNode, DeploymentNodeIO

from ..abstract_base import AbstractBase
from ..base_model import BaseModel
from .container import Container
from .container_instance import ContainerInstance
from .element import Element
from .enterprise import Enterprise, EnterpriseIO
from .person import Person, PersonIO
from .relationship import Relationship
from .sequential_integer_id_generator import SequentialIntegerIDGenerator
from .software_system import SoftwareSystem, SoftwareSystemIO


__all__ = ("ModelIO", "Model")


logger = logging.getLogger(__name__)


class ModelIO(BaseModel):
    """
    Represent a software architecture model.

    Attributes:
        enterprise (Enterprise): The enterprise associated with this model.
        people (set of Person): The set of people belonging to this model.
        software_systems (set of SoftwareSystem): The set of software systems belonging
            to this model.
        deployment_nodes (set of DeploymentNode): The set of deployment nodes belonging
            to this model.

    """

    enterprise: Optional[EnterpriseIO] = Field(
        default=None, description="The enterprise associated with this model."
    )
    people: List[PersonIO] = Field(
        default=[], description="The set of people belonging to this model."
    )
    software_systems: List[SoftwareSystemIO] = Field(
        default=[],
        alias="softwareSystems",
        description="The set of software systems belonging to this model.",
    )
    deployment_nodes: List[DeploymentNodeIO] = Field(
        default=[],
        alias="deploymentNodes",
        description="The set of deployment nodes belonging to this model.",
    )


class Model(AbstractBase):
    """
    Represent a software architecture model.

    Attributes:
        enterprise (Enterprise): The enterprise associated with this model.
        people (set of Person): The set of people belonging to this model.
        software_systems (set of SoftwareSystem): The set of software systems belonging
            to this model.
        deployment_nodes (set of DeploymentNode): The set of deployment nodes belonging
            to this model.

    """

    def __init__(
        self,
        enterprise: Optional[Enterprise] = None,
        people: Optional[Iterable[Person]] = (),
        software_systems: Iterable[SoftwareSystem] = (),
        deployment_nodes: Iterable[DeploymentNode] = (),
        **kwargs,
    ) -> None:
        """
        Initialize the model with its 'private' attributes.

        Args:
            **kwargs: Passed on to the parent constructor.

        """
        super().__init__(**kwargs)
        self.enterprise = enterprise
        self.people = set(people)
        self.software_systems = set(software_systems)
        self.deployment_nodes = set(deployment_nodes)
        # TODO: simply iterate attributes
        self._elements_by_id = {}
        self._relationships_by_id = {}
        self._id_generator = SequentialIntegerIDGenerator()

    def __contains__(self, element: Element):
        return element in self.get_elements()

    @classmethod
    def hydrate(cls, model_io: ModelIO) -> "Model":
        """"""
        model = cls(
            enterprise=Enterprise.hydrate(model_io.enterprise)
            if model_io.enterprise is not None
            else None,
            # TODO: relationships
        )

        for person_io in model_io.people:
            person = Person.hydrate(person_io)
            model.add_person(person=person)

        for software_system_io in model_io.software_systems:
            software_system = SoftwareSystem.hydrate(software_system_io)
            model.add_software_system(software_system=software_system)

        for deployment_node_io in model_io.deployment_nodes:
            deployment_node = DeploymentNode.hydrate(deployment_node_io)
            model.add_deployment_node(deployment_node=deployment_node)

        for element in model.get_elements():
            for relationship in element.relationships:  # type: Relationship
                relationship.source = model.get_element(relationship.source_id)
                relationship.destination = model.get_element(
                    relationship.destination_id
                )
                model.add_relationship(relationship)

        return model

    def add_person(self, person=None, **kwargs) -> Person:
        """
        Add a new person to the model.

        Args:
            person (Person, optional): Either provide a `Person` instance or
            **kwargs: Provide keyword arguments for instantiating a `Person`
                (recommended).

        Returns:
            Person: Either the same or a new instance, depending on arguments.

        Raises:
            ValueError: When a person with the same name already exists.

        See Also:
            Person

        """
        if person is None:
            person = Person(**kwargs)
        if any(person.name == p.name for p in self.people):
            ValueError(
                f"A person with the name '{person.name}' already exists in the model."
            )
        self._add_element(person)
        self.people.add(person)
        return person

    def add_software_system(self, software_system=None, **kwargs) -> SoftwareSystem:
        """
        Add a new software system to the model.

        Args:
            software_system (SoftwareSystem, optional): Either provide a
                `SoftwareSystem` instance or
            **kwargs: Provide keyword arguments for instantiating a `SoftwareSystem`
                (recommended).

        Returns:
            SoftwareSystem: Either the same or a new instance, depending on arguments.

        Raises:
            ValueError: When a software system with the same name already exists.

        See Also:
            SoftwareSystem

        """
        if software_system is None:
            software_system = SoftwareSystem(**kwargs)
        if any(software_system.name == s.name for s in self.software_systems):
            ValueError(
                f"A software system with the name {software_system.name} already "
                f"exists in the model."
            )
        self._add_element(software_system)
        self.software_systems.add(software_system)
        return software_system

    def add_container(
        self, container: Optional[Container] = None, **kwargs
    ) -> Container:
        """
        Add a new container to the model.

        Args:
            container (Container, optional): Either provide a
                `Container` instance or
            **kwargs: Provide keyword arguments for instantiating a `Container`
                (recommended).

        Returns:
            SoftwareSystem: Either the same or a new instance, depending on arguments.

        Raises:
            ValueError: When a container with the same name already exists.

        See Also:
            Container

        """
        if container is None:
            container = Container(**kwargs)
        if any(container.name == c.name for c in container.parent.containers):
            ValueError(
                f"A container with the name {container.name} already "
                f"exists in the model."
            )
        # TODO (midnighter): Modifying the parent seems like creating an undesired
        #  tight link here.
        container.parent.add(container)
        self._add_element(container)
        return container

    def add_container_instance(
        self,
        deployment_node: DeploymentNode,
        container: Container,
        replicate_container_relationships: bool,
    ) -> ContainerInstance:
        """
        Add a new container instance to the model.

        Args:
            deployment_node (DeploymentNode, optional): `DeploymentNode` instance
            container (Container, optional): `Container` instance

        Returns:
            ContainerInstance: A container instance.

        Raises:
            ValueError: When a container with the same name already exists.

        See Also:
            ContainerInstance

        """
        if container is None:
            raise ValueError("A container must be specified.")
        # TODO: implement
        # instance_number =

    def add_deployment_node(
        self, deployment_node: Optional[DeploymentNode] = None, **kwargs
    ) -> DeploymentNode:
        """
        Add a new deployment node to the model.
        Args:
            deployment_node (DeploymentNode, optional): Either provide a
                `DeploymentNode` instance or
            **kwargs: Provide keyword arguments for instantiating a `DeploymentNode`
                (recommended).

        Returns:
            DeploymentNode: Either the same or a new instance, depending on arguments.

        Raises:
            ValueError: When a deployment node with the same name already exists.

        See Also:
            DeploymentNode

        """
        if deployment_node is None:
            deployment_node = DeploymentNode(**kwargs)
        if deployment_node.id in {d.id for d in self.deployment_nodes}:
            ValueError(
                f"A deployment node with the ID {deployment_node.id} already "
                f"exists in the model."
            )
        self.deployment_nodes.add(deployment_node)
        self._add_element(deployment_node)
        return deployment_node

    def add_relationship(
        self, relationship: Relationship = None, **kwargs
    ) -> Optional[Relationship]:
        """
        Add a relationship to the model.

        Args:
            relationship (Relationship, optional): Either provide a
                `Relationship` instance or
            **kwargs: Provide keyword arguments for instantiating a `Relationship`
                (recommended).

        Returns:
            Relationship: Either the same or a new instance, depending on arguments.

        Raises:
            ValueError: When a relationship with the same ID already exists.

        See Also:
            Relationship

        """

        if relationship is None:
            relationship = Relationship(**kwargs)
        # Check
        if self._add_relationship(relationship):
            return relationship
        else:
            return

    def get_element(self, id: str) -> Optional[Element]:
        """
        Retrieve an element by its identifier if it exists.

        Args:
            id (str): The identifier of the requested element.

        Returns:
            Element or None: The corresponding element if it exists.

        """
        return self._elements_by_id.get(id)

    def get_relationship(self, id: str) -> Optional[Relationship]:
        """
        Retrieve a relationship by its identifier if it exists.

        Args:
            id (str): The identifier of the requested relationship.

        Returns:
            Relationship or None: The corresponding relationship if it exists.

        """
        return self._relationships_by_id.get(id)

    def get_relationships(self) -> ValuesView[Relationship]:
        """Return an iterator over all relationships contained in this model."""
        return self._relationships_by_id.values()

    def get_elements(self) -> ValuesView[Element]:
        return self._elements_by_id.values()

    def get_software_system_with_id(self, id: str) -> Optional[SoftwareSystem]:
        result = self.get_element(id)
        if not isinstance(result, SoftwareSystem):
            return None
        return result

    def _add_element(self, element: Element) -> None:
        """"""
        if not element.id:
            element.id = self._id_generator.generate_id()
        elif (
            element.id in self._elements_by_id
            or element.id in self._relationships_by_id
        ):
            raise ValueError(f"The element {element} has an existing ID.")
        self._elements_by_id[element.id] = element
        element.set_model(self)
        self._id_generator.found(element.id)

    def _add_relationship(self, relationship: Relationship) -> bool:
        """"""
        if not relationship.id:
            relationship.id = self._id_generator.generate_id()
        elif (
            # TODO(ilaif): @midnighter: not sure this is the best check,
            #  we should have a global id check?
            relationship.id in self._elements_by_id
            or relationship.id in self._relationships_by_id
        ):
            raise ValueError(f"The relationship {relationship} has an existing ID.")
        relationship.source.add_relationship(relationship)
        self._add_relationship_to_internal_structures(relationship)
        return True

    def _add_relationship_to_internal_structures(self, relationship: Relationship):
        self._relationships_by_id[relationship.id] = relationship
        self._id_generator.found(relationship.id)
