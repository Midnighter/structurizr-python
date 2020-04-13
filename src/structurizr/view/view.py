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
    software_system_id: str = Field("", alias="softwareSystemId")
    description: str = ""
    key: str
    paper_size: Optional[PaperSize] = Field(None, alias="paperSize")
    automatic_layout: Optional[AutomaticLayout] = Field(None, alias="automaticLayout")
    title: str

    element_views: Set[Any] = Field(..., alias="elementViews")
    relationship_views: Set[Any] = Field(..., alias="relationshipViews")

    layout_merge_strategy: Any = Field(..., alias="layoutMergeStrategy")

    def __init__(self, **kwargs):
        """Initialize a view with a 'private' view set."""
        super().__init__(**kwargs)
        # Using `object.__setattr__` is a workaround for setting a 'private' attribute
        # on a pydantic model. See https://github.com/samuelcolvin/pydantic/issues/655
        # for a longer discussion.
        object.__setattr__(self, "_viewset", lambda: None)

    def set_viewset(self, view_set) -> None:
        # Using `object.__setattr__` is a workaround for setting a 'private' attribute
        # on a pydantic model. See https://github.com/samuelcolvin/pydantic/issues/655
        # for a longer discussion.
        object.__setattr__(self, "_viewset", ref(view_set))
