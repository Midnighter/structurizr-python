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


"""Provide a superclass for all model elements."""


from abc import ABC, abstractmethod
from typing import Iterable, Iterator, List, Optional

from pydantic import Field, HttpUrl

from ..mixin import ModelRefMixin
from .model_item import ModelItem, ModelItemIO
from .relationship import Relationship, RelationshipIO
from .tags import Tags


__all__ = ("ElementIO", "Element")


class ElementIO(ModelItemIO, ABC):
    """
    Define a superclass for all model elements.

    Attributes:
        name (str):
        description (str):
        url (pydantic.HttpUrl):

    """

    name: str = Field(...)
    description: str = Field(default="")
    url: Optional[HttpUrl] = Field(default=None)
    relationships: List[RelationshipIO] = Field(default=())


class Element(ModelRefMixin, ModelItem, ABC):
    """
    Define a superclass for all model elements.

    Attributes:
        name (str):
        description (str):
        url (pydantic.HttpUrl):

    """

    def __init__(
        self,
        *,
        name: str,
        description: str = "",
        url: Optional[str] = None,
        relationships: Optional[Iterable[Relationship]] = (),
        **kwargs,
    ) -> None:
        """Initialize an element with an empty 'private' model reference."""
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self.url = url
        # Note: relationships should always match get_efferent_relationships() - i.e.
        # outbound relationships only
        self.relationships: Iterable[Relationship] = set(relationships)

        self.tags.add(Tags.ELEMENT)

    def __repr__(self):
        """Return a string representation of this instance."""
        return f"{type(self).__name__}(id={self.id}, name={self.name})"

    @property
    @abstractmethod
    def child_elements(self) -> Iterable["Element"]:
        """Return the elements that are children of this one."""
        pass  # pragma: no cover

    def get_relationships(self) -> Iterator[Relationship]:
        """Return a Iterator over all relationships involving this element."""
        return (
            r
            for r in self.get_model().get_relationships()
            if self is r.source or self is r.destination
        )

    def get_efferent_relationships(self) -> Iterator[Relationship]:
        """Return a Iterator over all outgoing relationships involving this element."""
        return (r for r in self.get_model().get_relationships() if self is r.source)

    def get_afferent_relationships(self) -> Iterator[Relationship]:
        """Return a Iterator over all incoming relationships involving this element."""
        return (
            r for r in self.get_model().get_relationships() if self is r.destination
        )

    def add_relationship(
        self,
        relationship: Optional[Relationship] = None,
        *,
        create_implied_relationships: bool = True,
        **kwargs,
    ) -> Relationship:
        """Add a new relationship from this element to another.

        This can be used either to add a `Relationship` instance that has already been
        constructed, or by passing the arguments (e.g. description, destination) with
        which to construct a new one.  The relationship will automatically be
        registered with the element's model.
        """
        if relationship is None:
            relationship = Relationship(**kwargs)
        elif relationship in self.relationships:
            return relationship
        if relationship.source is None:
            relationship.source = self
        elif relationship.source is not self:
            raise ValueError(
                f"Cannot add relationship {relationship} to element {self} that is "
                f"not its source."
            )
        self.relationships.add(relationship)
        self.model.add_relationship(
            relationship, create_implied_relationships=create_implied_relationships
        )
        return relationship

    @classmethod
    def hydrate_arguments(cls, element_io: ElementIO) -> dict:
        """Hydrate an ElementIO into the constructor arguments for Element."""
        return {
            **super().hydrate_arguments(element_io),
            "name": element_io.name,
            "description": element_io.description,
            "url": element_io.url,
            "relationships": map(Relationship.hydrate, element_io.relationships),
        }
