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


"""Ensure the expected outcomes of helper functions."""


from structurizr import helpers


def test_show_versions(capsys):
    """Expect a semi-defined output of package information."""
    helpers.show_versions()
    captured = capsys.readouterr()
    lines = captured.out.split("\n")
    assert lines[1].startswith("System Information")
    assert lines[2].startswith("==================")
    assert lines[3].startswith("OS")
    assert lines[4].startswith("OS-release")
    assert lines[5].startswith("Python")

    assert lines[7].startswith("Package Versions")
    assert lines[8].startswith("================")
    assert any(l.startswith("structurizr-python") for l in lines[9:])
