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


from typing import Set
from weakref import ref

from pydantic import BaseModel, Field

from ..model import AbstractModel, SoftwareSystem
from .system_context_view import SystemContextView


__all__ = ("ViewSet",)


class ViewSet(BaseModel):
    """
    Define a set of views onto a software architecture model.

    Views include static views, dynamic views and deployment views.

    Attributes:

    """

    # Using slots for 'private' attributes prevents them from being included in model
    # serialization. See https://github.com/samuelcolvin/pydantic/issues/655
    # for a longer discussion.
    __slots__ = ("_model",)

    # system_landscape_views: Set[SystemLandscapeView] = Field(
    #     (), alias="systemLandscapeViews"
    # )
    system_context_views: Set[SystemContextView] = Field((), alias="systemContextView")
    # container_views: Set[ContainerView] = Field((), alias="containerViews")
    # component_views: Set[ComponentView] = Field((), alias="componentViews")
    # dynamic_views: Set[DynamicView] = Field((), alias="dynamicViews")
    # deployment_views: Set[DeploymentView] = Field((), alias="deploymentViews")
    # filtered_views: Set[FilteredView] = Field((), alias="filteredViews")
    # configuration: Configuration = Field(None)

    def __init__(self, *, model: AbstractModel, **kwargs):
        """Initialize a view set with a 'private' model."""
        super().__init__(**kwargs)
        # Using `object.__setattr__` is a workaround for setting a 'private' attribute
        # on a pydantic model. See https://github.com/samuelcolvin/pydantic/issues/655
        # for a longer discussion.
        object.__setattr__(self, "_model", ref(model))
        # self.configuration = Configuration()

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
