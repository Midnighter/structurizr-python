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


"""Provide a mixin that includes a view set reference."""


from typing import TYPE_CHECKING
from weakref import ref


if TYPE_CHECKING:
    from ..view import ViewSet


__all__ = ("ViewSetRefMixin",)


class ViewSetRefMixin:
    """Define a view set reference mixin."""

    def __init__(self, **kwargs) -> None:
        """Initialize the mixin."""
        super().__init__(**kwargs)
        self._viewset = lambda: None

    def get_viewset(self) -> "ViewSet":
        """
        Retrieve the view set instance from the reference.

        Returns:
            ViewSet: The view set, if any.

        Raises:
            RuntimeError: In case there exists no referenced view set.

        """
        view_set = self._viewset()
        if view_set is None:
            raise RuntimeError(
                f"You must add this {type(self).__name__} view to a view set instance "
                f"first."
            )
        return view_set

    def set_viewset(self, viewset: "ViewSet") -> None:
        """
        Create a weak reference to a view set instance.

        Warnings:
            This is an internal method and should not be directly called by users.

        Args:
            viewset (ViewSet):

        """
        self._viewset = ref(viewset)
