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

"""
Ensure that relationships in Elements and in the Model are consistent.

See https://github.com/Midnighter/structurizr-python/issues/31.
"""

from pathlib import Path

import pytest

from structurizr import Workspace


DEFINITIONS = Path(__file__).parent / "data" / "workspace_definition"


@pytest.mark.parametrize(
    "filename",
    ["BigBank.json"],
)
def test_model_deserialises_deployment_nodes(filename: str):
    """Ensure deserialisaton of deployment nodes works."""
    path = DEFINITIONS / filename
    workspace = Workspace.load(path)
    model = workspace.model

    db_server = model.get_element("59")
    assert db_server.name == "Docker Container - Database Server"
    assert db_server is not None
    assert db_server.model is model
    assert db_server.parent.name == "Developer Laptop"
    assert db_server.parent.parent is None
