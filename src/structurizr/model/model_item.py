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

from ordered_set import OrderedSet
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

    id: str = Field(default="")
    tags: List[str] = Field(default=())
    properties: Dict[str, str] = Field(default={})
    perspectives: List[PerspectiveIO] = Field(default=())

    @validator("tags", pre=True)
    def split_tags(cls, tags: Union[str, Iterable[str]]) -> List[str]:
        """Convert comma-separated tag list into list if needed."""
        if isinstance(tags, str):
            return tags.split(",")
        return list(tags)

    def dict(self, **kwargs) -> dict:
        """Map this IO into a dictionary suitable for serialisation."""
        obj = super().dict(**kwargs)
        if "tags" in obj:
            obj["tags"] = ",".join(obj["tags"])
        return obj


class ModelItem(AbstractBase, ABC):
    """
    Define a base class for elements and relationships.

    Attributes:
        id (str):
        tags (set of str):
        properties (dict):
        perspectives (set of Perspective):

    """

    def __init__(
        self,
        *,
        id: str = "",
        tags: Iterable[str] = (),
        properties: Dict[str, str] = (),
        perspectives: Iterable[Perspective] = (),
        **kwargs,
    ):
        """Initialise a ModelItem instance."""
        super().__init__(**kwargs)
        self.id = id
        self.tags = OrderedSet(tags)
        self.properties = dict(properties)
        self.perspectives = set(perspectives)

    def __repr__(self) -> str:
        """Return repr(self)."""
        return f"{type(self).__name__}(id={self.id})"

    @classmethod
    def hydrate_arguments(cls, model_item_io: ModelItemIO) -> dict:
        """Hydrate an ModelItemIO into the constructor arguments for ModelItem."""
        return {
            "id": model_item_io.id,
            "tags": model_item_io.tags,
            "properties": model_item_io.properties,  # TODO: implement
            "perspectives": map(Perspective.hydrate, model_item_io.perspectives),
        }
