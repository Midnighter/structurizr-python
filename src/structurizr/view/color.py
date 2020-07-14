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


"""Provide a color object to validate and serialize colors."""


import pydantic.color


class Color(pydantic.color.Color):
    """Represent a natural color."""

    def as_hex(self) -> str:
        """Return a six character hex representation of the color."""
        values = [pydantic.color.float_to_255(c) for c in self._rgba[:3]]
        if self._rgba.alpha is not None:
            values.append(pydantic.color.float_to_255(self._rgba.alpha))

        return f"#{''.join(f'{v:02x}' for v in values)}"

    def __str__(self) -> str:
        """Return a hex string representation of the color."""
        return self.as_hex()
