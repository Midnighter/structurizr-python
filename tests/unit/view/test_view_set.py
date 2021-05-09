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

from structurizr.model.model import Model
from structurizr.view.view_set import ViewSet, ViewSetIO


@pytest.fixture(scope="function")
def empty_model() -> Model:
    """Provide an empty model for testing."""
    return Model()


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
    system1 = empty_model.add_software_system(name="sys1")
    viewset.create_dynamic_view(
        key="dyn1", description="dynamic", software_system=system1
    )
    io = ViewSetIO.from_orm(viewset)

    new_viewset = ViewSet.hydrate(io, empty_model)
    assert len(new_viewset.dynamic_views) == 1
    view = list(new_viewset.dynamic_views)[0]
    assert view.description == "dynamic"
    assert view.element is system1


@pytest.mark.xfail(strict=True)
def test_copying_layout(empty_model):
    """Check copying layout from another viewset."""
    assert 1 == 0  # TODO
