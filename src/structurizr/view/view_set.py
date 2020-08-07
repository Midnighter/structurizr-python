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
from .container_view import ContainerView, ContainerViewIO
from .system_context_view import SystemContextView, SystemContextViewIO
from .system_landscape_view import SystemLandscapeView, SystemLandscapeViewIO


if TYPE_CHECKING:
    from ..model import Model


__all__ = ("ViewSet", "ViewSetIO")


class ViewSetIO(BaseModel):
    """
    Define a set of views onto a software architecture model.

    Views include static views, dynamic views and deployment views.

    Attributes:

    """

    system_landscape_views: List[SystemLandscapeViewIO] = Field(
        default=(), alias="systemLandscapeViews"
    )
    system_context_views: List[SystemContextViewIO] = Field(
        default=(), alias="systemContextViews"
    )
    configuration: Optional[ConfigurationIO] = None
    container_views: List[ContainerViewIO] = Field(default=(), alias="containerViews")

    # TODO:
    # component_views: List[ComponentView] = Field(set(), alias="componentViews")
    # dynamic_views: List[DynamicView] = Field(set(), alias="dynamicViews")
    # deployment_views: List[DeploymentView] = Field(set(), alias="deploymentViews")
    # filtered_views: List[FilteredView] = Field(set(), alias="filteredViews")


class ViewSet(ModelRefMixin, AbstractBase):
    """
    Define a set of views onto a software architecture model.

    Views include static views, dynamic views and deployment views.

    Attributes:

    """

    def __init__(
        self,
        *,
        model: Optional["Model"] = None,
        # TODO:
        # enterprise_context_views: Iterable[EnterpriseContextView] = (),
        system_landscape_views: Iterable[SystemLandscapeView] = (),
        system_context_views: Iterable[SystemContextView] = (),
        container_views: Iterable[ContainerView] = (),
        configuration: Optional[Configuration] = None,
        **kwargs
    ) -> None:
        """Initialize a view set."""
        super().__init__(**kwargs)
        # self.enterprise_context_views = set(enterprise_context_views)
        self.system_landscape_views = set(system_landscape_views)
        self.system_context_views = set(system_context_views)
        self.container_views = set(container_views)
        # TODO
        self.configuration = Configuration() if configuration is None else configuration
        self.set_model(model)

    def create_system_landscape_view(
        self, system_landscape_view: Optional[SystemLandscapeView] = None, **kwargs
    ) -> SystemLandscapeView:
        # TODO:
        # assertThatTheViewKeyIsSpecifiedAndUnique(key);
        if system_landscape_view is None:
            system_landscape_view = SystemLandscapeView(
                model=self.get_model(), **kwargs
            )
        system_landscape_view.set_viewset(self)
        self.system_landscape_views.add(system_landscape_view)
        return system_landscape_view

    def create_system_context_view(
        self, system_context_view: Optional[SystemContextView] = None, **kwargs
    ) -> SystemContextView:
        # TODO:
        # assertThatTheSoftwareSystemIsNotNull(softwareSystem);
        # assertThatTheViewKeyIsSpecifiedAndUnique(key);
        if system_context_view is None:
            system_context_view = SystemContextView(**kwargs)
        system_context_view.set_viewset(self)
        self.system_context_views.add(system_context_view)
        return system_context_view

    def create_container_view(
        self, container_view: Optional[ContainerView] = None, **kwargs
    ) -> ContainerView:
        # TODO:
        # assertThatTheSoftwareSystemIsNotNull(softwareSystem);
        # assertThatTheViewKeyIsSpecifiedAndUnique(key);
        if container_view is None:
            container_view = ContainerView(**kwargs)
        container_view.set_viewset(self)
        self.container_views.add(container_view)
        return container_view

    @classmethod
    def hydrate(cls, views: ViewSetIO, model: Optional["Model"] = None) -> "ViewSet":
        system_context_views = []
        for view_io in views.system_context_views:
            view = SystemContextView.hydrate(view_io)
            view.software_system_id = view_io.software_system_id
            view.software_system = model.get_software_system_with_id(
                view.software_system_id
            )
            system_context_views.append(view)

        return cls(
            # model=model,
            # TODO:
            # enterprise_context_views: Iterable[EnterpriseContextView] = (),
            system_landscape_views=map(
                SystemLandscapeView.hydrate, views.system_landscape_views
            ),
            system_context_views=system_context_views,
            container_views=map(ContainerView.hydrate, views.container_views),
            configuration=Configuration.hydrate(views.configuration),
        )
