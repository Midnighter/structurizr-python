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


class SequenceNumber:
    """A class to provide interaction sequence numbers."""

    def __init__(self):
        """Initialise a new SequenceNumber instance."""
        self.counter = 0

    def get_next(self) -> str:
        """Return the next number in the sequence."""
        self.counter += 1
        return str(self.counter)
