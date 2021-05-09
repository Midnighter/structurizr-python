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

"""Ensure the correct behaviour of DynamicView."""

import pytest

from structurizr import Workspace
from structurizr.view.dynamic_view import DynamicView


@pytest.fixture(scope="function")
def empty_workspace() -> Workspace:
    """Provide an empty Workspace on demand for test cases to use."""
    return Workspace(name="Name", description="Description")


def test_create_new_dynamic_view(empty_workspace: Workspace):
    """Test basic construction."""
    view = DynamicView(description="Test view")
    assert view.description == "Test view"


@pytest.mark.xfail(strict=True)
def test_hydration(empty_workspace: Workspace):
    """Check hydrating and dehydrating."""
    assert 1 == 0  # TODO
