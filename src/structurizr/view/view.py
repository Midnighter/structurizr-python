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
from typing import Any, Iterable, List, Optional, Set

from pydantic import Field

from ..abstract_base import AbstractBase
from ..base_model import BaseModel
from ..mixin import ViewSetRefMixin
from ..model import Element, SoftwareSystem, SoftwareSystemIO
from .automatic_layout import AutomaticLayout, AutomaticLayoutIO
from .element_view import ElementView, ElementViewIO
from .paper_size import PaperSize
from .relationship_view import RelationshipView, RelationshipViewIO


__all__ = ("View", "ViewIO")


class ViewIO(BaseModel, ABC):
    """
    Define an abstract base class for all views.

    Views include static views, dynamic views and deployment views.

    Attributes:

    """

    key: str
    description: str
    software_system: Optional[SoftwareSystemIO] = Field(None, alias="softwareSystem")
    software_system_id: str = Field("", alias="softwareSystemId")
    paper_size: Optional[PaperSize] = Field(None, alias="paperSize")
    automatic_layout: Optional[AutomaticLayoutIO] = Field(None, alias="automaticLayout")
    title: str = ""

    element_views: List[ElementViewIO] = Field([], alias="elementViews")
    relationship_views: List[RelationshipViewIO] = Field([], alias="relationshipViews")

    # TODO
    layout_merge_strategy: Optional[Any] = Field(None, alias="layoutMergeStrategy")


class View(ViewSetRefMixin, AbstractBase, ABC):
    """
    Define an abstract base class for all views.

    Views include static views, dynamic views and deployment views.

    Attributes:

    """

    def __init__(
        self,
        *,
        software_system: SoftwareSystem,
        key: str,
        description: str,
        paper_size: Optional[PaperSize] = None,
        automatic_layout: Optional[AutomaticLayout] = None,
        title: str = "",
        element_views: Optional[Iterable[ElementView]] = None,
        relationship_views: Optional[Iterable[RelationshipView]] = None,
        layout_merge_strategy: Optional[Any] = None,
        **kwargs,
    ):
        """Initialize a view with a 'private' view set."""
        super().__init__(**kwargs)
        self.software_system = software_system
        self.key = key
        self.description = description
        self.paper_size = paper_size
        self.automatic_layout = automatic_layout
        self.title = title
        self.element_views = set() if element_views is None else set(element_views)
        self.relationship_views = (
            set() if relationship_views is None else set(relationship_views)
        )
        # TODO
        self.layout_merge_strategy = layout_merge_strategy

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
