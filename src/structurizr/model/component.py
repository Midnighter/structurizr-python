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


"""Provide a component model."""


from typing import TYPE_CHECKING, Iterable, List, Optional

from pydantic import Field

from .code_element import CodeElement
from .static_structure_element import StaticStructureElement, StaticStructureElementIO


if TYPE_CHECKING:
    from .container import Container


__all__ = ("Component", "ComponentIO")


class ComponentIO(StaticStructureElementIO):
    """
    Represent a component.

    A component is a grouping of related functionality behind an interface that
    runs inside a container.

    Attributes:
        id: The ID of this component in the model.
        name: The name of this component.
        description: A short description of this component.
        technology: The technology associated with this component
                    (e.g. Spring Bean).
        tags: A comma separated list of tags associated with this component.
        code: The set of code elements that make up this component.
        properties: A set of arbitrary name-value properties.
        relationships: The set of relationships from this component to
                       other elements.

    """

    technology: str = ""
    code_elements: List[CodeElement] = Field([], alias="codeElements")
    size: Optional[int] = None


class Component(StaticStructureElement):
    """
    Represent a component.

    A component is a grouping of related functionality behind an interface that
    runs inside a container.

    Attributes:
        id: The ID of this component in the model.
        name: The name of this component.
        description: A short description of this component.
        technology: The technology associated with this component
                    (e.g. Spring Bean).
        tags: A comma separated list of tags associated with this component.
        code: The set of code elements that make up this component.
        properties: A set of arbitrary name-value properties.
        relationships: The set of relationships from this component to
                       other elements.

    """

    def __init__(
        self,
        *,
        parent: Container,
        technology: str = "",
        code_elements: Iterable[CodeElement] = (),
        size: Optional[int] = None,
        **kwargs
    ):
        """
        Initialize a component model.

        Args:
            parent:
            technology:
            code_elements:
            size:
            **kwargs:

        """
        super().__init__(**kwargs)
        self.parent = parent
        self.technology = technology
        self.code_elements = set(code_elements)
        self.size = size
