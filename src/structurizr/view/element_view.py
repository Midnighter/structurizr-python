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


"""Provide a container for an element instance in a view."""


from typing import Optional

from ..abstract_base import AbstractBase
from ..base_model import BaseModel
from ..model import Element, ElementIO


__all__ = ("ElementView", "ElementViewIO")


class ElementViewIO(BaseModel):
    """
    Represent an instance of an element in a view.

    Attributes:

    """

    element: ElementIO
    id: Optional[str]
    x: Optional[int]
    y: Optional[int]


class ElementView(AbstractBase):
    """
    Represent an instance of an element in a view.

    Attributes:

    """

    def __init__(
        self,
        *,
        element: Element,
        x: Optional[int] = None,
        y: Optional[int] = None,
        id: str = "",
        **kwargs
    ) -> None:
        """Initialize an element view."""
        super().__init__(**kwargs)
        self.element = element
        self.id = id
        self.x = x
        self.y = y
