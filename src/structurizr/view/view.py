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


"""Provide a superclass for all views."""


from abc import ABC
from typing import TYPE_CHECKING, Any, Optional, Set
from weakref import ref

from pydantic import Field

from ..base_model import BaseModel
from ..model import Element, SoftwareSystem
from .automatic_layout import AutomaticLayout
from .element_view import ElementView
from .paper_size import PaperSize
from .relationship_view import RelationshipView


if TYPE_CHECKING:
    from .view_set import ViewSet


__all__ = ("View",)


class View(BaseModel, ABC):
    """
    Define an abstract base class for all views.

    Views include static views, dynamic views and deployment views.

    Attributes:

    """

    # Using slots for 'private' attributes prevents them from being included in model
    # serialization. See https://github.com/samuelcolvin/pydantic/issues/655
    # for a longer discussion.
    __slots__ = ("_viewset",)

    key: str
    description: str
    software_system: Optional[SoftwareSystem] = Field(None, alias="softwareSystem")
    software_system_id: str = Field("", alias="softwareSystemId")
    paper_size: Optional[PaperSize] = Field(None, alias="paperSize")
    automatic_layout: Optional[AutomaticLayout] = Field(None, alias="automaticLayout")
    title: str = ""

    element_views: Set[ElementView] = Field(set(), alias="elementViews")
    relationship_views: Set[RelationshipView] = Field(set(), alias="relationshipViews")

    # TODO
    layout_merge_strategy: Optional[Any] = Field(None, alias="layoutMergeStrategy")

    def __init__(
        self, *, software_system: SoftwareSystem, key: str, description: str, **kwargs
    ):
        """Initialize a view with a 'private' view set."""
        super().__init__(key=key, description=description, **kwargs)
        # This works around pydantic's feature of re-initializing children for
        # validation.
        # Assigning the system here maintains the original software system instance
        # as long as validation on assignment is turned off (the default).
        self.software_system = software_system
        # Using `object.__setattr__` is a workaround for setting a 'private' attribute
        # on a pydantic model. See https://github.com/samuelcolvin/pydantic/issues/655
        # for a longer discussion.
        object.__setattr__(self, "_viewset", lambda: None)

    def get_viewset(self) -> "ViewSet":
        """
        Retrieve the view set instance that contains this view.

        Returns:
            ViewSet: The view set that contains this view if any.

        Raises:
            RuntimeError: In case there exists no referenced view set.

        """
        viewset = self._viewset()
        if viewset is None:
            raise RuntimeError(
                f"You must add this {type(self).__name__} view to a ViewSet instance "
                f"first."
            )
        return viewset

    def set_viewset(self, view_set: "ViewSet") -> None:
        """
        Create a weak reference to a view set instance that contains this view.

        Warnings:
            This is an internal method and should not be directly called by users.

        Args:
            view_set (ViewSet):

        """
        # Using `object.__setattr__` is a workaround for setting a 'private' attribute
        # on a pydantic model. See https://github.com/samuelcolvin/pydantic/issues/655
        # for a longer discussion.
        object.__setattr__(self, "_viewset", ref(view_set))

    def _add_element(self, element: Element, add_relationships: bool) -> None:
        """
        Add the given element to this view.

        Args:
            element (Element): The element to add to the view.
            add_relationships (bool): Whether to include all of the element's
                relationships with other elements.

        """
        if element not in self.software_system.get_model():
            raise RuntimeError(
                f"The element {element} does not exist in the model associated with "
                f"this view."
            )
        self.element_views.add(ElementView(element=element))
        if add_relationships:
            self._add_relationships(element)

    def _add_relationships(self, element: Element) -> None:
        """
        Add all relationships involving the given element to this view.

        Args:
            element (Element): The model element.

        """
        elements: Set[Element] = {v.element for v in self.element_views}
        for relationship in element.get_efferent_relationships():
            if relationship.destination in elements:
                self.relationship_views.add(RelationshipView(relationship=relationship))
        for relationship in element.get_afferent_relationships():
            if relationship.source in elements:
                self.relationship_views.add(RelationshipView(relationship=relationship))
