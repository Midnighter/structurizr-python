# Copyright (c) 2020, Ilai Fallach.
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


"""Provide a vertex model."""
from typing import Optional

from pydantic import Field

from ..abstract_base import AbstractBase
from ..base_model import BaseModel


__all__ = ("Vertex", "VertexIO")


class VertexIO(BaseModel):
    """Define a wrapper for a vertex."""

    x: Optional[int] = Field(default=None)
    y: Optional[int] = Field(default=None)


class Vertex(AbstractBase):
    """Define a wrapper for a vertex."""

    def __init__(self, *, x: int, y: int, **kwargs) -> None:
        """Initialize an automatic layout."""
        super().__init__(**kwargs)
        self.x = x
        self.y = y

    @classmethod
    def hydrate(cls, vertex_io: VertexIO) -> "Vertex":
        """Hydrate a new Vertex instance from its IO."""
        return cls(x=vertex_io.x, y=vertex_io.y)
