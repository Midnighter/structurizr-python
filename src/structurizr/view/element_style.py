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
from pydantic.color import Color

from ..abstract_base import AbstractBase
from ..base_model import BaseModel
from .border import Border
from .shape import Shape


__all__ = ("ElementStyle", "ElementStyleIO")


class ElementStyleIO(BaseModel):
    """
    Represent an element's style.

    Attributes:

    """

    tag: str
    width: Optional[int]
    height: Optional[int]
    background: Optional[Color]
    stroke: Optional[str]
    color: Optional[Color]
    font_size: Optional[int] = Field(None, alias="fontSize")
    shape: Optional[Shape]
    icon: Optional[str]
    border: Optional[Border]
    opacity: Optional[int]
    metadata: Optional[bool]
    description: Optional[str]


class ElementStyle(AbstractBase):
    """
    Represent an element's style.

    Attributes:

    """

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
        **kwargs
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
