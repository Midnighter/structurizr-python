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


"""Provide a wrapper for a collection of animation steps."""


from typing import Iterable, List

from ..abstract_base import AbstractBase
from ..base_model import BaseModel


__all__ = ("Animation", "AnimationIO")


class AnimationIO(BaseModel):
    """
    Define a wrapper for a collection of animation steps.

    Attributes:
        order:
        elements:
        relationships:

    """

    order: int
    elements: List[str] = []
    relationships: List[str] = []


class Animation(AbstractBase):
    """
    Define a wrapper for a collection of animation steps.

    Attributes:
        order: the order in which this animation step appears
        elements: the IDs of the elements to show in this step
        relationships: ths IDs of the relationships to show in this step

    """

    def __init__(
        self,
        *,
        order: int,
        elements: Iterable[str] = (),
        relationships: Iterable[str] = (),
        **kwargs
    ):
        """Initialize an animation."""
        super().__init__(**kwargs)
        self.order = order
        self.elements = set(elements)
        self.relationships = set(relationships)

    @classmethod
    def hydrate(cls, animation_io: AnimationIO) -> "Animation":
        """Hydrate a new Animation instance from its IO."""
        return cls(
            order=animation_io.order,
            elements=animation_io.elements,
            relationships=animation_io.relationships,
        )
