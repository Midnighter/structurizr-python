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


"""
Implement various strategies for adding implied relationships to the model.

Implied relationship strategies are used to add relationships to parents when a
relationship is added to their children.  For example, assuming systems A and B with
child containers A1 and B1 respectively, then saying that A1 uses B1 implies that
A also uses B (and A uses B1 and A1 uses B).  Each strategy is represented as a
function that can be set on `Model.implied_relationship_strategy`, with the default
being to do nothing.
"""

from itertools import product
from typing import List

from .element import Element
from .relationship import Relationship
from .software_system import SoftwareSystem


def ignore_implied_relationship_strategy(relationship: Relationship):
    """Don't create any implied relationships."""
    pass


def create_implied_relationships_unless_any_exist(relationship: Relationship):
    """
    Create implied relationships unless there is any existing.

    This strategy creates implied relationships between all valid combinations of the
    parent elements, unless any relationship already exists between them.
    """
    source = relationship.source
    destination = relationship.destination
    ancestor_pairs = product(_get_ancestors(source), _get_ancestors(destination))
    for new_source, new_destination in ancestor_pairs:
        if _implied_relationship_is_allowed(new_source, new_destination):
            if not any(
                r.destination is new_destination
                for r in new_source.get_efferent_relationships()
            ):
                _clone_relationship(relationship, new_source, new_destination)


def create_implied_relationships_unless_same_exists(relationship: Relationship):
    """
    Create implied relationships unless there is one with the same description.

    This strategy creates implied relationships between all valid combinations of the
    parent elements, unless any relationship already exists between them which has the
    same description as the original.
    """
    source = relationship.source
    destination = relationship.destination
    ancestor_pairs = product(_get_ancestors(source), _get_ancestors(destination))
    for new_source, new_destination in ancestor_pairs:
        if _implied_relationship_is_allowed(new_source, new_destination):
            if not any(
                r.destination is new_destination
                and r.description == relationship.description
                for r in new_source.get_efferent_relationships()
            ):
                _clone_relationship(relationship, new_source, new_destination)


def _implied_relationship_is_allowed(source: Element, destination: Element):
    if source is destination:
        return False
    elif source in _get_ancestors(destination) or destination in _get_ancestors(source):
        return False
    return True


def _get_ancestors(element: Element) -> List[Element]:
    """Get the ancestors of an element, including itself."""
    result = []
    current = element
    while current is not None:
        result.append(current)
        current = None if isinstance(current, SoftwareSystem) else current.parent
    return result


def _clone_relationship(
    relationship: Relationship, new_source: Element, new_destination: Element
) -> Relationship:
    print(f"{new_source.name}->{new_destination.name}")
    return new_source.add_relationship(
        destination=new_destination,
        description=relationship.description,
        technology=relationship.technology,
        interaction_style=relationship.interaction_style,
        tags=relationship.tags,
        properties=relationship.properties,
        create_implied_relationships=False,
    )
