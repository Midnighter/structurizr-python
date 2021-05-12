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


from typing import Any, Dict, Iterable, List, Optional, Set

from pydantic import Field

from ..model import Element, Model, Relationship, SoftwareSystem
from .abstract_view import AbstractView, AbstractViewIO
from .automatic_layout import AutomaticLayout, AutomaticLayoutIO
from .element_view import ElementView, ElementViewIO
from .paper_size import PaperSize
from .relationship_view import RelationshipView, RelationshipViewIO


__all__ = ("View", "ViewIO")


class ViewIO(AbstractViewIO):
    """
    Define a base class for non-filtered views.

    Views include static views, dynamic views and deployment views.
    """

    software_system_id: Optional[str] = Field(default=None, alias="softwareSystemId")
    paper_size: Optional[PaperSize] = Field(default=None, alias="paperSize")
    automatic_layout: Optional[AutomaticLayoutIO] = Field(
        default=None, alias="automaticLayout"
    )

    element_views: List[ElementViewIO] = Field(default=(), alias="elements")
    relationship_views: List[RelationshipViewIO] = Field(
        default=(), alias="relationships"
    )

    # TODO
    # layout_merge_strategy: Optional[Any] = Field(
    #     default=None, alias="layoutMergeStrategy"
    # )


class View(AbstractView):
    """
    Define a base class for non-filtered views.

    Views include static views, dynamic views and deployment views.

    """

    def __init__(
        self,
        *,
        software_system: Optional[SoftwareSystem] = None,
        paper_size: Optional[PaperSize] = None,
        automatic_layout: Optional[AutomaticLayout] = None,
        element_views: Optional[Iterable[ElementView]] = (),
        relationship_views: Optional[Iterable[RelationshipView]] = (),
        layout_merge_strategy: Optional[Any] = None,
        **kwargs,
    ):
        """Initialize a view with a 'private' view set."""
        super().__init__(**kwargs)
        self.software_system = software_system
        self.software_system_id = software_system.id if software_system else None
        self.paper_size = paper_size
        self.automatic_layout = automatic_layout
        self.element_views: Set[ElementView] = set(element_views)
        self._relationship_views: Set[RelationshipView] = set(relationship_views)

        # TODO
        self.layout_merge_strategy = layout_merge_strategy

    @classmethod
    def hydrate_arguments(cls, view_io: ViewIO) -> Dict:
        """Hydrate a ViewIO into the constructor arguments for View."""
        return {
            **super().hydrate_arguments(view_io),
            # TODO: should we add this here? probably not: "software_system"
            "paper_size": view_io.paper_size,
            "automatic_layout": AutomaticLayout.hydrate(view_io.automatic_layout)
            if view_io.automatic_layout
            else None,
            "element_views": map(ElementView.hydrate, view_io.element_views),
            "relationship_views": map(
                RelationshipView.hydrate, view_io.relationship_views
            ),
        }

    @property
    def model(self) -> Model:
        """Return the `Model` for this view."""
        return self.software_system.get_model()

    @property
    def relationship_views(self) -> Iterable[RelationshipView]:
        """Return the relationship views contained by this view."""
        return set(self._relationship_views)

    def _add_element(self, element: Element, add_relationships: bool) -> ElementView:
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
        view = self.find_element_view(element=element)
        if view is None:
            view = ElementView(element=element)
            self.element_views.add(view)
        if add_relationships:
            self._add_relationships(element)
        return view

    def _remove_element(self, element: Element) -> None:
        """
        Remove the given element from this view.

        Args:
            element (Element): The element to remove from the view.

        """
        if element not in self.model:
            raise RuntimeError(
                f"The element {element} does not exist in the model associated with "
                f"this view."
            )
        self.element_views.add(ElementView(id=element.id))
        for element_view in list(self.element_views):  # Copy as modifying as we go
            if element_view.id == element.id:
                self.element_views.remove(element_view)

        for relationship_view in list(self._relationship_views):
            if (
                relationship_view.relationship.source.id == element.id
                or relationship_view.relationship.destination.id == element.id
            ):
                self._relationship_views.remove(relationship_view)

    def _add_relationship(
        self,
        relationship: Relationship,
        *,
        description: Optional[str] = None,
        order: Optional[str] = None,
        response: bool = False,
    ) -> RelationshipView:
        """Add a single relationship to this view.

        Returns:
            The new (or existing) view if both the source and destination for the
            relationship are in this view, else `None`.
        """
        if self.is_element_in_view(relationship.source) and self.is_element_in_view(
            relationship.destination
        ):
            view = self.find_relationship_view(
                relationship=relationship, description=description, response=response
            )
            if not view:
                view = RelationshipView(
                    relationship=relationship,
                    description=description,
                    order=order,
                    response=response,
                )
                self._relationship_views.add(view)
            return view

    def _add_relationships(self, element: Element) -> None:
        """
        Add all relationships involving the given element to this view.

        Args:
            element (Element): The model element.

        """
        elements: Set[str] = {v.id for v in self.element_views}

        for relationship in element.get_efferent_relationships():
            if relationship.destination.id in elements:
                self._relationship_views.add(
                    RelationshipView(relationship=relationship)
                )

        for relationship in element.get_afferent_relationships():
            if relationship.source.id in elements:
                self._relationship_views.add(
                    RelationshipView(relationship=relationship)
                )

    def copy_layout_information_from(self, source: "View") -> None:
        """Copy the layout information from another view, including child views."""
        if not self.paper_size:
            self.paper_size = source.paper_size

        for source_element_view in source.element_views:
            destination_element_view = self.find_element_view(
                element=source_element_view.element
            )
            if destination_element_view:
                destination_element_view.copy_layout_information_from(
                    source_element_view
                )

        for source_relationship_view in source.relationship_views:
            destintion_relationship_view = self.find_relationship_view(
                relationship=source_relationship_view.relationship
            )
            if destintion_relationship_view:
                destintion_relationship_view.copy_layout_information_from(
                    source_relationship_view
                )

    def is_element_in_view(self, element: Element) -> bool:
        """Return True if the given element is in this view."""
        return self.find_element_view(element=element) is not None

    def find_element_view(
        self,
        *,
        element: Optional[Element] = None,
    ) -> Optional[ElementView]:
        """Find a child element view matching a given element."""
        return next(
            (view for view in self.element_views if view.element.id == element.id), None
        )

    def find_relationship_view(
        self,
        *,
        relationship: Optional[Relationship] = None,
        description: Optional[str] = None,
        response: Optional[bool] = None,
    ) -> Optional[RelationshipView]:
        """
        Find a child relationship view matching the supplied non-None arguments.

        Args:
            relationship: find a child view with matching relationship ID
            description:  find a child view with matching view description.  Note that
                          the view description is not always the same as that of the
                          relationship
            response:     find a child view with matching response indicator.
        """
        for view in self._relationship_views:
            rel = view.relationship
            if (
                (relationship is None or rel.id == relationship.id)
                and (
                    description is None
                    or view.description == description
                    or (view.description is None and rel.description == description)
                )
                and (response is None or view.response == response)
            ):
                return view

    def check_parent_and_children_not_in_view(self, element: Element) -> None:
        """Ensure that an element can't be added if parent or children are in view."""
        for view in self.element_views:
            if view.element in element.child_elements:
                raise ValueError(f"A child of {element.name} is already in this view.")
            if view.element is getattr(element, "parent", None):
                raise ValueError(
                    f"The parent of {element.name} is already in this view."
                )
