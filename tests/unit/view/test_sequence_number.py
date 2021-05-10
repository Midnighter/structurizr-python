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

"""Ensure the correct behaviour of SequenceNumber."""

from structurizr.view.sequence_number import SequenceNumber


def test_basic_sequence():
    """Test simple incrementing sequence."""
    seq = SequenceNumber()
    assert seq.get_next() == "1"
    assert seq.get_next() == "2"
    assert seq.get_next() == "3"


def test_parallel_sequences():
    """Test "parallel" sequences."""
    seq = SequenceNumber()
    assert seq.get_next() == "1"

    seq.start_parallel_sequence()
    assert seq.get_next() == "2"
    seq.end_parallel_sequence(False)

    seq.start_parallel_sequence()
    assert seq.get_next() == "2"
    seq.end_parallel_sequence(True)

    assert seq.get_next() == "3"
