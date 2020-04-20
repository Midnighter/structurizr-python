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


"""Provide a superclass for deployment nodes and container instances."""


from abc import ABC

from .element import Element, ElementIO


__all__ = ("DeploymentElement", "DeploymentElementIO")


DEFAULT_DEPLOYMENT_ENVIRONMENT = "Default"


class DeploymentElementIO(ElementIO, ABC):
    """
    Define a superclass for all deployment elements.

    Attributes:
        environment (str):

    """

    environment: str = DEFAULT_DEPLOYMENT_ENVIRONMENT


class DeploymentElement(Element, ABC):
    """
    Define a superclass for all deployment elements.

    Attributes:
        environment (str):

    """

    def __init__(
        self, *, environment: str = DEFAULT_DEPLOYMENT_ENVIRONMENT, **kwargs
    ) -> None:
        """Initialize a deployment element."""
        super().__init__(**kwargs)
        self.environment = environment
