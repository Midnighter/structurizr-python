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

from typing import Iterable

import pytest

from structurizr.model.model import Model
from structurizr.view.container_view import ContainerView
from structurizr.view.filtered_view import FilterMode
from structurizr.view.paper_size import PaperSize
from structurizr.view.view_set import ViewSet, ViewSetIO


@pytest.fixture(scope="function")
def empty_model() -> Model:
    """Provide an empty model for testing."""
    yield Model()


@pytest.fixture(scope="function")
def empty_viewset(empty_model) -> ViewSet:
    """Provide an empty viewset for testing."""
    yield ViewSet(model=empty_model)


def test_view_set_construction(empty_model):
    """Test constructing a new view set."""
    viewset = ViewSet(model=empty_model)
    assert viewset.model is empty_model
    assert count(viewset.dynamic_views) == 0


def test_adding_dynamic_view(empty_model):
    """Check adding dyanmic view initialises it properly."""
    viewset = ViewSet(model=empty_model)
    view = viewset.create_dynamic_view(key="dyn1", description="test")
    assert view.model is empty_model
    assert view.get_viewset() is viewset
    assert view.description == "test"
    assert view in viewset.dynamic_views


def test_dynamic_view_hydrated(empty_viewset):
    """Check dynamic views hydrated properly."""
    viewset = empty_viewset
    system1 = viewset.model.add_software_system(name="sys1")
    viewset.create_dynamic_view(key="dyn1", description="dynamic", element=system1)
    io = ViewSetIO.from_orm(viewset)

    new_viewset = ViewSet.hydrate(io, viewset.model)
    assert count(new_viewset.dynamic_views) == 1
    view = list(new_viewset.dynamic_views)[0]
    assert view.description == "dynamic"
    assert view.element is system1


def test_copying_dynamic_view_layout(empty_viewset):
    """Check that layout info is copied over for Dynamic views."""
    source_viewset = empty_viewset
    source_view = source_viewset.create_dynamic_view(key="dyn1", description="test")
    source_view.paper_size = PaperSize.A4_Landscape

    target_viewset = ViewSet(model=empty_viewset.model)

    # Check it's OK if there isn't a matching view in the target
    target_viewset.copy_layout_information_from(source_viewset)

    # Now try one where we have a match
    target_view = target_viewset.create_dynamic_view(key="dyn1", description="test2")
    assert target_view.paper_size is None
    target_viewset.copy_layout_information_from(source_viewset)
    assert target_view.paper_size == PaperSize.A4_Landscape


@pytest.mark.xfail(strict=True)
def test_copying_layout(empty_model):
    """Check copying layout from other view types."""
    assert 1 == 0  # TODO


def test_filtered_view_hydrated(empty_viewset):
    """Check dynamic views hydrated properly."""
    viewset = empty_viewset
    system1 = viewset.model.add_software_system(name="sys1")
    container_view = viewset.create_container_view(
        key="container1", description="container", software_system=system1
    )
    viewset.create_filtered_view(
        key="filter1",
        view=container_view,
        description="filtered",
        mode=FilterMode.Include,
        tags=["v2"],
    )
    io = ViewSetIO.from_orm(viewset)

    new_viewset = ViewSet.hydrate(io, viewset.model)
    assert count(new_viewset.filtered_views) == 1
    view = list(new_viewset.filtered_views)[0]
    assert view.description == "filtered"
    assert isinstance(view.view, ContainerView)
    assert view.view.key == "container1"


def test_getting_view_by_key(empty_viewset):
    """Check retrieving views by key from the ViewSet."""
    viewset = empty_viewset
    system1 = viewset.model.add_software_system(name="sys1")
    container_view = viewset.create_container_view(
        key="container1", description="container", software_system=system1
    )

    assert viewset.get_view("container1") is container_view
    assert viewset.get_view("bogus") is None
    assert viewset["container1"] is container_view
    with pytest.raises(KeyError):
        viewset["bogus"]


def test_no_key_raises_error(empty_viewset):
    """Test that key must be specified."""
    viewset = empty_viewset
    system1 = viewset.model.add_software_system(name="sys1")

    with pytest.raises(ValueError, match="A key must be specified"):
        viewset.create_container_view(description="container", software_system=system1)


def test_empty_key_raises_error(empty_viewset):
    """Test that key must not be empty."""
    viewset = empty_viewset
    system1 = viewset.model.add_software_system(name="sys1")

    with pytest.raises(ValueError, match="A key must be specified"):
        viewset.create_container_view(
            key="", description="container", software_system=system1
        )


def test_duplicate_key_raises_error(empty_viewset):
    """Test that key cannot be a duplicate of another view."""
    viewset = empty_viewset
    system1 = viewset.model.add_software_system(name="sys1")

    viewset.create_container_view(
        key="container1", description="container", software_system=system1
    )
    with pytest.raises(ValueError, match="View already exists"):
        viewset.create_container_view(
            key="container1", description="container", software_system=system1
        )


def count(iterable: Iterable) -> int:
    """Count items in an iterable, as len doesn't work on generators."""
    return sum(1 for x in iterable)
