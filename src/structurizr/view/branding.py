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


"""Provide an implementation of a corporate branding."""


from typing import Optional

from ..abstract_base import AbstractBase
from ..base_model import BaseModel
from .font import Font, FontIO


__all__ = ("Branding", "BrandingIO")


class BrandingIO(BaseModel):
    """
    Represent an instance of a corporate branding.

    Attributes:

    """

    logo: Optional[str]
    font: Optional[FontIO]


class Branding(AbstractBase):
    """
    Represent a corporate branding.

    Attributes:

    """

    def __init__(
        self, *, logo: Optional[str] = None, font: Optional[Font] = None, **kwargs
    ) -> None:
        """Initialize a corporate branding."""
        super().__init__(**kwargs)
        self.logo = logo
        self.font = font
