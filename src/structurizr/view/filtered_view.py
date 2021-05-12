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


"""Provide a filtered view."""

from enum import Enum
from typing import Iterable, List, Optional

from pydantic import Field

from .abstract_view import AbstractView, AbstractViewIO
from .static_view import StaticView


__all__ = ("FilteredView", "FilteredViewIO")


class FilterMode(Enum):
    Include = "Include"
    Exclude = "Exclude"


class FilteredViewIO(AbstractViewIO):
    """
    Represent the FilteredView from the C4 model.

    Attributes:
        base_view_key: The key of the view on which this filtered view is based.
        mode: Whether elements/relationships are being included or excluded based
              upon the set of tag
        tags: The set of tags to include/exclude elements/relationships when rendering
              this filtered view.
    """

    base_view_key: str = Field(alias="baseViewKey")
    mode: FilterMode
    tags: List[str]


class FilteredView(AbstractView):
    """
    Represent the filtered view from the C4 model.

    A FilteredView is a view that is based on another view, but adding or removing
    specific elements specified by tags.

    Attributes:
        view: the view which this FilteredView is based on
        base_view_key: The key of the view on which this filtered view is based.
        mode: Whether elements/relationships are being included or excluded based
              upon the set of tag
        tags: The set of tags to include/exclude elements/relationships when rendering
              this filtered view.
    """

    def __init__(
        self,
        mode: FilterMode,
        tags: Iterable[str],
        view: Optional[StaticView] = None,
        base_view_key: Optional[str] = None,
        **kwargs
    ) -> None:
        """Initialize a filtered view."""
        super().__init__(**kwargs)
        self._base_view_key = base_view_key
        self.view = view
        self.mode = mode
        self.tags = set(tags)

    @property
    def base_view_key(self) -> str:
        """Return the key of the base view."""
        return self.view.key if self.view else self._base_view_key

    @classmethod
    def hydrate(
        cls,
        view_io: FilteredViewIO,
    ) -> "FilteredView":
        """Hydrate a new FilteredView instance from its IO."""
        return cls(
            **cls.hydrate_arguments(view_io),
            base_view_key=view_io.base_view_key,
            mode=view_io.mode,
            tags=view_io.tags
        )
