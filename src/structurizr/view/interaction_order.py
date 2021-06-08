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

"""Provide a type that supports logical sequencing of interactions."""

from typing import Any


class InteractionOrder(str):
    """
    Represent the order of interactions within a diagram.

    Orders are typically expressed as period-separated string, e.g. 1.2a.13, where
    numeric ordering is preserved as opposed to lexical - e.g. 1.13 > 1.2.
    """

    def __new__(cls, order: Any) -> "InteractionOrder":
        """Initialise a new InteractionOrder instance."""
        order_str = str(order)
        self = super(InteractionOrder, cls).__new__(cls, order_str)
        self._segments = order_str.split(".")
        return self

    def __lt__(self, other: "InteractionOrder") -> bool:
        """Return true if the this InteractionOrder is logically less than other."""
        if not isinstance(other, InteractionOrder):
            raise TypeError

        for (a, b) in zip(self._segments, other._segments):
            if _segment_less_than(a, b):
                return True
            elif _segment_less_than(b, a):
                return False

        return len(self._segments) < len(other._segments)

    def __le__(self, other: "InteractionOrder") -> bool:
        """Return true if the this InteractionOrder is logically <= other."""
        return not other < self

    def __gt__(self, other: "InteractionOrder") -> bool:
        """Return true if the this InteractionOrder is logically greater than other."""
        return other < self

    def __ge__(self, other: "InteractionOrder") -> bool:
        """Return true if the this InteractionOrder is logically >= other."""
        return not self < other


def _segment_less_than(a: str, b: str) -> bool:
    """Return True if a is logically less that b."""
    max_len = max(len(a), len(b))
    return a.rjust(max_len) < b.rjust(max_len)
