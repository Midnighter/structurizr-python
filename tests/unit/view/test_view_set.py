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

"""Ensure the correct behaviour of ViewSet."""

import pytest

from structurizr.view.view_set import ViewSet, ViewSetIO


class MockModel:
    """Mock model for testing."""

    pass


@pytest.fixture(scope="function")
def empty_model() -> MockModel:
    """Provide an emptty model for testing."""
    return MockModel()


def test_view_set_construction(empty_model):
    """Test constructing a new view set."""
    viewset = ViewSet(model=empty_model)
    assert viewset.model is empty_model
    assert viewset.dynamic_views == set()


def test_adding_dynamic_view(empty_model):
    """Check adding dyanmic view initialises it properly."""
    viewset = ViewSet(model=empty_model)
    view = viewset.create_dynamic_view(description="test")
    assert view.model is empty_model
    assert view.get_viewset() is viewset
    assert view.description == "test"
    assert view in viewset.dynamic_views


def test_dynamic_view_hydrated(empty_model):
    """Check dynamic views hydrated properly."""
    viewset = ViewSet(model=empty_model)
    viewset.create_dynamic_view(key="dyn1", description="dynamic")
    io = ViewSetIO.from_orm(viewset)

    new_viewset = ViewSet.hydrate(io, empty_model)
    assert len(new_viewset.dynamic_views) == 1
    assert list(new_viewset.dynamic_views)[0].description == "dynamic"


@pytest.mark.xfail(strict=True)
def test_copying_layout(empty_model):
    """Check copying layout from another viewset."""
    assert 1 == 0  # TODO
