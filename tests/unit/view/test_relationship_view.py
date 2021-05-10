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

"""Ensure the correct behaviour of RelationshipView."""

from structurizr.view.relationship_view import RelationshipView, RelationshipViewIO


def test_dynamic_view_specifics_serialise():
    """Ensure that the fields used by DynamicView get (de)serialised OK."""
    view = RelationshipView(id="id1", order="5", response=True)
    io = RelationshipViewIO.from_orm(view)
    json = io.json()
    assert '"order": "5"' in json
    assert '"response": true' in json

    view2 = RelationshipView.hydrate(io)
    assert view2.order == "5"
    assert view2.response

    # Check response is suppressed in json when False
    view.response = False
    io = RelationshipViewIO.from_orm(view)
    json = io.json()
    assert "response" not in json
    view2 = RelationshipView.hydrate(io)
    assert not view2.response
