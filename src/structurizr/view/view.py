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
from typing import Any, Optional, Set
from weakref import ref

from pydantic import BaseModel, Field

from ..model import SoftwareSystem
from .automatic_layout import AutomaticLayout
from .paper_size import PaperSize


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

    software_system: SoftwareSystem = Field(..., alias="softwareSystem")
    key: str
    description: str
    software_system_id: str = Field("", alias="softwareSystemId")
    paper_size: Optional[PaperSize] = Field(None, alias="paperSize")
    automatic_layout: Optional[AutomaticLayout] = Field(None, alias="automaticLayout")
    title: str = ""

    # TODO
    element_views: Set[Any] = Field((), alias="elementViews")
    # TODO
    relationship_views: Set[Any] = Field((), alias="relationshipViews")

    # TODO
    layout_merge_strategy: Optional[Any] = Field(None, alias="layoutMergeStrategy")

    def __init__(
        self, *, software_system: SoftwareSystem, key: str, description: str, **kwargs
    ):
        """Initialize a view with a 'private' view set."""
        super().__init__(
            software_system=software_system, key=key, description=description, **kwargs
        )
        # Using `object.__setattr__` is a workaround for setting a 'private' attribute
        # on a pydantic model. See https://github.com/samuelcolvin/pydantic/issues/655
        # for a longer discussion.
        object.__setattr__(self, "_viewset", lambda: None)

    def get_viewset(self):
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

    def set_viewset(self, view_set) -> None:
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
