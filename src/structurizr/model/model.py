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
from typing import Callable, Iterable, List, Optional, Set, ValuesView

from pydantic import Field

from ..abstract_base import AbstractBase
from ..base_model import BaseModel
from .deployment_node import DeploymentNode, DeploymentNodeIO
from .element import Element
from .enterprise import Enterprise, EnterpriseIO
from .implied_relationship_strategies import (
    ignore_implied_relationship_strategy as ignore_implied,
)
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
        default=(), description="The set of people belonging to this model."
    )
    software_systems: List[SoftwareSystemIO] = Field(
        default=(),
        alias="softwareSystems",
        description="The set of software systems belonging to this model.",
    )
    deployment_nodes: List[DeploymentNodeIO] = Field(
        default=(),
        alias="deploymentNodes",
        description="The set of top-level deployment nodes belonging to this model.",
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
        implied_relationship_strategy: Function used to create implied relationships.
            By default (or if set to `None`), no implied relationships will be created.
            See `implied_relationship_strategies.py` for more details.
    """

    def __init__(
        self,
        enterprise: Optional[Enterprise] = None,
        people: Optional[Iterable[Person]] = (),
        software_systems: Iterable[SoftwareSystem] = (),
        deployment_nodes: Iterable[DeploymentNode] = (),
        implied_relationship_strategy: Callable[[Relationship], None] = ignore_implied,
        **kwargs,
    ) -> None:
        """
        Initialize the model with its 'private' attributes.

        Args:
            **kwargs: Passed on to the parent constructor.

        """
        super().__init__(**kwargs)
        self.enterprise = enterprise
        self.implied_relationship_strategy = implied_relationship_strategy
        # TODO: simply iterate attributes
        self._elements_by_id = {}
        self._relationships_by_id = {}
        self._id_generator = SequentialIntegerIDGenerator()

    def __contains__(self, element: Element):
        """Return True if the element is in the model."""
        return element in self.get_elements()

    @property
    def software_systems(self) -> Set[SoftwareSystem]:
        """Return the software systems in the model."""
        return {
            element
            for element in self.get_elements()
            if isinstance(element, SoftwareSystem)
        }

    @property
    def people(self) -> Set[Person]:
        """Return the people in the model."""
        return {
            element for element in self.get_elements() if isinstance(element, Person)
        }

    @property
    def deployment_nodes(self) -> Set[DeploymentNode]:
        """Return the *top level* deployment nodes in the model."""
        return {
            element
            for element in self.get_elements()
            if isinstance(element, DeploymentNode) and element.parent is None
        }

    @classmethod
    def hydrate(cls, model_io: ModelIO) -> "Model":
        """Return a new model, hydrated from its IO."""
        model = cls(
            enterprise=Enterprise.hydrate(model_io.enterprise)
            if model_io.enterprise is not None
            else None,
            # TODO: relationships
        )

        for person_io in model_io.people:
            model += Person.hydrate(person_io)

        for software_system_io in model_io.software_systems:
            model += SoftwareSystem.hydrate(software_system_io)

        for deployment_node_io in model_io.deployment_nodes:
            model += DeploymentNode.hydrate(deployment_node_io, model=model)

        for element in model.get_elements():
            for relationship in element.relationships:
                relationship.source = model.get_element(relationship.source_id)
                relationship.destination = model.get_element(
                    relationship.destination_id
                )
                model.add_relationship(relationship, create_implied_relationships=False)

        return model

    def add_person(self, person=None, **kwargs) -> Person:
        """
        Add a new person to the model.

        Args:
            **kwargs: Provide keyword arguments for instantiating a `Person`.

        Returns:
            Person: New instance.

        Raises:
            ValueError: When a person with the same name already exists.

        See Also:
            Person

        """
        person = Person(**kwargs)
        self += person
        return person

    def add_software_system(self, name: str, **kwargs) -> SoftwareSystem:
        """
        Add a new software system to the model.

        Args:
            **kwargs: Provide keyword arguments for instantiating a `SoftwareSystem`
                (recommended).

        Returns:
            SoftwareSystem: New instance.

        Raises:
            ValueError: When a software system with the same name already exists.

        See Also:
            SoftwareSystem

        """
        software_system = SoftwareSystem(name=name, **kwargs)
        self += software_system
        return software_system

    def __iadd__(self, element: Element) -> "Model":
        """Add a newly constructed element to the model."""
        if element in self.get_elements():
            return self
        if isinstance(element, Person):
            if any(element.name == p.name for p in self.people):
                raise ValueError(
                    f"A person with the name '{element.name}' already exists in the "
                    f"model."
                )
        elif isinstance(element, SoftwareSystem):
            if any(element.name == s.name for s in self.software_systems):
                raise ValueError(
                    f"A software system with the name '{element.name}' already "
                    f"exists in the model."
                )
        elif isinstance(element, DeploymentNode):
            if any(
                element.name == d.name and element.environment == d.environment
                for d in self.deployment_nodes
            ):
                raise ValueError(
                    f"A deployment node with the name '{element.name}' already "
                    f"exists in environment '{element.environment}' of the model."
                )
        elif element.parent is None:
            raise ValueError(
                f"Element with name {element.name} has no parent.  Please ensure "
                f"you have added it to the parent element."
            )
        self._add_element(element)
        return self

    def add_deployment_node(
        self,
        name: str,
        description: str = "",
        technology: str = "",
        **kwargs,
    ) -> DeploymentNode:
        """
        Add a new deployment node to the model.

        Args:
            name(str): Name of the deployment node
            description(str): Optional description
            technology(str): Optional technologies
            **kwargs: additional keyword arguments for instantiating a `DeploymentNode`.

        Returns:
            DeploymentNode: The newly created DeploymentNode.

        Raises:
            ValueError: When a deployment node with the same name already exists.

        See Also:
            DeploymentNode

        """
        deployment_node = DeploymentNode(
            name=name, description=description, technology=technology, **kwargs
        )
        self += deployment_node
        return deployment_node

    def add_relationship(
        self,
        relationship: Relationship = None,
        *,
        create_implied_relationships: bool = True,
        **kwargs,
    ) -> Optional[Relationship]:
        """
        Add a relationship to the model.

        Args:
            relationship (Relationship, optional): Either provide a
                `Relationship` instance or
            **kwargs: Provide keyword arguments for instantiating a `Relationship`
                (recommended).
            create_implied_relationships (bool, optional): If `True` (default) then use
                the `implied_relationship_strategy` to create relationships implied by
                this one.  See `implied_relationship_strategies.py` for details.

        Returns:
            Relationship: Either the same or a new instance, depending on arguments.

        Raises:
            ValueError: When a relationship with the same ID already exists.

        See Also:
            Relationship

        """
        if relationship is None:
            relationship = Relationship(**kwargs)
        self._add_relationship(relationship, create_implied_relationships)
        return relationship

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
        """Return an iterator over all elements contained in this model."""
        return self._elements_by_id.values()

    def get_software_system_with_id(self, id: str) -> Optional[SoftwareSystem]:
        """Return the software system with a given ID."""
        result = self.get_element(id)
        if not isinstance(result, SoftwareSystem):
            return None
        return result

    def _add_element(self, element: Element) -> None:
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
        for child in element.child_elements:
            self += child

    def _add_relationship(
        self, relationship: Relationship, create_implied_relationships: bool
    ):
        if relationship in self.get_relationships():
            return
        if not relationship.id:
            relationship.id = self._id_generator.generate_id()
        elif relationship.id in self._elements_by_id:
            raise ValueError(
                f"{relationship} has the same ID as "
                f"{self._elements_by_id[relationship.id]}."
            )
        elif relationship.id in self._relationships_by_id:
            raise ValueError(
                f"{relationship} has the same ID as "
                f"{self._relationships_by_id[relationship.id]}."
            )
        relationship.source.add_relationship(
            relationship, create_implied_relationships=False
        )
        self._add_relationship_to_internal_structures(relationship)

        if create_implied_relationships:
            self.implied_relationship_strategy(relationship)

    def _add_relationship_to_internal_structures(self, relationship: Relationship):
        self._relationships_by_id[relationship.id] = relationship
        self._id_generator.found(relationship.id)
