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
    "value, expected",
    [
        ("#ffffff", "#ffffff"),
        ("#fff", "#ffffff"),
        ("#f0f0f0", "#f0f0f0"),
        ("#000", "#000000"),
        ("#000000", "#000000"),
        ("green", "#008000"),
        ("white", "#ffffff"),
        pytest.param(
            "never-gonna-let-you-down",
            "",
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
def test_color_str_value(value: str, expected: str) -> None:
    """Expect that the color string value is a six character hex code."""
    assert str(Color(value)) == expected
