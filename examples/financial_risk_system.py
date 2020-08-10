# Copyright (c) 2020, Moritz E. Beber.
# Copyright (c) 2017, Sixty North AS.
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


"""Provide an example of the financial risk system."""


import logging

from structurizr import Workspace
from structurizr.model import InteractionStyle, Tags
from structurizr.view import Border, ElementStyle, RelationshipStyle, Shape


TAG_ALERT = "Alert"


def main() -> Workspace:
    """Create the financial risk system example."""

    ALERT_TAG = "Alert"

    workspace = Workspace(
        name="Financial Risk System",
        description="This is a simple (incomplete) example C4 model based upon the "
        "financial risk system architecture kata, which can be found at "
        "https://structurizr.com/help/examples.",
    )

    model = workspace.model

    financial_risk_system = model.add_software_system(
        name="Financial Risk System",
        description="Calculates the bank's exposure to risk for product X.",
    )

    business_user = model.add_person(
        name="Business User", description="A regular business user."
    )
    business_user.uses(
        destination=financial_risk_system, description="Views reports using"
    )

    configuration_user = model.add_person(
        name="Configuration User",
        description="A regular business user who can also configure the parameters "
        "used in the risk calculations.",
    )
    configuration_user.uses(
        destination=financial_risk_system, description="Configures parameters using"
    )

    trade_data_system = model.add_software_system(
        name="Trade Data System",
        description="The system of record for trades of type X.",
    )
    financial_risk_system.uses(
        destination=trade_data_system, description="Gets trade data from"
    )

    reference_data_system = model.add_software_system(
        name="Reference Data System",
        description="Manages reference data for all counterparties the bank interacts "
        "with.",
    )
    financial_risk_system.uses(
        destination=reference_data_system, description="Gets counterparty data from"
    )

    reference_data_system_v2 = model.add_software_system(
        name="Reference Data System v2.0",
        description="Manages reference data for all counterparties the bank interacts "
        "with.",
    )
    reference_data_system_v2.tags.add("Future State")
    financial_risk_system.uses(
        destination=reference_data_system_v2, description="Gets counterparty data from"
    ).tags.add("Future State")

    email_system = model.add_software_system(
        name="E-mail system", description="The bank's Microsoft Exchange system."
    )
    financial_risk_system.uses(
        destination=email_system,
        description="Sends a notification that a report is ready to",
    )
    email_system.delivers(
        destination=business_user,
        description="Sends a notification that a report is ready to",
        technology="E-mail message",
        interaction_style=InteractionStyle.Asynchronous,
    )

    central_monitoring_service = model.add_software_system(
        name="Central Monitoring Service",
        description="The bank's central monitoring and alerting dashboard.",
    )
    financial_risk_system.uses(
        destination=central_monitoring_service,
        description="Sends critical failure alerts to",
        technology="SNMP",
        interaction_style=InteractionStyle.Asynchronous,
    ).tags.add(ALERT_TAG)

    active_directory = model.add_software_system(
        name="Active Directory",
        description="The bank's authentication and authorisation system.",
    )
    financial_risk_system.uses(
        destination=active_directory,
        description="Uses for user authentication and authorisation",
    )

    views = workspace.views
    contextView = views.create_system_context_view(
        software_system=financial_risk_system,
        key="Context",
        description="An example System Context diagram for the Financial Risk System architecture kata.",
    )
    contextView.add_all_software_systems()
    contextView.add_all_people()

    styles = views.configuration.styles
    financial_risk_system.tags.add("Risk System")

    styles.add(ElementStyle(tag=Tags.ELEMENT, color="#ffffff", font_size=34))
    styles.add(ElementStyle(tag="Risk System", background="#550000", color="#ffffff"))
    styles.add(
        ElementStyle(
            tag=Tags.SOFTWARE_SYSTEM,
            width=650,
            height=400,
            background="#801515",
            shape=Shape.RoundedBox,
        )
    )
    styles.add(
        ElementStyle(
            tag=Tags.PERSON, width=550, background="#d46a6a", shape=Shape.Person
        )
    )

    styles.add(
        RelationshipStyle(
            tag=Tags.RELATIONSHIP, thickness=4, dashed=False, font_size=32, width=400
        )
    )
    styles.add(RelationshipStyle(tag=Tags.SYNCHRONOUS, dashed=False))
    styles.add(RelationshipStyle(tag=Tags.ASYNCHRONOUS, dashed=True))
    styles.add(RelationshipStyle(tag=ALERT_TAG, color="#ff0000"))
    styles.add(ElementStyle(tag="Future State", opacity=30, border=Border.Dashed))
    styles.add(RelationshipStyle(tag="Future State", opacity=30, dashed=True))

    return workspace


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    main()
