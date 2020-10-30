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


"""Provide a configuration for rendering a workspace."""


from typing import Optional

from pydantic import Field

from ..abstract_base import AbstractBase
from ..base_model import BaseModel
from .branding import Branding, BrandingIO
from .styles import Styles, StylesIO
from .terminology import Terminology, TerminologyIO
from .view_sort_order import ViewSortOrder


__all__ = ("Configuration", "ConfigurationIO")


class ConfigurationIO(BaseModel):
    """Represent a configuration instance."""

    branding: Optional[BrandingIO]
    styles: Optional[StylesIO]
    theme: Optional[str]
    terminology: Optional[TerminologyIO]
    default_view: Optional[str] = Field(None, alias="defaultView")
    last_saved_view: Optional[str] = Field(None, alias="lastSavedView")
    view_sort_order: ViewSortOrder = Field(
        default=ViewSortOrder.Default,
        alias="viewSortOrder",
    )


class Configuration(AbstractBase):
    """Configure how information in a workspace is rendered."""

    def __init__(
        self,
        *,
        branding: Optional[Branding] = None,
        styles: Optional[Styles] = None,
        theme: Optional[str] = None,
        terminology: Optional[Terminology] = None,
        default_view: Optional[str] = None,
        last_saved_view: Optional[str] = None,
        view_sort_order: ViewSortOrder = ViewSortOrder.Default,
        **kwargs
    ) -> None:
        """Initialize an element view."""
        super().__init__(**kwargs)
        self.branding = Branding() if branding is None else branding
        self.styles = Styles() if styles is None else styles
        self.theme = theme
        self.terminology = Terminology() if terminology is None else terminology
        self.default_view = default_view
        self.last_saved_view = last_saved_view
        self.view_sort_order = view_sort_order

    @classmethod
    def hydrate(cls, configuration_io: ConfigurationIO) -> "Configuration":
        """Hydrate new Configuration instance from its IO."""
        return cls(
            # TODO:
            # branding=Branding.hydrate(configuration_io.branding),
            styles=Styles.hydrate(configuration_io.styles),
            theme=configuration_io.theme,
            # terminology=Terminology.hydrate(configuration_io.terminology),
            default_view=configuration_io.default_view,
            last_saved_view=configuration_io.last_saved_view,
            view_sort_order=configuration_io.view_sort_order,
        )
