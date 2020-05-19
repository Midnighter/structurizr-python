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


"""Provide different views onto a Structurizr software architecture."""

from .border import Border
from .shape import Shape
from .orientation import Orientation
from .paper_size import PaperSize
from .rank_direction import RankDirection
from .automatic_layout import AutomaticLayout, AutomaticLayoutIO
from .animation import Animation, AnimationIO
from .system_context_view import SystemContextView, SystemContextViewIO
from .view_set import ViewSet, ViewSetIO
from .element_style import ElementStyle
