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


from typing import TYPE_CHECKING, Iterable, List, Optional, Set

from pydantic import Field

from ..abstract_base import AbstractBase
from ..base_model import BaseModel
from ..mixin import ModelRefMixin
from .component_view import ComponentView, ComponentViewIO
from .configuration import Configuration, ConfigurationIO
from .container_view import ContainerView, ContainerViewIO
from .deployment_view import DeploymentView, DeploymentViewIO
from .system_context_view import SystemContextView, SystemContextViewIO
from .system_landscape_view import SystemLandscapeView, SystemLandscapeViewIO
from .view import View


if TYPE_CHECKING:
    from ..model import Model


__all__ = ("ViewSet", "ViewSetIO")


class ViewSetIO(BaseModel):
    """
    Define a set of views onto a software architecture model.

    Views include static views, dynamic views and deployment views.
    """

    system_landscape_views: List[SystemLandscapeViewIO] = Field(
        default=(), alias="systemLandscapeViews"
    )
    system_context_views: List[SystemContextViewIO] = Field(
        default=(), alias="systemContextViews"
    )
    configuration: ConfigurationIO
    container_views: List[ContainerViewIO] = Field(default=(), alias="containerViews")
    component_views: List[ComponentViewIO] = Field(default=(), alias="componentViews")
    deployment_views: List[DeploymentViewIO] = Field(
        default=(), alias="deploymentViews"
    )

    # TODO:
    # dynamic_views: List[DynamicView] = Field(set(), alias="dynamicViews")
    # filtered_views: List[FilteredView] = Field(set(), alias="filteredViews")


class ViewSet(ModelRefMixin, AbstractBase):
    """
    Define a set of views onto a software architecture model.

    Views include static views, dynamic views and deployment views.
    """

    def __init__(
        self,
        *,
        model: Optional["Model"],
        # TODO:
        # enterprise_context_views: Iterable[EnterpriseContextView] = (),
        system_landscape_views: Iterable[SystemLandscapeView] = (),
        system_context_views: Iterable[SystemContextView] = (),
        container_views: Iterable[ContainerView] = (),
        component_views: Iterable[ComponentView] = (),
        deployment_views: Iterable[DeploymentView] = (),
        configuration: Optional[Configuration] = None,
        **kwargs
    ) -> None:
        """Initialize a view set."""
        super().__init__(**kwargs)
        # self.enterprise_context_views = set(enterprise_context_views)
        self.system_landscape_views: Set[SystemLandscapeView] = set(
            system_landscape_views
        )
        self.system_context_views: Set[SystemContextView] = set(system_context_views)
        self.container_views: Set[ContainerView] = set(container_views)
        self.component_views: Set[ComponentView] = set(component_views)
        self.deployment_views: Set[DeploymentView] = set(deployment_views)
        self.configuration = Configuration() if configuration is None else configuration
        self.set_model(model)

    @classmethod
    def hydrate(cls, views: ViewSetIO, model: "Model") -> "ViewSet":
        """Hydrate a new ViewSet instance from its IO."""
        system_landscape_views = []
        for view_io in views.system_landscape_views:
            view = SystemLandscapeView.hydrate(view_io, model=model)
            cls._hydrate_view(view, model=model)
            system_landscape_views.append(view)

        system_context_views = []
        for view_io in views.system_context_views:
            software_system = model.get_software_system_with_id(
                view_io.software_system_id
            )
            view = SystemContextView.hydrate(view_io, software_system=software_system)
            cls._hydrate_view(view, model=model)
            system_context_views.append(view)

        container_views = []
        for view_io in views.container_views:
            software_system = model.get_software_system_with_id(
                id=view_io.software_system_id,
            )
            view = ContainerView.hydrate(view_io, software_system=software_system)
            cls._hydrate_view(view, model=model)
            container_views.append(view)

        component_views = []
        for view_io in views.component_views:
            container = model.get_element(view_io.container_id)
            view = ComponentView.hydrate(view_io, container=container)
            cls._hydrate_view(view, model=model)
            component_views.append(view)

        deployment_views = []
        for view_io in views.deployment_views:
            view = DeploymentView.hydrate(view_io)
            cls._hydrate_view(view, model=model)
            deployment_views.append(view)

        return cls(
            model=model,
            # TODO:
            # enterprise_context_views: Iterable[EnterpriseContextView] = (),
            system_landscape_views=system_landscape_views,
            system_context_views=system_context_views,
            container_views=container_views,
            component_views=component_views,
            deployment_views=deployment_views,
            configuration=Configuration.hydrate(views.configuration),
        )

    @classmethod
    def _hydrate_view(cls, view: View, model: "Model") -> None:
        for element_view in view.element_views:
            element_view.element = model.get_element(element_view.id)

        for relationship_view in view.relationship_views:
            relationship_view.relationship = model.get_relationship(
                relationship_view.id
            )

    def create_system_landscape_view(
        self, system_landscape_view: Optional[SystemLandscapeView] = None, **kwargs
    ) -> SystemLandscapeView:
        """
        Add a new SystemLandscapeView to the ViewSet.

        Args:
            system_landscape_view (SystemLandscapeView, optional): Either provide a
                `SystemLandscapeView` instance or
            **kwargs: Provide keyword arguments for instantiating a
                `SystemLandscapeView` (recommended).
        """
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
        """
        Add a new SystemContextView to the ViewSet.

        Args:
            system_context_view (SystemContextView, optional): Either provide a
                `SystemContextView` instance or
            **kwargs: Provide keyword arguments for instantiating a `SystemContextView`
                (recommended).
        """
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
        """
        Add a new ContainerView to the ViewSet.

        Args:
            container_view (ContainerView, optional): Either provide a
                `ContainerView` instance or
            **kwargs: Provide keyword arguments for instantiating a `ContainerView`
                (recommended).
        """
        # TODO:
        # assertThatTheSoftwareSystemIsNotNull(softwareSystem);
        # assertThatTheViewKeyIsSpecifiedAndUnique(key);
        if container_view is None:
            container_view = ContainerView(**kwargs)
        container_view.set_viewset(self)
        self.container_views.add(container_view)
        return container_view

    def create_component_view(
        self, component_view: Optional[ComponentView] = None, **kwargs
    ) -> ComponentView:
        """
        Add a new ComponentView to the ViewSet.

        Args:
            component_view (ComponentView, optional): Either provide a
                `ComponentView` instance or
            **kwargs: Provide keyword arguments for instantiating a `ComponentView`
                (recommended).
        """
        # TODO:
        # AssertThatTheViewKeyIsUnique(key);
        if component_view is None:
            component_view = ComponentView(**kwargs)
        component_view.set_viewset(self)
        self.component_views.add(component_view)
        return component_view

    def create_deployment_view(self, **kwargs) -> DeploymentView:
        """
        Add a new DeploymentView to the ViewSet.

        Args:
            **kwargs: Provide keyword arguments for instantiating a `DeploymentView`
        """
        # TODO:
        # AssertThatTheViewKeyIsUnique(key);
        deployment_view = DeploymentView(**kwargs)
        deployment_view.set_viewset(self)
        deployment_view.set_model(self.model)
        self.deployment_views.add(deployment_view)
        return deployment_view

    def copy_layout_information_from(self, source: "ViewSet") -> None:
        """Copy all the layout information from a source ViewSet."""
        for source_view in source.system_landscape_views:
            destination_view = self._find_system_landscape_view(source_view)
            if destination_view:
                destination_view.copy_layout_information_from(source_view)

        for source_view in source.system_context_views:
            destination_view = self._find_system_context_view(source_view)
            if destination_view:
                destination_view.copy_layout_information_from(source_view)

        for source_view in source.container_views:
            destination_view = self._find_container_view(source_view)
            if destination_view:
                destination_view.copy_layout_information_from(source_view)

        for source_view in source.component_views:
            destination_view = self._find_component_view(source_view)
            if destination_view:
                destination_view.copy_layout_information_from(source_view)

        # TODO: dynamic view
        # for source_view in source.dynamic_views:
        #     destination_view = self.find_dynamic_view(source_view)
        #     if destination_view:
        #         destination_view.copy_layout_information_from(source_view)

        for source_view in source.deployment_views:
            destination_view = self._find_deployment_view(source_view)
            if destination_view:
                destination_view.copy_layout_information_from(source_view)

    def _find_system_landscape_view(
        self, view: SystemLandscapeView
    ) -> Optional[SystemLandscapeView]:
        for current_view in self.system_landscape_views:
            if view.key == current_view.key:
                return current_view
        return None

    def _find_system_context_view(
        self,
        view: SystemContextView,
    ) -> Optional[SystemContextView]:
        for current_view in self.system_context_views:
            if view.key == current_view.key:
                return current_view
        return None

    def _find_container_view(self, view: ContainerView) -> Optional[ContainerView]:
        for current_view in self.container_views:
            if view.key == current_view.key:
                return current_view
        return None

    def _find_component_view(self, view: ComponentView) -> Optional[ComponentView]:
        for current_view in self.component_views:
            if view.key == current_view.key:
                return current_view
        return None

    # TODO: dynamic view
    # def find_dynamic_view(self, view: DynamicView) -> DynamicView:
    #     for current_view in self.dynamic_views:
    #         if view.key == current_view.key:
    #             return current_view
    #     return None

    def _find_deployment_view(self, view: DeploymentView) -> DeploymentView:
        for current_view in self.deployment_views:
            if view.key == current_view.key:
                return current_view
        return None
