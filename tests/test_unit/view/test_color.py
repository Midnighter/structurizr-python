# Copyright (c) 2020, Moritz E. Beber, Ilai Fallach.
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


"""Ensure the expected behaviour of the color type."""


import pydantic
import pytest

from structurizr.view.color import Color


@pytest.mark.parametrize(
    "color",
    [
        {"value": "#ffffff", "expected": "#ffffff"},
        {"value": "#fff", "expected": "#ffffff"},
        {"value": "#f0f0f0", "expected": "#f0f0f0"},
        {"value": "#000", "expected": "#000000"},
        {"value": "#000000", "expected": "#000000"},
        {"value": "green", "expected": "#008000"},
        {"value": "white", "expected": "#ffffff"},
        pytest.param(
            {"value": "never-gonna-let-you-down", "expected": None},
            marks=pytest.mark.raises(
                exception=pydantic.errors.ColorError,
                message=(
                    "value is not a valid color: string not "
                    "recognised as a valid color"
                ),
            ),
        ),
    ],
)
def test_code_element_init(color):
    """Expect proper initialization from arguments."""
    assert str(Color(color["value"])) == color["expected"]
