# Copyright (c) 2020, Moritz E. Beber.
#
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


"""Ensure the expected behaviour of the architectural perspective model."""


import pytest
from pydantic import ValidationError

from structurizr.model.perspective import Perspective


@pytest.mark.parametrize(
    "attributes",
    [
        pytest.param(
            {},
            marks=pytest.mark.raises(
                exception=ValidationError, message="name\n  field required"
            ),
        ),
        pytest.param(
            {},
            marks=pytest.mark.raises(
                exception=ValidationError, message="description\n  field required"
            ),
        ),
        {
            "name": "Accessibility",
            "description": "The ability of the system to be used by people with "
            "disabilities.",
        },
    ],
)
def test_perspective_init(attributes):
    """Expect proper initialization from arguments."""
    perspective = Perspective(**attributes)
    for attr, expected in attributes.items():
        assert getattr(perspective, attr) == expected
