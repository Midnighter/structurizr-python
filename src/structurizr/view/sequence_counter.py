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

"""Provide an incrementing sequence counter."""


class SequenceCounter:
    """Provides an incrementing counter."""

    def __init__(self, parent: "SequenceCounter" = None):
        """Initialise a new SequenceCounter."""
        self.sequence = 0
        self.parent = parent

    def increment(self):
        """Advance the counter."""
        self.sequence += 1

    def __str__(self):
        """Provide a string representation of the counter."""
        return str(self.sequence)


class ParallelSequenceCounter(SequenceCounter):
    """Provide support for parallel sequences."""

    def __init__(self, parent: SequenceCounter):
        """Initialise a new ParallelSequenceCounter instance."""
        super().__init__(parent)
        self.sequence = parent.sequence


class SubsequenceCounter(SequenceCounter):
    """Provide support for subsequences."""

    def __init__(self, parent: SequenceCounter):
        """Initialise a new SubsequenceCounter instance."""
        super().__init__(parent)

    def __str__(self):
        """Provide a string representation of the counter."""
        return f"{self.parent}.{self.sequence}"
