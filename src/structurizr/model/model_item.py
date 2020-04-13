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


"""Provide the base class for elements and relationships."""


from abc import ABC
from typing import Dict, Set

from pydantic import BaseModel, Field

from .perspective import Perspective


__all__ = ("ModelItem",)


class ModelItem(BaseModel, ABC):
    """
    Define a base class for elements and relationships.

    Attributes:
        id (str):
        origin_id (str):
        tags (set of str):
        properties (dict):
        perspectives (set of Perspective):

    """

    id: str = Field("")
    origin_id: str = Field("", alias="originId")
    tags: Set[str] = Field(set())
    properties: Dict[str, str] = Field({})
    perspectives: Set[Perspective] = Field(set())

    def __hash__(self) -> int:
        """Return an integer that represents a unique hash value for this instance."""
        return id(self)
