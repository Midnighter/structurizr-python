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


"""Ensure the expected behaviour of the interaction style enumeration."""


import pytest

from structurizr.model.interaction_style import InteractionStyle


@pytest.mark.parametrize(
    "style, expected",
    [
        ("Synchronous", InteractionStyle.Synchronous),
        ("Asynchronous", InteractionStyle.Asynchronous),
    ],
)
def test_interaction_style(style: str, expected: InteractionStyle):
    """Expect proper initialization from interaction style strings."""
    assert InteractionStyle(style) == expected
