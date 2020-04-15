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


"""Provide an architectural perspective model."""


from pydantic import Field

from ..abstract_base import AbstractBase
from ..base_model import BaseModel


__all__ = ("Perspective", "PerspectiveIO")


class PerspectiveIO(BaseModel):
    """
    Represent an architectural perspective.

    Architectural perspectives can be applied to elements and relationships.

    Notes:
        See https://www.viewpoints-and-perspectives.info/home/perspectives/ for more
        details of this concept.

    Attributes:
        name (str): The name of the perspective, e.g., 'Security'.
        description (str): A longer description of the architectural perspective.

    """

    name: str = Field(..., description="The name of the perspective, e.g., 'Security'.")
    description: str = Field(
        ..., description="A longer description of the architectural perspective."
    )


class Perspective(AbstractBase):
    """
    Represent an architectural perspective.

    Architectural perspectives can be applied to elements and relationships.

    Notes:
        See https://www.viewpoints-and-perspectives.info/home/perspectives/ for more
        details of this concept.

    Attributes:
        name (str): The name of the perspective, e.g., 'Security'.
        description (str): A longer description of the architectural perspective.

    """

    def __init__(self, *, name: str, description: str, **kwargs) -> None:
        """Initialize an architectural perspective."""
        super().__init__(**kwargs)
        self.name = name
        self.description = description
