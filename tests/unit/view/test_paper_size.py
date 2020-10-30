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


"""Test that the paper size enum behaves as expected."""

from collections import namedtuple

import pytest

from structurizr.view import Orientation, PaperSize


Dimensions = namedtuple("Dimensions", "value, size, orientation, width, height")


@pytest.fixture(
    scope="module",
    params=[
        ("A6_Portrait", "A6", Orientation.Portrait, 1240, 1748),
        ("A6_Landscape", "A6", Orientation.Landscape, 1748, 1240),
        ("A5_Portrait", "A5", Orientation.Portrait, 1748, 2480),
        ("A5_Landscape", "A5", Orientation.Landscape, 2480, 1748),
        ("A4_Portrait", "A4", Orientation.Portrait, 2480, 3508),
        ("A4_Landscape", "A4", Orientation.Landscape, 3508, 2480),
        ("A3_Portrait", "A3", Orientation.Portrait, 3508, 4961),
        ("A3_Landscape", "A3", Orientation.Landscape, 4961, 3508),
        ("A2_Portrait", "A2", Orientation.Portrait, 4961, 7016),
        ("A2_Landscape", "A2", Orientation.Landscape, 7016, 4961),
        ("A1_Portrait", "A1", Orientation.Portrait, 7016, 9933),
        ("A1_Landscape", "A1", Orientation.Landscape, 9933, 7016),
        ("A0_Portrait", "A0", Orientation.Portrait, 9933, 14043),
        ("A0_Landscape", "A0", Orientation.Landscape, 14043, 9933),
        ("Letter_Portrait", "Letter", Orientation.Portrait, 2550, 3300),
        ("Letter_Landscape", "Letter", Orientation.Landscape, 3300, 2550),
        ("Legal_Portrait", "Legal", Orientation.Portrait, 2550, 4200),
        ("Legal_Landscape", "Legal", Orientation.Landscape, 4200, 2550),
        ("Slide_4_3", "Slide 4:3", Orientation.Landscape, 3306, 2480),
        ("Slide_16_9", "Slide 16:9", Orientation.Landscape, 3508, 1973),
        ("Slide_16_10", "Slide 16:10", Orientation.Landscape, 3508, 2193),
    ],
    ids=[
        "A6_Portrait",
        "A6_Landscape",
        "A5_Portrait",
        "A5_Landscape",
        "A4_Portrait",
        "A4_Landscape",
        "A3_Portrait",
        "A3_Landscape",
        "A2_Portrait",
        "A2_Landscape",
        "A1_Portrait",
        "A1_Landscape",
        "A0_Portrait",
        "A0_Landscape",
        "Letter_Portrait",
        "Letter_Landscape",
        "Legal_Portrait",
        "Legal_Landscape",
        "Slide_4_3",
        "Slide_16_9",
        "Slide_16_10",
    ],
)
def expected(request):
    """Return expected dimensions to use in test cases."""
    return Dimensions(*request.param)


def test_from_value(expected: Dimensions):
    """Test getting a PaperSize by value for each size."""
    paper = PaperSize(expected.value)
    assert paper.name == expected.value
    assert paper.value == expected.value
    assert paper.size == expected.size
    assert paper.orientation == expected.orientation
    assert paper.width == expected.width
    assert paper.height == expected.height


def test_from_getitem(expected: Dimensions):
    """Test getting a PaperSize with getitem for each size."""
    paper = PaperSize[expected.value]
    assert paper.name == expected.value
    assert paper.value == expected.value
    assert paper.size == expected.size
    assert paper.orientation == expected.orientation
    assert paper.width == expected.width
    assert paper.height == expected.height


def test_from_attribute(expected: Dimensions):
    """Test getting a PaperSize as attribute of enum for each size."""
    paper = getattr(PaperSize, expected.value)
    assert paper.name == expected.value
    assert paper.value == expected.value
    assert paper.size == expected.size
    assert paper.orientation == expected.orientation
    assert paper.width == expected.width
    assert paper.height == expected.height
