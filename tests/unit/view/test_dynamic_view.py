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
from structurizr.model import Container, SoftwareSystem
from structurizr.view.dynamic_view import DynamicView, DynamicViewIO


@pytest.fixture(scope="function")
def empty_workspace() -> Workspace:
    """Provide an empty Workspace on demand for test cases to use."""
    return Workspace(name="Name", description="Description")


def test_create_new_dynamic_view(empty_workspace: Workspace):
    """Test basic construction."""
    view = DynamicView(description="Test view")
    assert view.description == "Test view"


def test_cosntructor_param_validation(empty_workspace: Workspace):
    """Test validation of constructor parameters."""
    system = SoftwareSystem(name="sys1")
    container = Container(name="con1")

    view1 = DynamicView(description="Description")
    assert view1.element is None
    view2 = DynamicView(description="Description", software_system=system)
    assert view2.element is system
    view3 = DynamicView(description="Description", container=container)
    assert view3.element is container
    with pytest.raises(ValueError, match="You cannot specify"):
        DynamicView(
            description="Description", software_system=system, container=container
        )


def test_hydration(empty_workspace: Workspace):
    """Check dehydrating and hydrating."""
    system = empty_workspace.model.add_software_system(name="system", id="sys1")

    view = DynamicView(key="dyn1", description="Description", software_system=system)
    view.set_model(empty_workspace.model)

    io = DynamicViewIO.from_orm(view)
    d = io.dict()
    assert d["elementId"] == "sys1"

    view2 = DynamicView.hydrate(io, element=system)
    assert view2.key == "dyn1"
    assert view2.description == "Description"
    assert view2.element is system
