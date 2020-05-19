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


"""Provide a set of views onto a software architecture model."""


from typing import TYPE_CHECKING, Iterable, List, Optional

from pydantic import Field

from ..abstract_base import AbstractBase
from ..base_model import BaseModel
from ..mixin import ModelRefMixin
from .configuration import Configuration, ConfigurationIO
from .system_context_view import SystemContextView, SystemContextViewIO


if TYPE_CHECKING:
    from ..model import Model


__all__ = ("ViewSet", "ViewSetIO")


class ViewSetIO(BaseModel):
    """
    Define a set of views onto a software architecture model.

    Views include static views, dynamic views and deployment views.

    Attributes:

    """

    # TODO
    # system_landscape_views: Set[SystemLandscapeView] = Field(
    #     set(), alias="systemLandscapeViews"
    # )
    system_context_views: List[SystemContextViewIO] = Field(
        [], alias="systemContextView"
    )
    configuration: Optional[ConfigurationIO]
    # TODO
    # container_views: Set[ContainerView] = Field(set(), alias="containerViews")
    # component_views: Set[ComponentView] = Field(set(), alias="componentViews")
    # dynamic_views: Set[DynamicView] = Field(set(), alias="dynamicViews")
    # deployment_views: Set[DeploymentView] = Field(set(), alias="deploymentViews")
    # filtered_views: Set[FilteredView] = Field(set(), alias="filteredViews")


class ViewSet(ModelRefMixin, AbstractBase):
    """
    Define a set of views onto a software architecture model.

    Views include static views, dynamic views and deployment views.

    Attributes:

    """

    def __init__(
        self,
        *,
        model: "Model",
        system_context_views: Iterable[SystemContextView] = (),
        configuration: Optional[Configuration] = None,
        **kwargs
    ) -> None:
        """Initialize a view set."""
        super().__init__(**kwargs)
        self.system_context_views = set(system_context_views)
        # TODO
        self.configuration = Configuration() if configuration is None else configuration
        self.set_model(model)

    def create_system_context_view(
        self, system_context_view: SystemContextView = None, **kwargs
    ) -> SystemContextView:
        # assertThatTheSoftwareSystemIsNotNull(softwareSystem);
        # assertThatTheViewKeyIsSpecifiedAndUnique(key);
        if system_context_view is None:
            system_context_view = SystemContextView(**kwargs)
        system_context_view.set_viewset(self)
        self.system_context_views.add(system_context_view)
        return system_context_view
