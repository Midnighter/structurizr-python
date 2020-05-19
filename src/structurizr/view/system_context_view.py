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


"""Provide a system context view."""


from pydantic import Field

from .static_view import StaticView, StaticViewIO


__all__ = ("SystemContextView", "SystemContextViewIO")


class SystemContextViewIO(StaticViewIO):
    """
    Represent the system context view from the C4 model.

    Show how a software system fits into its environment, in terms of the users (people)
    and other software system dependencies.

    Attributes:
        enterprise_boundary_visible (bool):

    """

    enterprise_boundary_visible: bool = Field(True, alias="enterpriseBoundaryVisible")


class SystemContextView(StaticView):
    """
    Represent the system context view from the C4 model.

    Show how a software system fits into its environment, in terms of the users (people)
    and other software system dependencies.

    Attributes:
        enterprise_boundary_visible (bool):

    """

    def __init__(self, *, enterprise_boundary_visible: bool = True, **kwargs) -> None:
        """Initialize a system context view."""
        super().__init__(**kwargs)
        self.enterprise_boundary_visible = enterprise_boundary_visible

    def add_all_elements(self) -> None:
        """Add all software systems and all people to this view."""
        self.add_all_software_systems()
        self.add_all_people()

    @classmethod
    def hydrate(
        cls, system_context_view_io: SystemContextViewIO
    ) -> "SystemContextView":
        """"""
        return cls(
            enterprise_boundary_visible=system_context_view_io.enterprise_boundary_visible,
            description=system_context_view_io.description,
            key=system_context_view_io.key,
            software_system=system_context_view_io.software_system,
        )
