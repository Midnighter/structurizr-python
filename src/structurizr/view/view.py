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
from ..model import Element, SoftwareSystem
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
    software_system_id: str = Field(default="", alias="softwareSystemId")
    paper_size: Optional[PaperSize] = Field(default=None, alias="paperSize")
    automatic_layout: Optional[AutomaticLayoutIO] = Field(
        default=None, alias="automaticLayout"
    )
    title: str = ""

    element_views: List[ElementViewIO] = Field(default=(), alias="elementViews")
    relationship_views: List[RelationshipViewIO] = Field(
        default=(), alias="relationshipViews"
    )

    # TODO
    layout_merge_strategy: Optional[Any] = Field(
        default=None, alias="layoutMergeStrategy"
    )


class View(ViewSetRefMixin, AbstractBase, ABC):
    """
    Define an abstract base class for all views.

    Views include static views, dynamic views and deployment views.

    Attributes:

    """

    def __init__(
        self,
        *,
        software_system: Optional[SoftwareSystem] = None,
        key: str = None,
        description: str,
        paper_size: Optional[PaperSize] = None,
        automatic_layout: Optional[AutomaticLayout] = None,
        title: str = "",
        element_views: Optional[Iterable[ElementView]] = (),
        relationship_views: Optional[Iterable[RelationshipView]] = (),
        layout_merge_strategy: Optional[Any] = None,
        **kwargs,
    ):
        """Initialize a view with a 'private' view set."""
        super().__init__(**kwargs)
        self.software_system = software_system
        self.software_system_id = software_system.id if software_system else None
        self.key = key
        self.description = description
        self.paper_size = paper_size
        self.automatic_layout = automatic_layout
        self.title = title
        self.element_views = set(element_views)
        self.relationship_views = set(relationship_views)

        # TODO
        self.layout_merge_strategy = layout_merge_strategy

    @property
    def model(self):
        return self.software_system.get_model()

    def _add_element(self, element: Element, add_relationships: bool) -> None:
        """
        Add the given element to this view.

        Args:
            element (Element): The element to add to the view.
            add_relationships (bool): Whether to include all of the element's
                relationships with other elements.

        """
        if element not in self.model:
            raise RuntimeError(
                f"The element {element} does not exist in the model associated with "
                f"this view."
            )
        # TODO: finish x,y coordinates , x=0, y=0
        self.element_views.add(ElementView(id=element.id))
        if add_relationships:
            self._add_relationships(element)

    def _add_relationships(self, element: Element) -> None:
        """
        Add all relationships involving the given element to this view.

        Args:
            element (Element): The model element.

        """
        elements: Set[str] = {v.id for v in self.element_views}

        for relationship in element.get_efferent_relationships():
            if relationship.destination.id in elements:
                # TODO: finish relationshipview construction
                self.relationship_views.add(RelationshipView(id=relationship.id))

        for relationship in element.get_afferent_relationships():
            if relationship.source.id in elements:
                # TODO: finish relationshipview construction
                self.relationship_views.add(RelationshipView(id=relationship.id))
