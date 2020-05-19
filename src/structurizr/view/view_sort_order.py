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


"""Provide different ways sort the order of views."""


from enum import Enum, unique


__all__ = ("ViewSortOrder",)


@unique
class ViewSortOrder(Enum):
    """
    Customize a view sort order.

    Attributes:
        Default: Views are grouped by the software system they are associated with, and
            then sorted by type (System Landscape, System Context, Container, Component,
            Dynamic and Deployment) within these groups.
        Type: Views are sorted by type (System Landscape, System Context, Container,
            Component, Dynamic and Deployment).
        Key: Views are sorted by the view key (alphabetical, ascending).

    """

    Default = "Default"
    Type = "Type"
    Key = "Key"
