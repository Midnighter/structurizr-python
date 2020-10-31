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


"""Provide a way to style a relationship."""


from typing import Optional

from pydantic import Field

from ..abstract_base import AbstractBase
from ..base_model import BaseModel
from .color import Color
from .routing import Routing


__all__ = ("RelationshipStyle", "RelationshipStyleIO")


class RelationshipStyleIO(BaseModel):
    """Represent a relationship's style."""

    tag: str
    thickness: Optional[int]
    width: Optional[int]
    color: Optional[Color]
    font_size: Optional[int] = Field(default=None, alias="fontSize")
    dashed: Optional[bool]
    routing: Optional[Routing]
    position: Optional[int]
    opacity: Optional[int]


class RelationshipStyle(AbstractBase):
    """Define an relationship's style."""

    START_OF_LINE = 0
    END_OF_LINE = 100

    def __init__(
        self,
        *,
        tag: str,
        thickness: Optional[int] = None,
        width: Optional[int] = None,
        color: Optional[str] = None,
        font_size: Optional[int] = None,
        dashed: Optional[bool] = None,
        routing: Optional[Routing] = None,
        position: Optional[int] = None,
        opacity: Optional[int] = None,
        **kwargs
    ) -> None:
        """Initialize a relationship style."""
        super().__init__(**kwargs)
        self.tag = tag
        self.thickness = thickness
        self.color = color
        self.font_size = font_size
        self.width = width
        self.dashed = dashed
        self.routing = routing
        self.position = position
        self.opacity = opacity

    @classmethod
    def hydrate(cls, relationship_style_io: RelationshipStyleIO) -> "RelationshipStyle":
        """Hydrate a new RelationshipStyle instance from its IO."""
        return cls(
            tag=relationship_style_io.tag,
            thickness=relationship_style_io.thickness,
            color=relationship_style_io.color,
            font_size=relationship_style_io.font_size,
            width=relationship_style_io.width,
            dashed=relationship_style_io.dashed,
            routing=relationship_style_io.routing,
            position=relationship_style_io.position,
            opacity=relationship_style_io.opacity,
        )
