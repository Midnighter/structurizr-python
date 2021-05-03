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

"""Ensure grouping works with example workspace."""

from pathlib import Path

from structurizr import Workspace


DEFINITIONS = Path(__file__).parent / "data" / "workspace_definition"


def test_loading_workspace_with_groups():
    """Check loading an example workspace with groupings defined."""
    path = DEFINITIONS / "Grouping.json"

    workspace = Workspace.load(path)
    consumer_a = workspace.model.get_element("1")
    consumer_d = workspace.model.get_element("4")
    assert consumer_a.name == "Consumer A"
    assert consumer_a.group == "Consumers - Group 1"
    assert consumer_d.name == "Consumer D"
    assert consumer_d.group == "Consumers - Group 2"

    service_2_api = workspace.model.get_element("9")
    assert service_2_api.name == "Service 2 API"
    assert service_2_api.group == "Service 2"
