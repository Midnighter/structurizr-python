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


"""Provide required tags."""


from ..abstract_base import AbstractBase


__all__ = ("Tags",)


class Tags(AbstractBase):
    """Define required tags."""

    ELEMENT = "Element"
    RELATIONSHIP = "Relationship"

    PERSON = "Person"
    SOFTWARE_SYSTEM = "Software System"
    CONTAINER = "Container"
    COMPONENT = "Component"

    DEPLOYMENT_NODE = "Deployment Node"
    CONTAINER_INSTANCE = "Container Instance"

    SYNCHRONOUS = "Synchronous"
    ASYNCHRONOUS = "Asynchronous"
