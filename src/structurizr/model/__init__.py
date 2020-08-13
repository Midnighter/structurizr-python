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


"""Provide models for defining a Structurizr software architecture."""


from .enterprise import Enterprise, EnterpriseIO
from .perspective import Perspective, PerspectiveIO
from .location import Location
from .interaction_style import InteractionStyle
from .element import Element, ElementIO
from .person import Person, PersonIO
from .software_system import SoftwareSystem, SoftwareSystemIO
from .relationship import Relationship, RelationshipIO
from .model import Model, ModelIO
from .tags import Tags
from .container import Container, ContainerIO
from .component import Component, ComponentIO


_symbols = locals()

RelationshipIO.update_forward_refs(**_symbols)
