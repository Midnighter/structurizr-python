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

    view_set: Any = Field(..., alias="viewSet")
