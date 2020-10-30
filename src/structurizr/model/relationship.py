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


"""Provide the relationship model."""


from typing import TYPE_CHECKING, Optional

from pydantic import Field

from .interaction_style import InteractionStyle
from .model_item import ModelItem, ModelItemIO
from .tags import Tags


if TYPE_CHECKING:  # pragma: no cover
    from .element import Element

__all__ = ("Relationship", "RelationshipIO")


class RelationshipIO(ModelItemIO):
    """
    Represent a relationship between two elements.

    Attributes:
        id: The ID of this relationship in the model.
        description: A short description of this relationship.
        tags: A comma separated list of tags associated with this relationship.
        source_id: The ID of the source element.
        destination_id: The ID of the destination element.
        technology: The technology associated with this relationship
                    (e.g. HTTPS, JDBC, etc.).
        interaction_style: The interaction style (synchronous or asynchronous).

    """

    source_id: Optional[str] = Field("", alias="sourceId")
    destination_id: Optional[str] = Field("", alias="destinationId")
    description: Optional[str] = ""
    technology: Optional[str] = ""
    interaction_style: Optional[InteractionStyle] = Field(
        InteractionStyle.Synchronous, alias="interactionStyle"
    )
    linked_relationship_id: Optional[str] = Field("", alias="linkedRelationshipId")


class Relationship(ModelItem):
    """
    Represent a relationship between two elements.

    Attributes:
        id: The ID of this relationship in the model.
        description: A short description of this relationship.
        tags: A comma separated list of tags associated with this relationship.
        source_id: The ID of the source element.
        destination_id: The ID of the destination element.
        technology: The technology associated with this relationship
                    (e.g. HTTPS, JDBC, etc.).
        interaction_style: The interaction style (synchronous or asynchronous).

    """

    def __init__(
        self,
        *,
        source: Optional["Element"] = None,
        source_id: str = "",
        destination: Optional["Element"] = None,
        destination_id: str = "",
        description: str = "",
        technology: str = "",
        interaction_style: InteractionStyle = InteractionStyle.Synchronous,
        linked_relationship_id: str = "",
        **kwargs
    ) -> None:
        """Initialize a relationship between two elements."""
        super().__init__(**kwargs)
        self.source = source
        self._source_id = source_id
        self.destination = destination
        self._destination_id = destination_id
        self.description = description
        self.technology = technology
        self.linked_relationship_id = linked_relationship_id

        self.tags.add(Tags.RELATIONSHIP)
        self.tags.add(
            Tags.SYNCHRONOUS
            if interaction_style == InteractionStyle.Synchronous
            else Tags.ASYNCHRONOUS
        )

    @property
    def source_id(self) -> str:
        """Return the ID of the source element of this relationship."""
        if self.source is not None:
            return self.source.id

        return self._source_id

    @property
    def destination_id(self) -> str:
        """Return the ID of the destination element of this relationship."""
        if self.destination is not None:
            return self.destination.id

        return self._destination_id

    @property
    def interaction_style(self) -> str:
        """Return the interaction style of the relationship based on its tags."""
        return (
            InteractionStyle.Asynchronous
            if Tags.ASYNCHRONOUS in self.tags
            else InteractionStyle.Synchronous
        )

    @classmethod
    def hydrate(cls, relationship_io: RelationshipIO) -> "Relationship":
        """Hydrate a new instance of Relationship from its IO."""
        return cls(
            id=relationship_io.id,
            tags=relationship_io.tags,
            properties=relationship_io.properties,
            perspectives=relationship_io.perspectives,
            source_id=relationship_io.source_id,
            destination_id=relationship_io.destination_id,
            description=relationship_io.description,
            technology=relationship_io.technology,
            interaction_style=relationship_io.interaction_style,
        )
