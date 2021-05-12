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


"""Provide a superclass for all views."""


from abc import ABC
from typing import Dict

from ..abstract_base import AbstractBase
from ..base_model import BaseModel
from ..mixin import ViewSetRefMixin


__all__ = ("AbstractView", "AbstractViewIO")


class AbstractViewIO(BaseModel, ABC):
    """
    Define an abstract base class for all views.

    Views include static views, dynamic views, deployment views and filtered views.
    """

    key: str
    description: str = ""
    title: str = ""


class AbstractView(ViewSetRefMixin, AbstractBase, ABC):
    """
    Define an abstract base class for all views.

    Views include static views, dynamic views, deployment views and filtered views.

    """

    def __init__(
        self,
        *,
        key: str = None,
        description: str,
        title: str = "",
        **kwargs,
    ):
        """Initialize a view with a 'private' view set."""
        super().__init__(**kwargs)
        self.key = key
        self.description = description
        self.title = title

    def __repr__(self) -> str:
        """Return repr(self)."""
        return f"{type(self).__name__}(key={self.key})"

    @classmethod
    def hydrate_arguments(cls, view_io: AbstractViewIO) -> Dict:
        """Hydrate an AbstractViewIO into the constructor args for AbstractView."""
        return {
            "key": view_io.key,
            "description": view_io.description,
            "title": view_io.title,
        }
