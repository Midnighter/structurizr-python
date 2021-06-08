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

"""Provide a sequence number, used in Dynamic views."""


from .interaction_order import InteractionOrder
from .sequence_counter import (
    ParallelSequenceCounter,
    SequenceCounter,
    SubsequenceCounter,
)


class SequenceNumber:
    """A class to provide interaction sequence numbers."""

    def __init__(self):
        """Initialise a new SequenceNumber instance."""
        self.counter = SequenceCounter()

    def get_next(self) -> InteractionOrder:
        """Return the next number in the sequence."""
        self.counter.increment()
        return InteractionOrder(self.counter)

    def start_subsequence(self):
        """Start a subsequence.

        See `DynamicView.subvsequence()` for an explanation.
        """
        self.counter = SubsequenceCounter(self.counter)

    def end_subsequence(self):
        """End an active subsequence."""
        self.counter = self.counter.parent

    def start_parallel_sequence(self):
        """Begin a parallel sequence.

        See `DynamicView.parallel_sequence()` for an explanation.
        """
        self.counter = ParallelSequenceCounter(self.counter)

    def end_parallel_sequence(self, continue_numbering: bool):
        """End a parallel sequence.

        Args:
            continue_numbering: if True then the main sequence will continue from
                                the next number after this parallel sequence, else
                                it will reset back to before this parallel sequence
                                began.

        See `DynamicView.parallel_sequence()` for an explanation.
        """
        if continue_numbering:
            sequence = self.counter.sequence
            self.counter = self.counter.parent
            self.counter.sequence = sequence
        else:
            self.counter = self.counter.parent
