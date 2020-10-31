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


"""Provide a container for a relationship instance in a view."""


from typing import Any, Iterable, List, Optional

from pydantic import Field

from ..abstract_base import AbstractBase
from ..base_model import BaseModel
from ..model.relationship import Relationship
from .vertex import Vertex, VertexIO


__all__ = ("RelationshipView", "RelationshipViewIO")


START_OF_LINE = 0
END_OF_LINE = 100


class RelationshipViewIO(BaseModel):
    """Represent an instance of a relationship in a view."""

    id: Optional[str]
    order: Optional[str]
    description: Optional[str]
    vertices: List[VertexIO] = Field(default=())
    # TODO
    routing: Optional[Any]
    position: Optional[int]


class RelationshipView(AbstractBase):
    """Represent an instance of a relationship in a view."""

    def __init__(
        self,
        *,
        relationship: Optional[Relationship] = None,
        id: Optional[str] = None,
        description: Optional[str] = None,
        order: Optional[str] = None,
        vertices: Iterable[Vertex] = (),
        routing: Optional[Any] = None,
        position: Optional[int] = None,
        **kwargs,
    ) -> None:
        """Initialize a relationship view."""
        super().__init__(**kwargs)
        self.relationship = relationship
        self.id = relationship.id if relationship else id
        self.description = description
        self.order = order
        self.vertices = set(vertices)
        self.routing = routing
        self.position = position

    def __repr__(self) -> str:
        """Return repr(self)."""
        return (
            f"{type(self).__name__}("
            f"id={self.id}, "
            f"source_id={self.relationship.source_id}, "
            f"destination_id={self.relationship.destination_id}"
            f")"
        )

    @classmethod
    def hydrate(cls, relationship_view_io: RelationshipViewIO) -> "RelationshipView":
        """Hydrate a new RelationshipView instance from its IO."""
        return cls(
            id=relationship_view_io.id,
            description=relationship_view_io.description,
            order=relationship_view_io.order,
            vertices=map(Vertex.hydrate, relationship_view_io.vertices),
            routing=relationship_view_io.routing,
            position=relationship_view_io.position,
        )

    def copy_layout_information_from(self, source: "RelationshipView") -> None:
        """Copy the layout information from another RelationshipView."""
        self.vertices = source.vertices
        self.routing = source.routing
        self.position = source.position
