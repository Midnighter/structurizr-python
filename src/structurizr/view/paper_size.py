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


"""Provide a representation of paper size."""


from enum import Enum

from .orientation import Orientation


__all__ = ("PaperSize",)


class PaperSize(Enum):
    """Represent paper sizes in pixels at 300dpi."""

    A6_Portrait = ("A6", Orientation.Portrait, 1240, 1748)
    A6_Landscape = ("A6", Orientation.Landscape, 1748, 1240)

    A5_Portrait = ("A5", Orientation.Portrait, 1748, 2480)
    A5_Landscape = ("A5", Orientation.Landscape, 2480, 1748)

    A4_Portrait = ("A4", Orientation.Portrait, 2480, 3508)
    A4_Landscape = ("A4", Orientation.Landscape, 3508, 2480)

    A3_Portrait = ("A3", Orientation.Portrait, 3508, 4961)
    A3_Landscape = ("A3", Orientation.Landscape, 4961, 3508)

    A2_Portrait = ("A2", Orientation.Portrait, 4961, 7016)
    A2_Landscape = ("A2", Orientation.Landscape, 7016, 4961)

    A1_Portrait = ("A1", Orientation.Portrait, 7016, 9933)
    A1_Landscape = ("A1", Orientation.Landscape, 9933, 7016)

    A0_Portrait = ("A0", Orientation.Portrait, 9933, 14043)
    A0_Landscape = ("A0", Orientation.Landscape, 14043, 9933)

    Letter_Portrait = ("Letter", Orientation.Portrait, 2550, 3300)
    Letter_Landscape = ("Letter", Orientation.Landscape, 3300, 2550)

    Legal_Portrait = ("Legal", Orientation.Portrait, 2550, 4200)
    Legal_Landscape = ("Legal", Orientation.Landscape, 4200, 2550)

    Slide_4_3 = ("Slide 4:3", Orientation.Landscape, 3306, 2480)
    Slide_16_9 = ("Slide 16:9", Orientation.Landscape, 3508, 1973)
    Slide_16_10 = ("Slide 16:10", Orientation.Landscape, 3508, 2193)

    def __init__(
        self, name: str, orientation: Orientation, width: int, height: int, **kwargs
    ) -> None:
        """Initialize a specific paper size."""
        super().__init__(**kwargs)
        self.size_name = name
        self.orientation = orientation
        self.width = width
        self.height = height
