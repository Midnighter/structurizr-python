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
from typing import Any, Iterable, Iterator, List, Optional, Set

from pydantic import Field

from ..abstract_base import AbstractBase
from ..base_model import BaseModel
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
        None, description="The enterprise associated with this model."
    )
    people: Optional[List[PersonIO]] = Field(
        [], description="The set of people belonging to this model."
    )
    software_systems: Optional[List[SoftwareSystemIO]] = Field(
        [],
        alias="softwareSystems",
        description="The set of software systems belonging to this model.",
    )
    deployment_nodes: Optional[List[Any]] = Field(
        [],
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
        software_systems: Optional[Iterable[SoftwareSystem]] = (),
        # TODO
        deployment_nodes: Optional[Iterable[Any]] = (),
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
        return (
            element in self.people
            or element in self.software_systems
            or element in self.deployment_nodes
        )

    @classmethod
    def hydrate(cls, model_io: ModelIO) -> "Model":
        """"""
        return Model(
            enterprise=Enterprise.hydrate(model_io.enterprise)
            if model_io.enterprise is not None
            else None,
            people=map(Person.hydrate, model_io.people),
            software_systems=map(SoftwareSystem.hydrate, model_io.software_systems),
            # TODO: deployment nodes, relationships
        )

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
            ValueError: When a person with the same name already exists.

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

    # def add_deployment_node(self, deployment_node=None,
    #                         **kwargs) -> DeploymentNode:
    #     """Add a new software system to the model."""
    #     if deployment_node is None:
    #         deployment_node = DeploymentNode(**kwargs)
    #     if deployment_node.id in {d.id for d in self.deployment_nodes}:
    #         ValueError(
    #             f"A deployment node with the ID {deployment_node.id} already "
    #             f"exists in the model.")
    #     self.deployment_nodes.add(deployment_node)
    #     return deployment_node

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

    def get_relationships(self) -> Iterator[Relationship]:
        """Return an iterator over all relationships contained in this model."""
        return self._relationships_by_id.values()

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
            relationship.id in self._elements_by_id
            or relationship.id in self._relationships_by_id
        ):
            raise ValueError(f"The relationship {relationship} has an existing ID.")
        self._relationships_by_id[relationship.id] = relationship
        self._id_generator.found(relationship.id)
        return True
