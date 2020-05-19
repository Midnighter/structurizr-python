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


"""Provide a container for an element instance in a view."""


from typing import Optional

from pydantic import Field

from ..abstract_base import AbstractBase
from ..base_model import BaseModel


__all__ = ("Terminology", "TerminologyIO")


class TerminologyIO(BaseModel):
    """
    Represent an instance of an element in a view.

    Attributes:

    """

    enterprise: Optional[str]
    person: Optional[str]
    software_system: Optional[str] = Field(None, alias="softwareSystem")
    container: Optional[str]
    component: Optional[str]
    code: Optional[str]
    deployment_node: Optional[str] = Field(None, alias="deploymentNode")
    relationship: Optional[str]


class Terminology(AbstractBase):
    """
    Provides a way for the terminology on diagrams, etc to be modified (e.g. language translations).

    Attributes:

    """

    def __init__(
        self,
        *,
        enterprise: Optional[str] = None,
        person: Optional[str] = None,
        software_system: Optional[str] = None,
        container: Optional[str] = None,
        component: Optional[str] = None,
        code: Optional[str] = None,
        deployment_node: Optional[str] = None,
        relationship: Optional[str] = None,
        **kwargs
    ) -> None:
        """Initialize an element view."""
        super().__init__(**kwargs)
        self.enterprise = enterprise
        self.person = person
        self.software_system = software_system
        self.container = container
        self.component = component
        self.code = code
        self.deployment_node = deployment_node
        self.relationship = relationship
