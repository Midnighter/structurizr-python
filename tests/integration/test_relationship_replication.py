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


"""Test the behaviour when replicating relationships to element instances."""


import pytest

from structurizr.model import InteractionStyle, Model


@pytest.fixture(scope="function")
def empty_model() -> Model:
    """Provide an new empty model on demand for test cases to use."""
    return Model()


def test_replication_adds_relationships_in_the_same_environment(empty_model: Model):
    """Ensure within the same environment, relationships are replicated."""
    # Adapted from the Java ModelTests
    model = empty_model
    system1 = model.add_software_system("Software System 1")
    container1 = system1.add_container("Container 1")

    system2 = model.add_software_system("Software System 2")
    container2 = system2.add_container("Container 2")

    system3 = model.add_software_system("Software System 3")
    container3 = system3.add_container("Container 3")

    system4 = model.add_software_system("Software System 4")

    container1.uses(
        container2,
        "Uses 1",
        "Technology 1",
        interaction_style=InteractionStyle.Synchronous,
    )
    container2.uses(
        container3,
        "Uses 2",
        "Technology 2",
        interaction_style=InteractionStyle.Asynchronous,
    )
    container3.uses(system4)

    dev_deployment_node = model.add_deployment_node(
        "Deployment Node", environment="Development"
    )
    container_instance1 = dev_deployment_node.add_container(container1)
    container_instance2 = dev_deployment_node.add_container(container2)
    container_instance3 = dev_deployment_node.add_container(container3)
    system_instance = dev_deployment_node.add_software_system(system4)

    # The following live element instances should not affect the relationships of the
    # development element instances
    live_deployment_node = model.add_deployment_node(
        "Deployment Node", environment="Live"
    )
    live_deployment_node.add_container(container1)
    live_deployment_node.add_container(container2)
    live_deployment_node.add_container(container3)
    live_deployment_node.add_software_system(system4)

    assert len(container_instance1.relationships) == 1
    relationship = next(iter(container_instance1.relationships))
    assert relationship.source is container_instance1
    assert relationship.destination is container_instance2
    assert relationship.description == "Uses 1"
    assert relationship.technology == "Technology 1"
    assert relationship.interaction_style == InteractionStyle.Synchronous
    assert relationship.tags == set()

    assert len(container_instance2.relationships) == 1
    relationship = next(iter(container_instance2.relationships))
    assert relationship.source is container_instance2
    assert relationship.destination is container_instance3
    assert relationship.description == "Uses 2"
    assert relationship.technology == "Technology 2"
    assert relationship.interaction_style == InteractionStyle.Asynchronous
    assert relationship.tags == set()

    assert len(container_instance3.relationships) == 1
    relationship = next(iter(container_instance3.relationships))
    assert relationship.source is container_instance3
    assert relationship.destination is system_instance
    assert relationship.description == "Uses"
    assert relationship.technology == ""
    assert relationship.interaction_style == InteractionStyle.Synchronous
    assert relationship.tags == set()


def test_not_replicating_doesnt_add_relationships(empty_model: Model):
    """Ensure within the same environment, relationships are replicated."""
    # Adapted from the Java ModelTests
    model = empty_model
    system1 = model.add_software_system("Software System 1")
    container1 = system1.add_container("Container 1")

    system2 = model.add_software_system("Software System 2")
    container2 = system2.add_container("Container 2")

    system3 = model.add_software_system("Software System 3")
    container3 = system3.add_container("Container 3")

    system4 = model.add_software_system("Software System 4")

    container1.uses(
        container2,
        "Uses 1",
        "Technology 1",
        interaction_style=InteractionStyle.Synchronous,
    )
    container2.uses(
        container3,
        "Uses 2",
        "Technology 2",
        interaction_style=InteractionStyle.Asynchronous,
    )
    container3.uses(system4)

    dev_deployment_node = model.add_deployment_node(
        "Deployment Node", environment="Development"
    )
    container_instance1 = dev_deployment_node.add_container(
        container1, replicate_relationships=False
    )
    container_instance2 = dev_deployment_node.add_container(
        container2, replicate_relationships=False
    )
    container_instance3 = dev_deployment_node.add_container(
        container3, replicate_relationships=False
    )

    assert container_instance1.relationships == set()
    assert container_instance2.relationships == set()
    assert container_instance3.relationships == set()
