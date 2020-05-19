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


"""Provide a collection of styles."""


from typing import Iterable, List, Optional, Union

from ..abstract_base import AbstractBase
from ..base_model import BaseModel
from .element_style import ElementStyle, ElementStyleIO
from .relationship_style import RelationshipStyle, RelationshipStyleIO


__all__ = ("Styles", "StylesIO")


class StylesIO(BaseModel):
    """
    Represent a collection of styles.

    Attributes:

    """

    elements: Optional[List[ElementStyleIO]]
    relationships: Optional[List[RelationshipStyleIO]]


class Styles(AbstractBase):
    """
    Represent a collection of styles.

    Attributes:

    """

    def __init__(
        self,
        *,
        elements: Iterable[ElementStyle] = (),
        relationships: Iterable[RelationshipStyle] = (),
        **kwargs,
    ) -> None:
        """Initialize the element and relationship styles."""
        super().__init__(**kwargs)
        self.elements = list(elements)
        self.relationships = list(relationships)

    def add(self, style: Union[ElementStyle, RelationshipStyle]) -> None:
        """"""
        if isinstance(style, ElementStyle):
            self.elements.append(style)
        elif isinstance(style, RelationshipStyle):
            self.relationships.append(style)
        else:
            raise ValueError(
                f"Can't add unknown type of style '{type(style).__name__}'."
            )

    def add_element_style(self, **kwargs) -> None:
        """"""
        self.elements.append(ElementStyle(**kwargs))

    def clear_element_styles(self) -> None:
        """"""
        self.elements.clear()

    def add_relationship_style(self, **kwargs) -> None:
        """"""
        self.relationships.append(RelationshipStyle(**kwargs))

    def clear_relationships_styles(self) -> None:
        """"""
        self.relationships.clear()
