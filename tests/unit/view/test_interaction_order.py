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

"""Ensure the correct behaviour of InteractionOrder."""

from typing import List

import pytest

from structurizr.view.interaction_order import InteractionOrder


def test_basics():
    """Check basic ordering."""
    assert InteractionOrder("1") < InteractionOrder("2")
    assert not InteractionOrder("2") < InteractionOrder("1")
    assert not InteractionOrder("2") < InteractionOrder("2")


def test_construction_on_non_str_types():
    """Verify that InteractionOrder can be constructed on non-str types."""
    assert InteractionOrder(2) < InteractionOrder(10)


def test_comparing_bad_types_raises_error():
    """Test behaviour when trying to compare against a different type."""
    with pytest.raises(TypeError):
        if InteractionOrder("7") < 8:
            pass


def test_numeric_ordering():
    """Check numeric (rather than lexical) ordering is preserved."""
    assert InteractionOrder("1") < InteractionOrder("10")
    assert InteractionOrder("5") < InteractionOrder("10")


def test_multi_segment():
    """Test handling where orders are period-separated."""
    assert InteractionOrder("5.3") < InteractionOrder("5.10")
    assert InteractionOrder("5") < InteractionOrder("5.1")
    assert not InteractionOrder("5.1") < InteractionOrder("5")


def test_alphanumeric():
    """Test alphanumeric ordering works."""
    assert InteractionOrder("c") < InteractionOrder("d")
    assert InteractionOrder("2.a") < InteractionOrder("10.b")
    assert InteractionOrder("2a") < InteractionOrder("10b")


def test_sorting():
    """Test sorting works as expected."""

    def orders(list: List[str]) -> List[InteractionOrder]:
        return [InteractionOrder(s) for s in list]

    assert sorted(orders(["1.11", "1.1", "1.10"])) == orders(["1.1", "1.10", "1.11"])
    assert sorted(orders(["2c", "2a", "2"])) == orders(["2", "2a", "2c"])
    assert sorted(orders(["1", "1.1.1", "1.1"])) == orders(["1", "1.1", "1.1.1"])


def test_various_operators():
    """Check behaviour of operators other than less-than."""
    assert not InteractionOrder("1") == InteractionOrder("2")
    assert InteractionOrder("2") == InteractionOrder("2")

    assert InteractionOrder("1") != InteractionOrder("2")
    assert not InteractionOrder("2") != InteractionOrder("2")

    assert InteractionOrder("2") < InteractionOrder("10")
    assert not InteractionOrder("2") < InteractionOrder("2")
    assert not InteractionOrder("10") < InteractionOrder("2")
    assert InteractionOrder("2") <= InteractionOrder("10")
    assert InteractionOrder("2") <= InteractionOrder("2")
    assert not InteractionOrder("10") <= InteractionOrder("2")

    assert not InteractionOrder("2") > InteractionOrder("10")
    assert not InteractionOrder("2") > InteractionOrder("2")
    assert InteractionOrder("10") > InteractionOrder("2")
    assert not InteractionOrder("2") >= InteractionOrder("10")
    assert InteractionOrder("2") >= InteractionOrder("2")
    assert InteractionOrder("10") >= InteractionOrder("2")
