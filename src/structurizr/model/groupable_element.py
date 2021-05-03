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


"""Provide a superclass for all elements that can be included in a group."""


from abc import ABC
from typing import Optional

from .element import Element, ElementIO


__all__ = ("GroupableElementIO", "GroupableElement")


class GroupableElementIO(ElementIO, ABC):
    """
    Define a superclass for all elements that can be included in a group.

    Attributes:
        group (str): The name of thegroup in which this element should be included, or
            None if no group.
    """

    group: Optional[str]


class GroupableElement(Element, ABC):
    """
    Define a superclass for all elements that can be included in a group.

    Attributes:
        group (str): The name of thegroup in which this element should be included, or
            None if no group.
    """

    def __init__(self, *, group: Optional[str] = None, **kwargs):
        """Initialise a GroupableElement."""
        super().__init__(**kwargs)
        group = group.strip() or None if group else None
        self.group = group

    @classmethod
    def hydrate_arguments(cls, io: GroupableElementIO) -> dict:
        """Hydrate an ElementIO into the constructor arguments for Element."""
        return {
            **super().hydrate_arguments(io),
            "group": io.group,
        }
