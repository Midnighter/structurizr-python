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

"""Provie a Dynamic View.

A dynamic diagram can be useful when you want to show how elements in a static model
collaborate at runtime to implement a user story, use case, feature, etc. This dynamic
diagram is based upon a UML communication diagram (previously known as a "UML
collaboration diagram"). It is similar to a UML sequence diagram although it allows a
free-form arrangement of diagram elements with numbered interactions to indicate
ordering.
"""

from ..mixin.model_ref_mixin import ModelRefMixin
from .view import View, ViewIO


__all__ = ("DynamicView", "DynamicViewIO")


class DynamicViewIO(ViewIO):
    """Represent the dynamic view from the C4 model."""

    pass


class DynamicView(ModelRefMixin, View):
    """Represent the dynamic view from the C4 model."""

    def __init__(self, **kwargs) -> None:
        """Initialize a DynamicView."""
        super().__init__(**kwargs)

    @classmethod
    def hydrate(cls, io: DynamicViewIO) -> "DynamicView":
        """Hydrate a new DynamicView instance from its IO."""
        return cls(
            **cls.hydrate_arguments(io),
        )
