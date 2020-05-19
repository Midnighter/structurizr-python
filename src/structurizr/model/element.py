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


"""Provide a superclass for all model elements."""


from abc import ABC
from typing import TYPE_CHECKING, Iterator, Optional

from pydantic import Field, HttpUrl

from ..mixin import ModelRefMixin
from .model_item import ModelItem, ModelItemIO


if TYPE_CHECKING:
    from .relationship import Relationship


__all__ = ("ElementIO", "Element")


class ElementIO(ModelItemIO, ABC):
    """
    Define a superclass for all model elements.

    Attributes:
        name (str):
        description (str):
        url (pydantic.HttpUrl):

    """

    name: str = Field(...)
    description: str = Field("")
    url: Optional[HttpUrl] = Field(None)


class Element(ModelRefMixin, ModelItem, ABC):
    """
    Define a superclass for all model elements.

    Attributes:
        name (str):
        description (str):
        url (pydantic.HttpUrl):

    """

    def __init__(
        self, *, name: str, description: str = "", url: Optional[str] = None, **kwargs
    ) -> None:
        """Initialize an element with an empty 'private' model reference."""
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self.url = url

    def get_relationships(self) -> Iterator["Relationship"]:
        """Return a Iterator over all relationships involving this element."""
        return (
            r
            for r in self.get_model().get_relationships()
            if self is r.source or self is r.destination
        )

    def get_efferent_relationships(self) -> Iterator["Relationship"]:
        """Return a Iterator over all outgoing relationships involving this element."""
        return (r for r in self.get_model().get_relationships() if self is r.source)

    def get_afferent_relationships(self) -> Iterator["Relationship"]:
        """Return a Iterator over all incoming relationships involving this element."""
        return (
            r for r in self.get_model().get_relationships() if self is r.destination
        )
