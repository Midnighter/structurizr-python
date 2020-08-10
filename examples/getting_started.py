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


"""
Provide a 'getting started' example.

Illustrate how to create a software architecture diagram using code.
"""


import logging

from structurizr import Workspace
from structurizr.model import Tags
from structurizr.view import ElementStyle, Shape
from structurizr.view.paper_size import PaperSize


def main() -> Workspace:
    """Create the 'getting started' example."""
    workspace = Workspace(
        name="Getting Started", description="This is a model of my software system.",
    )

    model = workspace.model

    user = model.add_person(name="User", description="A user of my software system.")
    software_system = model.add_software_system(
        name="Software System", description="My software system."
    )
    user.uses(software_system, "Uses")

    context_view = workspace.views.create_system_context_view(
        software_system=software_system,
        key="SystemContext",
        description="An example of a System Context diagram.",
    )
    context_view.add_all_elements()
    context_view.paper_size = PaperSize.A5_Landscape

    styles = workspace.views.configuration.styles
    styles.add(
        ElementStyle(tag=Tags.SOFTWARE_SYSTEM, background="#1168bd", color="#ffffff")
    )
    styles.add(
        ElementStyle(
            tag=Tags.PERSON, background="#08427b", color="#ffffff", shape=Shape.Person,
        )
    )
    return workspace


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    main()
