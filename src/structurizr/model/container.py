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


"""Provide a container model."""


from typing import TYPE_CHECKING, Iterable, List, Optional

from .static_structure_element import StaticStructureElement, StaticStructureElementIO


if TYPE_CHECKING:
    from .component import Component
    from .software_system import SoftwareSystem


__all__ = ("Container", "ContainerIO")


class ContainerIO(StaticStructureElementIO):
    """
    Represent a container.

    A container is something that can execute code or host data.

    Attributes:
        id: The ID of this container in the model.
        name: The name of this container.
        description: A short description of this container.
        technology: The technology associated with this container
                    (e.g. Apache Tomcat).
        tags: A comma separated list of tags associated with this container.
        components: The set of components within this container.
        properties: A set of arbitrary name-value properties.
        relationships: The set of relationships from this container to
                       other elements.

    """

    technology: Optional[str] = ""
    components: List[Component] = set()


class Container(StaticStructureElement):
    """
    Represent a container.

    A container is something that can execute code or host data.

    Attributes:
        id: The ID of this container in the model.
        name: The name of this container.
        description: A short description of this container.
        technology: The technology associated with this container
                    (e.g. Apache Tomcat).
        tags: A comma separated list of tags associated with this container.
        components: The set of components within this container.
        properties: A set of arbitrary name-value properties.
        relationships: The set of relationships from this container to
                       other elements.

    """

    def __init__(
        self,
        *,
        parent: SoftwareSystem,
        technology: str = "",
        components: Iterable[Component] = (),
        **kwargs
    ):
        """
        Initialize a container model.

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
        self.components = set(components)
