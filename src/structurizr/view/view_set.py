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


from itertools import chain
from typing import TYPE_CHECKING, Iterable, List, Optional, Set

from pydantic import Field

from ..abstract_base import AbstractBase
from ..base_model import BaseModel
from ..mixin import ModelRefMixin
from .abstract_view import AbstractView
from .component_view import ComponentView, ComponentViewIO
from .configuration import Configuration, ConfigurationIO
from .container_view import ContainerView, ContainerViewIO
from .deployment_view import DeploymentView, DeploymentViewIO
from .dynamic_view import DynamicView, DynamicViewIO
from .filtered_view import FilteredView, FilteredViewIO
from .system_context_view import SystemContextView, SystemContextViewIO
from .system_landscape_view import SystemLandscapeView, SystemLandscapeViewIO
from .view import View


if TYPE_CHECKING:
    from ..model import Model  # pragma: no cover


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
    dynamic_views: List[DynamicViewIO] = Field(default=(), alias="dynamicViews")
    filtered_views: List[FilteredViewIO] = Field(default=(), alias="filteredViews")


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
        filtered_views: Iterable[FilteredView] = (),
        dynamic_views: Iterable[DynamicView] = (),
        configuration: Optional[Configuration] = None,
        **kwargs,
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
        self.dynamic_views: Set[DynamicView] = set(dynamic_views)
        self.filtered_views: Set[FilteredView] = set(filtered_views)
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

        dynamic_views = []
        for view_io in views.dynamic_views:
            element = (
                model.get_element(view_io.element_id) if view_io.element_id else None
            )
            view = DynamicView.hydrate(view_io, element=element)
            cls._hydrate_view(view, model=model)
            dynamic_views.append(view)

        filtered_views = [
            FilteredView.hydrate(view_io) for view_io in views.filtered_views
        ]

        result = cls(
            model=model,
            # TODO:
            # enterprise_context_views: Iterable[EnterpriseContextView] = (),
            system_landscape_views=system_landscape_views,
            system_context_views=system_context_views,
            container_views=container_views,
            component_views=component_views,
            deployment_views=deployment_views,
            dynamic_views=dynamic_views,
            filtered_views=filtered_views,
            configuration=Configuration.hydrate(views.configuration),
        )

        # Patch up filtered views
        for filtered_view in result.filtered_views:
            filtered_view.view = result[filtered_view.base_view_key]

        return result

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
        if system_landscape_view is None:
            system_landscape_view = SystemLandscapeView(
                model=self.get_model(), **kwargs
            )
        self._ensure_key_is_specific_and_unique(system_landscape_view.key)
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
        if system_context_view is None:
            system_context_view = SystemContextView(**kwargs)
        self._ensure_key_is_specific_and_unique(system_context_view.key)
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
        if container_view is None:
            container_view = ContainerView(**kwargs)
        self._ensure_key_is_specific_and_unique(container_view.key)
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
        if component_view is None:
            component_view = ComponentView(**kwargs)
        self._ensure_key_is_specific_and_unique(component_view.key)
        component_view.set_viewset(self)
        self.component_views.add(component_view)
        return component_view

    def create_deployment_view(self, **kwargs) -> DeploymentView:
        """
        Add a new DeploymentView to the ViewSet.

        Args:
            **kwargs: Provide keyword arguments for instantiating a `DeploymentView`
        """
        deployment_view = DeploymentView(**kwargs)
        self._ensure_key_is_specific_and_unique(deployment_view.key)
        deployment_view.set_viewset(self)
        deployment_view.set_model(self.model)
        self.deployment_views.add(deployment_view)
        return deployment_view

    def create_dynamic_view(self, **kwargs) -> DynamicView:
        """
        Add a new DynamicView to the ViewSet.

        Args:
            **kwagrs: Provide keyword arguments for instantiating a `DynamicView`.
        """
        dynamic_view = DynamicView(**kwargs)
        self._ensure_key_is_specific_and_unique(dynamic_view.key)
        dynamic_view.set_viewset(self)
        dynamic_view.set_model(self.model)
        self.dynamic_views.add(dynamic_view)
        return dynamic_view

    def create_filtered_view(self, **kwargs) -> FilteredView:
        """
        Add a new FilteredView to the ViewSet.

        Args:
            **kwargs: Provide keyword arguments for instantiating a `FilteredView`.
        """
        filtered_view = FilteredView(**kwargs)
        self._ensure_key_is_specific_and_unique(filtered_view.key)
        filtered_view.set_viewset(self)
        self.filtered_views.add(filtered_view)
        return filtered_view

    def get_view(self, key: str) -> Optional[AbstractView]:
        """Return the view with the given key, or None."""
        all_views = chain(
            self.system_landscape_views,
            self.system_context_views,
            self.container_views,
            self.component_views,
            self.deployment_views,
            self.dynamic_views,
            self.filtered_views,
        )
        return next((view for view in all_views if view.key == key), None)

    def __getitem__(self, key: str) -> AbstractView:
        """Return the view with the given key or raise a KeyError."""
        result = self.get_view(key)
        if not result:
            raise KeyError(f"No view with key '{key}' in ViewSet")
        return result

    def copy_layout_information_from(self, source: "ViewSet") -> None:
        """Copy all the layout information from a source ViewSet."""

        # Note that filtered views don't have any layout information to copy.
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

        for source_view in source.dynamic_views:
            destination_view = self._find_dynamic_view(source_view)
            if destination_view:
                destination_view.copy_layout_information_from(source_view)

        for source_view in source.deployment_views:
            destination_view = self._find_deployment_view(source_view)
            if destination_view:
                destination_view.copy_layout_information_from(source_view)

    def _ensure_key_is_specific_and_unique(self, key: str) -> None:
        if key is None or key == "":
            raise ValueError("A key must be specified.")
        if self.get_view(key) is not None:
            raise ValueError(f"View already exists in workspace with key '{key}'.")

    def _find_system_landscape_view(
        self, view: SystemLandscapeView
    ) -> Optional[SystemLandscapeView]:
        for current_view in self.system_landscape_views:
            if view.key == current_view.key:
                return current_view

    def _find_system_context_view(
        self,
        view: SystemContextView,
    ) -> Optional[SystemContextView]:
        for current_view in self.system_context_views:
            if view.key == current_view.key:
                return current_view

    def _find_container_view(self, view: ContainerView) -> Optional[ContainerView]:
        for current_view in self.container_views:
            if view.key == current_view.key:
                return current_view

    def _find_component_view(self, view: ComponentView) -> Optional[ComponentView]:
        for current_view in self.component_views:
            if view.key == current_view.key:
                return current_view

    def _find_dynamic_view(self, view: DynamicView) -> Optional[DynamicView]:
        for current_view in self.dynamic_views:
            if view.key == current_view.key:
                return current_view

    def _find_deployment_view(self, view: DeploymentView) -> DeploymentView:
        for current_view in self.deployment_views:
            if view.key == current_view.key:
                return current_view
