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


"""Provide a superclass for all static structure model elements."""


from abc import ABC
from typing import TYPE_CHECKING, Optional

from .element import Element, ElementIO


if TYPE_CHECKING:
    from .relationship import Relationship


__all__ = ("StaticStructureElementIO", "StaticStructureElement")


class StaticStructureElementIO(ElementIO, ABC):
    """
    Define a superclass for all static structure model elements.

    This is the superclass for model elements that describe the static structure
    of a software system, namely Person, SoftwareSystem, Container and Component.

    """

    pass


class StaticStructureElement(Element, ABC):
    """
    Define a superclass for all static structure model elements.

    This is the superclass for model elements that describe the static structure
    of a software system, namely Person, SoftwareSystem, Container and Component.

    """

    def uses(
        self, destination: Element, description: str, **kwargs
    ) -> Optional["Relationship"]:
        return self.get_model().add_relationship(
            source=self, destination=destination, description=description, **kwargs
        )

    def delivers(
        self, destination: Element, description: str, **kwargs
    ) -> Optional["Relationship"]:
        return self.get_model().add_relationship(
            source=self, destination=destination, description=description, **kwargs
        )
