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

"""Provie a Dynamic View.

A dynamic diagram can be useful when you want to show how elements in a static model
collaborate at runtime to implement a user story, use case, feature, etc. This dynamic
diagram is based upon a UML communication diagram (previously known as a "UML
collaboration diagram"). It is similar to a UML sequence diagram although it allows a
free-form arrangement of diagram elements with numbered interactions to indicate
ordering.
"""

from typing import Optional, Union

from pydantic import Field

from ..mixin.model_ref_mixin import ModelRefMixin
from ..model.container import Container
from ..model.software_system import SoftwareSystem
from .view import View, ViewIO


__all__ = ("DynamicView", "DynamicViewIO")


class DynamicViewIO(ViewIO):
    """
    Represent the dynamic view from the C4 model.

    Attributes:
        element: The software system or container that this view is focused on.
    """

    element_id: Optional[str] = Field(default=None, alias="elementId")


class DynamicView(ModelRefMixin, View):
    """
    Represent the dynamic view from the C4 model.

    Attributes:
        element: The software system or container that this view is focused on.
    """

    def __init__(
        self,
        *,
        software_system: Optional[SoftwareSystem] = None,
        container: Optional[Container] = None,
        **kwargs
    ) -> None:
        """Initialize a DynamicView.

        Note that we explicitly don't pass the software_system to the superclass as we
        don't want it to appear in the JSON output (DynamicView uses elementId
        instead).
        """
        if software_system is not None and container is not None:
            raise ValueError("You cannot specify both software_system and container")
        super().__init__(**kwargs)
        self.element = software_system or container
        self.element_id = self.element.id if self.element else None

    @classmethod
    def hydrate(
        cls, io: DynamicViewIO, *, element: Optional[Union[SoftwareSystem, Container]]
    ) -> "DynamicView":
        """Hydrate a new DynamicView instance from its IO."""
        system = element if isinstance(element, SoftwareSystem) else None
        container = element if isinstance(element, Container) else None
        return cls(
            software_system=system,
            container=container,
            **cls.hydrate_arguments(io),
        )
