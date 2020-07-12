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


"""Ensure correct workspace (de-)serialization."""


from importlib import import_module
from pathlib import Path

import pytest
from pydantic import ValidationError

from structurizr import Workspace, WorkspaceIO
from structurizr.model import ModelIO


DEFINITIONS = Path(__file__).parent / "data" / "workspace_definition"
EXAMPLES = Path(__file__).parent.parent.parent / "examples"
VALIDATIONS = Path(__file__).parent / "data" / "workspace_validation"


def pytest_generate_tests(metafunc) -> None:
    if "invalid_workspace" in metafunc.fixturenames:
        files = sorted(Path("data", "workspace_validation").glob("*.json.gz"))
        ids = [p.name for p in files]
        metafunc.parametrize(
            "invalid_workspace",
            [
                pytest.param(f, marks=pytest.mark.raises(exception=ValidationError))
                for f in files
            ],
            ids=ids,
        )


def test_invalid_workspace(invalid_workspace):
    WorkspaceIO.parse_file(invalid_workspace)


@pytest.mark.parametrize("filename", ["Trivial.json.gz", "GettingStarted.json.gz"])
def test_deserialize_workspace(filename):
    """Expect that a trivial workspace definition is successfully deserialized."""
    path = DEFINITIONS / filename
    Workspace.load(path)


@pytest.mark.xfail(reason="Workspace and model comparison is still id dependent.")
@pytest.mark.parametrize(
    "example, filename", [("getting_started", "GettingStarted.json.gz")]
)
def test_serialize_workspace(example, filename, monkeypatch):
    """Expect that ."""
    monkeypatch.syspath_prepend(EXAMPLES)
    example = import_module(example)
    path = DEFINITIONS / filename
    expected = ModelIO.from_orm(Workspace.load(path).model)
    assert ModelIO.from_orm(example.main().model) == expected
