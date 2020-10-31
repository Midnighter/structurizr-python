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


"""Provide a way to style an element."""


from typing import Optional

from pydantic import Field

from ..abstract_base import AbstractBase
from ..base_model import BaseModel
from .border import Border
from .color import Color
from .shape import Shape


__all__ = ("ElementStyle", "ElementStyleIO")


class ElementStyleIO(BaseModel):
    """Represent an element's style."""

    tag: str
    width: Optional[int]
    height: Optional[int]
    background: Optional[Color]
    stroke: Optional[str]
    color: Optional[Color]
    font_size: Optional[int] = Field(default=None, alias="fontSize")
    shape: Optional[Shape]
    icon: Optional[str]
    border: Optional[Border]
    opacity: Optional[int]
    metadata: Optional[bool]
    description: Optional[str]


class ElementStyle(AbstractBase):
    """Represent an element's style."""

    DEFAULT_WIDTH = 450
    DEFAULT_HEIGHT = 300

    def __init__(
        self,
        *,
        tag: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        background: Optional[str] = None,
        stroke: Optional[str] = None,
        color: Optional[str] = None,
        font_size: Optional[int] = None,
        shape: Optional[Shape] = None,
        icon: Optional[str] = None,
        border: Optional[Border] = None,
        opacity: Optional[int] = None,
        metadata: Optional[bool] = None,
        description: Optional[str] = None,
        **kwargs,
    ) -> None:
        """Initialize an element style."""
        super().__init__(**kwargs)
        self.tag = tag
        self.width = width
        self.height = height
        self.background = background
        self.stroke = stroke
        self.color = color
        self.font_size = font_size
        self.shape = shape
        self.icon = icon
        self.border = border
        self.opacity = opacity
        self.metadata = metadata
        self.description = description

    def __repr__(self) -> str:
        """Return repr(self)."""
        return f"{type(self).__name__}(tag={self.tag})"

    @classmethod
    def hydrate(cls, element_style_io: ElementStyleIO) -> "ElementStyle":
        """Hydrate a new ElementStyle instance from its IO."""
        return cls(
            tag=element_style_io.tag,
            width=element_style_io.width,
            height=element_style_io.height,
            background=element_style_io.background,
            stroke=element_style_io.stroke,
            color=element_style_io.color,
            font_size=element_style_io.font_size,
            shape=element_style_io.shape,
            icon=element_style_io.icon,
            border=element_style_io.border,
            opacity=element_style_io.opacity,
            metadata=element_style_io.metadata,
            description=element_style_io.description,
        )
