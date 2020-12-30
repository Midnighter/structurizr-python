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


"""Ensure the expected behaviour of DeploymentView."""


from structurizr.view.container_view import ContainerView, ContainerViewIO


def test_external_system_boundary_preserved():
    """Test the externalSoftwareSystemBoundariesVisible flag appears in the JSON.

    Not having this set means that Structurizr assumes it is false (see
    https://github.com/Midnighter/structurizr-python/issues/67).  When exported
    from Structurizr, the flag is present whether true or false, so check that
    is also the case here.
    """
    view = ContainerView(
        key="key",
        description="description",
        external_software_system_boundary_visible=True,
    )
    json = ContainerViewIO.from_orm(view).json()
    assert '"externalSoftwareSystemBoundariesVisible": true' in json

    view = ContainerView(
        key="key",
        description="description",
        external_software_system_boundary_visible=False,
    )
    json = ContainerViewIO.from_orm(view).json()
    assert '"externalSoftwareSystemBoundariesVisible": false' in json
