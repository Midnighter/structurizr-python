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


"""Provide a system landscape view."""


from pydantic import Field

from ..mixin import ModelRefMixin
from ..model import Model
from .static_view import StaticView, StaticViewIO


__all__ = ("SystemLandscapeView", "SystemLandscapeViewIO")


class SystemLandscapeViewIO(StaticViewIO):
    """
    Represent a system landscape view that sits above the C4 model.

    This is the "big picture" view, showing the software systems and people in a given
    environment. The permitted elements in this view are software systems and people.

    Attributes:
        enterprise_boundary_visible (bool): Determines whether the enterprise boundary
        (to differentiate "internal" elements from "external" elements") should be
        visible on the resulting diagram.

    """

    enterprise_boundary_visible: bool = Field(True, alias="enterpriseBoundaryVisible")


class SystemLandscapeView(ModelRefMixin, StaticView):
    """
    Represent a system landscape view that sits above the C4 model.

    This is the "big picture" view, showing the software systems and people in a given
    environment. The permitted elements in this view are software systems and people.

    Attributes:
        enterprise_boundary_visible (bool):

    """

    def __init__(
        self, *, model: Model, enterprise_boundary_visible: bool = True, **kwargs
    ) -> None:
        """Initialize a system landscape view."""
        super().__init__(**kwargs)
        self.enterprise_boundary_visible = enterprise_boundary_visible
        self.set_model(model)

    def add_all_elements(self) -> None:
        """Add all software systems and all people to this view."""
        self.add_all_software_systems()
        self.add_all_people()

    @classmethod
    def hydrate(
        cls,
        system_landscape_view_io: SystemLandscapeViewIO,
        model: Model,
    ) -> "SystemLandscapeView":
        """Hydrate a new SystemLandscapeView instance from its IO."""
        return cls(
            **cls.hydrate_arguments(system_landscape_view_io),
            model=model,
            enterprise_boundary_visible=(
                system_landscape_view_io.enterprise_boundary_visible
            ),
        )
