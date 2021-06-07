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

"""Ensure the correct behaviour of ViewOrder."""

from typing import List

import pytest

from structurizr.view.view_order import ViewOrder


def test_basics():
    """Check basic ordering."""
    assert ViewOrder("1") < ViewOrder("2")
    assert not ViewOrder("2") < ViewOrder("1")
    assert not ViewOrder("2") < ViewOrder("2")


def test_comparing_bad_types_raises_error():
    """Test behaviour when trying to compare against a different type."""
    with pytest.raises(TypeError):
        if ViewOrder("7") < 8:
            pass


def test_numeric_ordering():
    """Check numeric (rather than lexical) ordering is preserved."""
    assert ViewOrder("1") < ViewOrder("10")
    assert ViewOrder("5") < ViewOrder("10")


def test_multi_segment():
    """Test handling where orders are period-separated."""
    assert ViewOrder("5.3") < ViewOrder("5.10")
    assert ViewOrder("5") < ViewOrder("5.1")
    assert not ViewOrder("5.1") < ViewOrder("5")


def test_alphanumeric():
    """Test alphanumeric ordering works."""
    assert ViewOrder("c") < ViewOrder("d")
    assert ViewOrder("2.a") < ViewOrder("10.b")
    assert ViewOrder("2a") < ViewOrder("10b")


def test_sorting():
    """Test sorting works as expected."""

    def orders(list: List[str]) -> List[ViewOrder]:
        return [ViewOrder(s) for s in list]

    assert sorted(orders(["1.11", "1.1", "1.10"])) == orders(["1.1", "1.10", "1.11"])
    assert sorted(orders(["2c", "2a", "2"])) == orders(["2", "2a", "2c"])
    assert sorted(orders(["1", "1.1.1", "1.1"])) == orders(["1", "1.1", "1.1.1"])


def test_various_operators():
    """Check behaviour of operators other than less-than."""
    assert not ViewOrder("1") == ViewOrder("2")
    assert ViewOrder("2") == ViewOrder("2")

    assert ViewOrder("1") != ViewOrder("2")
    assert not ViewOrder("2") != ViewOrder("2")

    assert ViewOrder("2") < ViewOrder("10")
    assert not ViewOrder("2") < ViewOrder("2")
    assert not ViewOrder("10") < ViewOrder("2")
    assert ViewOrder("2") <= ViewOrder("10")
    assert ViewOrder("2") <= ViewOrder("2")
    assert not ViewOrder("10") <= ViewOrder("2")

    assert not ViewOrder("2") > ViewOrder("10")
    assert not ViewOrder("2") > ViewOrder("2")
    assert ViewOrder("10") > ViewOrder("2")
    assert not ViewOrder("2") >= ViewOrder("10")
    assert ViewOrder("2") >= ViewOrder("2")
    assert ViewOrder("10") >= ViewOrder("2")
