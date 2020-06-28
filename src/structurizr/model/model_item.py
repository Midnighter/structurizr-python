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
from typing import Dict, Iterable, List, Union

from pydantic import Field, validator

from ..abstract_base import AbstractBase
from ..base_model import BaseModel
from .perspective import Perspective, PerspectiveIO


__all__ = ("ModelItemIO", "ModelItem")


class ModelItemIO(BaseModel, ABC):
    """
    Define a base class for elements and relationships.

    Attributes:
        id (str):
        tags (set of str):
        properties (dict):
        perspectives (set of Perspective):

    """

    id: str = Field("")
    tags: List[str] = Field([])
    properties: Dict[str, str] = Field({})
    perspectives: List[PerspectiveIO] = Field([])

    @validator("tags", pre=True)
    def split_tags(cls, tags: Union[str, List[str]]) -> List[str]:
        if isinstance(tags, str):
            return tags.split(",")
        return tags

    def dict(self, **kwargs) -> dict:
        """"""
        obj = super().dict(**kwargs)
        if "tags" in obj and len(obj["tags"]) > 0:
            obj["tags"] = ",".join(obj["tags"])
        return obj


class ModelItem(AbstractBase, ABC):
    """
    Define a base class for elements and relationships.

    Attributes:
        id (str):
        origin_id (str):
        tags (set of str):
        properties (dict):
        perspectives (set of Perspective):

    """

    def __init__(
        self,
        *,
        id: str = "",
        origin_id: str = "",
        tags: Iterable[str] = (),
        properties: [Dict[str, str]] = (),
        perspectives: Iterable[Perspective] = (),
        **kwargs
    ):
        """"""
        super().__init__(**kwargs)
        self.id = id
        self.origin_id = origin_id
        self.tags = set(tags)
        self.properties = dict(properties)
        self.perspectives = set(perspectives)
