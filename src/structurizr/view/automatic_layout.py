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


"""Provide an automatic layout configuration."""


from pydantic import BaseModel, Field

from .rank_direction import RankDirection


__all__ = ("AutomaticLayout",)


class AutomaticLayout(BaseModel):
    """
    Define a wrapper for automatic layout configuration.

    Attributes:

    """

    rank_direction: RankDirection = Field(..., alias="rankDirection")
    rank_separation: int = Field(..., alias="rankSeparation")
    node_separation: int = Field(..., alias="nodeSeparation")
    edge_separation: int = Field(..., alias="edgeSeparation")
    vertices: bool
