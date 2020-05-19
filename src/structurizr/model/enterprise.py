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


"""Provide an enterprise model."""


from pydantic import Field

from ..abstract_base import AbstractBase
from ..base_model import BaseModel


__all__ = ("Enterprise", "EnterpriseIO")


class EnterpriseIO(BaseModel):
    """
    Represent an enterprise.

    Attributes:
        name (str): The name of the enterprise.

    """

    name: str = Field(..., description="The name of the enterprise.")


class Enterprise(AbstractBase):
    """
    Represent an enterprise.

    Attributes:
        name (str): The name of the enterprise.

    """

    def __init__(self, *, name: str, **kwargs) -> None:
        """Initialize an enterprise by name."""
        super().__init__(**kwargs)
        self.name = name

    @classmethod
    def hydrate(cls, enterprise_io: EnterpriseIO) -> "Enterprise":
        """"""
        return cls(name=enterprise_io.name)
