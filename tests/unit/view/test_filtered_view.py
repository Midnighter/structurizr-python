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


"""Ensure the expected behaviour of FilteredView."""


from structurizr.view.container_view import ContainerView
from structurizr.view.filtered_view import FilteredView, FilteredViewIO, FilterMode


def test_uses_view_key_if_view_specified():
    """Test the logic around base_view_key."""
    filtered_view = FilteredView(
        base_view_key="key1", description="test", mode=FilterMode.Exclude, tags=[]
    )
    assert filtered_view.base_view_key == "key1"

    filtered_view.view = ContainerView(key="static_key", description="container")
    assert filtered_view.base_view_key == "static_key"


def test_serialisation():
    """Test serialisation and deserialisation works."""
    container_view = ContainerView(key="static_key", description="container")
    filtered_view = FilteredView(
        key="filter1",
        view=container_view,
        description="test",
        mode=FilterMode.Exclude,
        tags=["v1"],
    )
    io = FilteredViewIO.from_orm(filtered_view)
    view2 = FilteredView.hydrate(io)

    assert view2.base_view_key == "static_key"
    assert view2.key == "filter1"
    assert view2.description == "test"
    assert view2.mode == FilterMode.Exclude
    assert view2.tags == {"v1"}


def test_tags_are_serialised_as_an_array():
    """Ensure that tags are serialised as an array, not comma-separated."""
    container_view = ContainerView(key="static_key", description="container")
    filtered_view = FilteredView(
        key="filter1",
        view=container_view,
        description="test",
        mode=FilterMode.Exclude,
        tags=["v1", "test"],
    )
    io = FilteredViewIO.from_orm(filtered_view).json()
    assert '"tags": ["v1", "test"]' in io
