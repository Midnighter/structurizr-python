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

"""Provide a dynamic view."""

from contextlib import contextmanager
from operator import attrgetter
from typing import Iterable, Optional, Tuple, Union

from pydantic import Field

from ..mixin.model_ref_mixin import ModelRefMixin
from ..model import Component, Container, Element, Person, Relationship, SoftwareSystem
from ..model.static_structure_element import StaticStructureElement
from .relationship_view import RelationshipView
from .sequence_number import SequenceNumber
from .view import View, ViewIO


__all__ = ("DynamicView", "DynamicViewIO")


class DynamicViewIO(ViewIO):
    """
    Represent a dynamic view on a C4 model.

    Attributes:
        element: The software system or container that this view is focused on.
    """

    element_id: Optional[str] = Field(default=None, alias="elementId")


class DynamicView(ModelRefMixin, View):
    """
    Represent a dynamic view on a C4 model.

    A dynamic diagram can be useful when you want to show how elements in a static
    model collaborate at runtime to implement a user story, use case, feature, etc.
    This dynamic diagram is based upon a UML communication diagram (previously known
    as a "UML collaboration diagram"). It is similar to a UML sequence diagram
    although it allows a free-form arrangement of diagram elements with numbered
    interactions to indicate ordering.

    Attributes:
        element: The software system or container that this view is focused on.
    """

    def __init__(
        self,
        *,
        element: Optional[Union[Container, SoftwareSystem]] = None,
        **kwargs,
    ) -> None:
        """Initialize a DynamicView.

        Note that we explicitly don't pass the software_system to the superclass as we
        don't want it to appear in the JSON output (DynamicView uses elementId
        instead).
        """
        if "software_system" in kwargs:
            raise ValueError(
                "Software system must be specified through the 'element' argument for "
                "DynamicViews"
            )
        super().__init__(**kwargs)
        self.element = element
        self.element_id = self.element.id if self.element else None
        self.sequence_number = SequenceNumber()

    def add(
        self,
        source: Element,
        destination: Element,
        description: Optional[str] = None,
        *,
        technology: Optional[str] = None,
    ) -> RelationshipView:
        """Add a relationship to this DynamicView.

        This will search for a relationship in the model from the source to the
        destination with matching technology (if specified).  It will also look for
        situations where this interaction is a "response" in that it goes in the
        opposite direction to the relationship in the model.  If a description is
        provided then this will be used in the view in preference to the description
        on the relationship.

        Examples:
            Example of a request/response, assuming a single relationship in the model:

                dynamic_view.add(container1, container2, "Requests data from")
                dynamic_view.add(container2, container1, "Sends response back to")

        """
        self.check_element_can_be_added(source)
        self.check_element_can_be_added(destination)
        relationship, response = self._find_relationship(
            source, description, destination, technology
        )
        if relationship is None:
            if technology:
                raise ValueError(
                    f"A relationship between {source.name} and "
                    f"{destination.name} with technology "
                    f"'{technology}' does not exist in the model."
                )
            else:
                raise ValueError(
                    f"A relationship between {source.name} and "
                    f"{destination.name} does not exist in "
                    "the model."
                )
        self._add_element(source, False)
        self._add_element(destination, False)
        return self._add_relationship(
            relationship,
            description=description or relationship.description,
            order=self.sequence_number.get_next(),
            response=response,
        )

    @contextmanager
    def subsequence(self):
        """
        Start a context-managed subsequence.

        Subsequences allow nested interaction sequences, showing "child" calls through
        numbering 1.1, 1.2, etc.  Subsequences can themselves be nested.

        Examples:
        As an example, assume four Components, A-D.  A makes a service request to B,
        which in turn calls both C then D to process the request before returning the
        results back to A.  This can be shown using:

            dynamic_view.add(a, b, "Sends service request to")
            with dynamic_view.subsequence():
                dynamic_view.add(b, c, "Makes subcall to")
                dynamic_view.add(b, d, "Makes second subcall to")
            dynamic_view.add(b, a, "Sends results back to")

        This would result in four interactions shown, with orders "1", "1.1", "1.2"
        and "2" respectively.
        """
        try:
            self.sequence_number.start_subsequence()
            yield self
        finally:
            self.sequence_number.end_subsequence()

    @contextmanager
    def parallel_sequence(self, *, continue_numbering: bool = False):
        r"""
        Start a context-managed parallel sequence.

        Args:
            continue_numbering: Whether to continue the main sequence number
                from where the parallel sequence ended when its context is
                ended (`True`) or to reset the main sequence to where it began
                (`False`). The latter is usually done so that you can start a
                new parallel sequence.

        Examples:
        Parallel sequences allow for multiple parallel flows to share the same
        sequence numbers, for example,

                   /-> C -\
          A -> B -{        }-> E -> F
                   \-> D -/

        could happen concurrently but you want both B->C and B->D to get order
        number 2, and C->E and D->E to get order number 3.  To achieve this,
        you would do:

            dynamic_view.add(a, b)      # Will be order "1"
            with dynamic_view.parallel_sequence():
                dynamic_view.add(b, c)  # "2"
                dynamic_view.add(c, e)  # "3"
            with dynamic_view.parallel_sequence(continue_numbering=True):
                dynamic_view.add(b, d)  # "2" again
                dynamic_view.add(d, e)  # "3"
            dynamiic_view.add(e, f)     # "4"
        """
        try:
            self.sequence_number.start_parallel_sequence()
            yield self
        finally:
            self.sequence_number.end_parallel_sequence(continue_numbering)

    @property
    def relationship_views(self) -> Iterable[RelationshipView]:
        """Return the relationship views in order of their sequence number.

        Sorting uses "version number" style ordering, so 1 < 1.1 < 2 < 10.
        """
        return sorted(self._relationship_views, key=attrgetter("order"))

    def check_element_can_be_added(self, element: Element) -> None:
        """Make sure that the element is valid to be added to this view."""
        if not isinstance(element, StaticStructureElement):
            raise ValueError(
                "Only people, software systems, containers and components can be "
                "added to dynamic views."
            )
        if isinstance(element, Person):
            return

        if isinstance(self.element, SoftwareSystem):
            # System scope, so only systems and containers are allowed
            if element is self.element:
                raise ValueError(
                    f"{element.name} is already the scope of this view and cannot be "
                    "added to it."
                )
            if isinstance(element, Component):
                raise ValueError(
                    "Components can't be added to a dynamic view when the scope is a "
                    "software system"
                )
            self.check_parent_and_children_not_in_view(element)
        elif isinstance(self.element, Container):
            # Container scope
            if element is self.element or element is self.element.parent:
                raise ValueError(
                    f"{element.name} is already the scope of this view and cannot be "
                    "added to it."
                )
            self.check_parent_and_children_not_in_view(element)
        else:
            # No scope - only systems can be added
            assert self.element is None
            if not isinstance(element, SoftwareSystem):
                raise ValueError(
                    "Only people and software systems can be added to this dynamic "
                    "view."
                )

    def _find_relationship(
        self,
        source: Element,
        description: str,
        destination: Element,
        technology: Optional[str],
    ) -> Tuple[Optional[Relationship], bool]:
        """Return the best matching relationship and whether it is a response."""

        # First preference is exactly matching description
        rel = next(
            (
                rel
                for rel in source.get_efferent_relationships()
                if rel.destination is destination
                and (rel.description == description or not description)
                and (rel.technology == technology or technology is None)
            ),
            None,
        )
        if rel:
            return rel, False

        # Next preference is non-matching description
        rel = next(
            (
                rel
                for rel in source.get_efferent_relationships()
                if rel.destination is destination
                and (rel.technology == technology or technology is None)
            ),
            None,
        )
        if rel:
            return rel, False

        # Finally look for "response" to relationship in the opposite direction but
        # ignore descriptions
        rel = next(
            (
                rel
                for rel in source.get_afferent_relationships()
                if rel.source is destination
                and (rel.technology == technology or technology is None)
            ),
            None,
        )
        return rel, True

    @classmethod
    def hydrate(
        cls, io: DynamicViewIO, *, element: Optional[Union[SoftwareSystem, Container]]
    ) -> "DynamicView":
        """Hydrate a new DynamicView instance from its IO."""
        return cls(
            element=element,
            **cls.hydrate_arguments(io),
        )
