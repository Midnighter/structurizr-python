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


"""Provide a superclass for all static views."""


from abc import ABC, abstractmethod
from typing import Dict, Iterable, List, Optional, Type, Union

from ..model import Container, Element, Person, SoftwareSystem
from .animation import Animation, AnimationIO
from .view import View, ViewIO


__all__ = ("StaticView", "StaticViewIO")


class StaticViewIO(ViewIO, ABC):
    """
    Define an abstract base class for all static views.

    Static views include system landscape, system context, container and component
    views.

    Attributes:
        animations:

    """

    animations: List[AnimationIO] = []


class StaticView(View, ABC):
    """
    Define an abstract base class for all static views.

    Static views include system landscape, system context, container and component
    views.

    Attributes:
        animations:

    """

    def __init__(
        self, *, animations: Optional[Iterable[Animation]] = None, **kwargs
    ) -> None:
        """Initialize a static view."""
        super().__init__(**kwargs)
        self.animations = [] if animations is None else list(animations)

    @classmethod
    def hydrate_arguments(cls, static_view_io: StaticViewIO) -> Dict:
        """Hydrate a StaticViewIO into the constructor arguments for StaticView."""
        return {
            **super().hydrate_arguments(static_view_io),
            "animations": map(Animation.hydrate, static_view_io.animations),
        }

    @abstractmethod
    def add_all_elements(self) -> None:
        """Add all permitted elements from a model to this view."""
        pass  # pragma: no cover

    def add(
        self,
        element: Union[Person, SoftwareSystem],
        add_relationships: bool = True,
    ) -> None:
        """
        Add the given person or software system to this view.

        Args:
            element (Person or SoftwareSystem): The element to add to this view.
            add_relationships (bool, optional): Whether to include all of the static
                element's relationships with other elements (default `True`).

        """
        self._add_element(element, add_relationships)

    def add_all_people(self) -> None:
        """Add all people in the model to this view."""
        for person in self.model.people:
            self.add(person)

    def add_all_software_systems(self) -> None:
        """Add all software systems in the model to this view."""
        for system in self.model.software_systems:
            self.add(system)

    def add_nearest_neighbours(
        self,
        element: Element,
        element_type: Union[Type[Person], Type[SoftwareSystem], Type[Container]],
    ) -> None:
        """Add all permitted elements from a model to this view."""
        self._add_element(element, False)

        # TODO(ilaif): @midnighter - Should we move to @property instead
        #  of get_X()? More pythonic.
        # (midnighter): Probably yes.
        for relationship in self.model.get_relationships():
            if relationship.source == element and isinstance(
                relationship.destination, element_type
            ):
                self._add_element(relationship.destination, add_relationships=True)

            if relationship.destination == element and isinstance(
                relationship.source, element_type
            ):
                self._add_element(relationship.source, add_relationships=True)
