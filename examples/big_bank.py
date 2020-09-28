# Copyright (c) 2020, Moritz E. Beber.
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Provide a 'Big Bank' example.

Illustrate how to create a software architecture diagram using code, based on
https://github.com/structurizr/dsl/blob/master/examples/big-bank-plc.dsl.
"""


import logging

from structurizr import Workspace
from structurizr.model import Enterprise, Location, Tags
from structurizr.view import ElementStyle, PaperSize, RelationshipStyle, Shape


def main():
    """Standard entry point for examples.  Do not rename."""
    return create_big_bank_workspace()


def create_big_bank_workspace():
    """Create the big bank example."""

    workspace = Workspace(
        name="Big Bank plc",
        description=(
            "This is an example workspace to illustrate the key features of "
            "Structurizr, based around a fictional online banking system."
        ),
    )

    existing_system_tag = "Existing System"
    bank_staff_tag = "Bank Staff"
    web_browser_tag = "Web Browser"
    mobile_app_tag = "Mobile App"
    database_tag = "Database"
    failover_tag = "Failover"

    model = workspace.model
    views = workspace.views

    model.enterprise = Enterprise(name="Big Bank plc")

    # people and software systems
    customer = model.add_person(
        location=Location.External,
        name="Personal Banking Customer",
        description="A customer of the bank, with personal bank accounts.",
        id="customer",
    )

    internet_banking_system = model.add_software_system(
        location=Location.Internal,
        name="Internet Banking System",
        description=(
            "Allows customers to view information about "
            "their bank accounts, and make payments."
        ),
        id="internetBankingSystem",
    )
    customer.uses(
        internet_banking_system, "Views account balances, and makes payments using"
    )

    mainframe_banking_system = model.add_software_system(
        location=Location.Internal,
        name="Mainframe Banking System",
        description=(
            "Stores all of the core banking information "
            "about customers, accounts, transactions, etc."
        ),
        id="mainframe",
    )
    mainframe_banking_system.tags.add(existing_system_tag)
    internet_banking_system.uses(
        mainframe_banking_system,
        "Gets account information from, and makes payments using",
    )

    email_system = model.add_software_system(
        location=Location.Internal,
        name="E-mail System",
        description="The internal Microsoft Exchange e-mail system.",
        id="email",
    )
    internet_banking_system.uses(
        destination=email_system,
        description="Sends e-mail using",
    )
    email_system.tags.add(existing_system_tag)
    email_system.delivers(
        destination=customer,
        description="Sends e-mails to",
    )

    atm = model.add_software_system(
        location=Location.Internal,
        name="ATM",
        description="Allows customers to withdraw cash.",
        id="atm",
    )
    atm.tags.add(existing_system_tag)
    atm.uses(mainframe_banking_system, "Uses")
    customer.uses(atm, "Withdraws cash using")

    customer_service_staff = model.add_person(
        location=Location.Internal,
        name="Customer Service Staff",
        description="Customer service staff within the bank.",
        id="supportStaff",
    )
    customer_service_staff.tags.add(bank_staff_tag)
    customer_service_staff.uses(mainframe_banking_system, "Uses")
    customer.interacts_with(
        customer_service_staff, "Asks questions to", technology="Telephone"
    )

    backOfficeStaff = model.add_person(
        location=Location.Internal,
        name="Back Office Staff",
        description="Administration and support staff within the bank.",
        id="backoffice",
    )
    backOfficeStaff.tags.add(bank_staff_tag)
    backOfficeStaff.uses(mainframe_banking_system, "Uses")

    # containers
    single_page_application = internet_banking_system.add_container(
        "Single-Page Application",
        (
            "Provides all of the Internet banking functionality "
            "to customers via their web browser."
        ),
        "JavaScript and Angular",
        id="singlePageApplication",
    )
    single_page_application.tags.add(web_browser_tag)
    mobile_app = internet_banking_system.add_container(
        "Mobile App",
        "Provides a limited subset of the Internet banking functionality to customers via their mobile device.",
        "Xamarin",
        id="mobileApp",
    )
    mobile_app.tags.add(mobile_app_tag)
    web_application = internet_banking_system.add_container(
        "Web Application",
        "Delivers the static content and the Internet banking single page application.",
        "Java and Spring MVC",
        id="webApplication",
    )
    api_application = internet_banking_system.add_container(
        "API Application",
        "Provides Internet banking functionality via a JSON/HTTPS API.",
        "Java and Spring MVC",
        id="apiApplication",
    )
    database = internet_banking_system.add_container(
        "Database",
        "Stores user registration information, hashed authentication credentials, access logs, etc.",
        "Relational Database Schema",
        id="database",
    )
    database.tags.add(database_tag)

    customer.uses(web_application, "Uses", technology="HTTPS")
    customer.uses(single_page_application, "Uses")
    customer.uses(mobile_app, "Uses")
    web_application.uses(
        single_page_application, "Delivers to the customers web browser"
    )
    api_application.uses(database, "Reads from and writes to", technology="JDBC")
    api_application.uses(mainframe_banking_system, "Uses", technology="XML/HTTPS")
    api_application.uses(email_system, "Sends e-mail using", technology="SMTP")

    # components
    # - for a real-world software system, you would probably want to extract the components using
    # - static analysis/reflection rather than manually specifying them all

    signin_controller = api_application.add_component(
        name="Sign In Controller",
        description="Allows users to sign in to the Internet Banking System.",
        technology="Spring MVC Rest Controller",
        id="signinController",
    )
    accounts_summary_controller = api_application.add_component(
        name="Accounts Summary Controller",
        description="Provides customers with a summary of their bank accounts.",
        technology="Spring MVC Rest Controller",
        id="accountsSummaryController",
    )
    reset_password_controller = api_application.add_component(
        name="Reset Password Controller",
        description="Allows users to reset their passwords with a single use URL.",
        technology="Spring MVC Rest Controller",
        id="resetPasswordController",
    )
    security_component = api_application.add_component(
        name="Security Component",
        description="Provides functionality related to signing in, changing passwords, etc.",
        technology="Spring Bean",
        id="securityComponent",
    )
    mainframe_banking_systemFacade = api_application.add_component(
        name="Mainframe Banking System Facade",
        description="A facade onto the mainframe banking system.",
        technology="Spring Bean",
        id="mainframeBankingSystemFacade",
    )
    email_component = api_application.add_component(
        name="E-mail Component",
        description="Sends e-mails to users.",
        technology="Spring Bean",
        id="emailComponent",
    )

    for component in api_application.components:
        if component.technology == "Spring MVC Rest Controller":
            single_page_application.uses(component, "Makes API calls to", "JSON/HTTPS")
            mobile_app.uses(component, "Makes API calls to", "JSON/HTTPS")

    signin_controller.uses(security_component, "Uses")
    accounts_summary_controller.uses(mainframe_banking_systemFacade, "Uses")
    reset_password_controller.uses(security_component, "Uses")
    reset_password_controller.uses(email_component, "Uses")
    security_component.uses(database, "Reads from and writes to", "JDBC")
    mainframe_banking_systemFacade.uses(mainframe_banking_system, "Uses", "XML/HTTPS")
    email_component.uses(email_system, "Sends e-mail using")

    # TODO:!
    # model.AddImplicitRelationships()

    # # deployment nodes and container instances
    # developer_laptop = model.add_deployment_node(
    #     environment="Development",
    #     name="Developer Laptop",
    #     description="A developer laptop.",
    #     technology="Microsoft Windows 10 or Apple macOS",
    # )
    # apache_tomcat = developer_laptop.add_deployment_node(
    #     name="Docker - Web Server",
    #     description="A Docker container.",
    #     technology="Docker",
    # ).add_deployment_node(
    #     name="Apache Tomcat",
    #     description="An open source Java EE web server.",
    #     technology="Apache Tomcat 8.x",
    #     instances=1,
    #     properties={"Xmx": "512M", "Xms": "1024M", "Java Version": "8"},
    # )
    # apache_tomcat.add_container(webApplication)
    # apache_tomcat.Add(apiApplication)

    # developer_laptop.add_deployment_node(
    #     "Docker - Database Server", "A Docker container.", "Docker"
    # ).add_deployment_node(
    #     "Database Server", "A development database.", "Oracle 12c"
    # ).Add(
    #     database
    # )

    # developer_laptop.add_deployment_node(
    #     "Web Browser", "", "Chrome, Firefox, Safari, or Edge"
    # ).Add(single_page_application)

    # customer_mobile_device = model.add_deployment_node(
    #     "Live", "Customer's mobile device", "", "Apple iOS or Android"
    # )
    # customer_mobile_device.Add(mobile_app)

    # customer_computer = model.add_deployment_node(
    #     "Live", "Customer's computer", "", "Microsoft Windows or Apple macOS"
    # )
    # customer_computer.add_deployment_node(
    #     "Web Browser", "", "Chrome, Firefox, Safari, or Edge"
    # ).Add(single_page_application)

    # bigBankDataCenter = model.add_deployment_node(
    #     "Live", "Big Bank plc", "", "Big Bank plc data center"
    # )

    # liveWebServer = bigBankDataCenter.add_deployment_node(
    #     "bigbank-web***",
    #     "A web server residing in the web server farm, accessed via F5 BIG-IP LTMs.",
    #     "Ubuntu 16.04 LTS",
    #     4,
    #     DictionaryUtils.Create("Location=London and Reading"),
    # )
    # liveWebServer.add_deployment_node(
    #     "Apache Tomcat",
    #     "An open source Java EE web server.",
    #     "Apache Tomcat 8.x",
    #     1,
    #     DictionaryUtils.Create("Xmx=512M", "Xms=1024M", "Java Version=8"),
    # ).Add(webApplication)

    # liveApiServer = bigBankDataCenter.add_deployment_node(
    #     "bigbank-api***",
    #     "A web server residing in the web server farm, accessed via F5 BIG-IP LTMs.",
    #     "Ubuntu 16.04 LTS",
    #     8,
    #     DictionaryUtils.Create("Location=London and Reading"),
    # )
    # liveApiServer.add_deployment_node(
    #     "Apache Tomcat",
    #     "An open source Java EE web server.",
    #     "Apache Tomcat 8.x",
    #     1,
    #     DictionaryUtils.Create("Xmx=512M", "Xms=1024M", "Java Version=8"),
    # ).Add(apiApplication)

    # primaryDatabaseServer = bigBankDataCenter.add_deployment_node(
    #     "bigbank-db01",
    #     "The primary database server.",
    #     "Ubuntu 16.04 LTS",
    #     1,
    #     DictionaryUtils.Create("Location=London"),
    # ).add_deployment_node(
    #     "Oracle - Primary", "The primary, live database server.", "Oracle 12c"
    # )
    # primaryDatabaseServer.Add(database)

    # bigBankdb02 = bigBankDataCenter.add_deployment_node(
    #     "bigbank-db02",
    #     "The secondary database server.",
    #     "Ubuntu 16.04 LTS",
    #     1,
    #     DictionaryUtils.Create("Location=Reading"),
    # )
    # bigBankdb02.tags.add(FailoverTag)
    # secondaryDatabaseServer = bigBankdb02.add_deployment_node(
    #     "Oracle - Secondary",
    #     "A secondary, standby database server, used for failover purposes only.",
    #     "Oracle 12c",
    # )
    # secondaryDatabaseServer.tags.add(FailoverTag)
    # secondaryDatabase = secondaryDatabaseServer.Add(database)

    # # model.Relationships.Where(r=>r.Destination.Equals(secondaryDatabase)).ToList().ForEach(r=>r.tags.add(FailoverTag))
    # dataReplicationRelationship = primaryDatabaseServer.uses(
    #     secondaryDatabaseServer, "Replicates data to", ""
    # )
    # secondaryDatabase.tags.add(FailoverTag)

    # views/diagrams
    system_landscape_view = views.create_system_landscape_view(
        key="SystemLandscape",
        description="The system landscape diagram for Big Bank plc.",
    )
    system_landscape_view.add_all_elements()
    system_landscape_view.paper_size = PaperSize.A5_Landscape

    system_context_view = views.create_system_context_view(
        software_system=internet_banking_system,
        key="SystemContext",
        description="The system context diagram for the Internet Banking System.",
    )
    system_context_view.enterprise_boundary_visible = False
    system_context_view.add_nearest_neighbours(internet_banking_system)
    system_context_view.paper_size = PaperSize.A5_Landscape

    container_view = views.create_container_view(
        software_system=internet_banking_system,
        key="Containers",
        description="The container diagram for the Internet Banking System.",
    )
    container_view.add(customer)
    container_view.add_all_containers()
    container_view.add(mainframe_banking_system)
    container_view.add(email_system)
    container_view.paper_size = PaperSize.A5_Landscape

    component_view = views.create_component_view(
        container=api_application,
        key="Components",
        description="The component diagram for the API Application.",
    )
    component_view.add(mobile_app)
    component_view.add(single_page_application)
    component_view.add(database)
    component_view.add_all_components()
    component_view.add(mainframe_banking_system)
    component_view.add(email_system)
    component_view.paper_size = PaperSize.A5_Landscape

    # systemLandscapeView.AddAnimation(internet_banking_system, customer, mainframe_banking_system, emailSystem)
    # systemLandscapeView.AddAnimation(atm)
    # systemLandscapeView.AddAnimation(customerServiceStaff, backOfficeStaff)

    # systemContextView.AddAnimation(internet_banking_system)
    # systemContextView.AddAnimation(customer)
    # systemContextView.AddAnimation(mainframe_banking_system)
    # systemContextView.AddAnimation(emailSystem)

    # containerView.AddAnimation(customer, mainframe_banking_system, emailSystem)
    # containerView.AddAnimation(webApplication)
    # containerView.AddAnimation(singlePageApplication)
    # containerView.AddAnimation(mobile_app)
    # containerView.AddAnimation(apiApplication)
    # containerView.AddAnimation(database)

    # componentView.AddAnimation(singlePageApplication, mobile_app)
    # componentView.AddAnimation(signinController, securityComponent, database)
    # componentView.AddAnimation(accountsSummaryController, mainframe_banking_systemFacade, mainframe_banking_system)
    # componentView.AddAnimation(resetPasswordController, emailComponent, database)

    # # dynamic diagrams and deployment diagrams are not available with the Free Plan
    # DynamicView dynamicView = views.CreateDynamicView(apiApplication, "SignIn", "Summarises how the sign in feature works in the single-page application.")
    # dynamicView.Add(singlePageApplication, "Submits credentials to", signinController)
    # dynamicView.Add(signinController, "Calls isAuthenticated() on", securityComponent)
    # dynamicView.Add(securityComponent, "select * from users where username = ?", database)
    # dynamicView.PaperSize = PaperSize.A5_Landscape

    # DeploymentView developmentDeploymentView = views.CreateDeploymentView(internet_banking_system, "DevelopmentDeployment", "An example development deployment scenario for the Internet Banking System.")
    # developmentDeploymentView.Environment = "Development"
    # developmentDeploymentView.Add(developerLaptop)
    # developmentDeploymentView.PaperSize = PaperSize.A5_Landscape

    # DeploymentView liveDeploymentView = views.CreateDeploymentView(internet_banking_system, "LiveDeployment", "An example live deployment scenario for the Internet Banking System.")
    # liveDeploymentView.Environment = "Live"
    # liveDeploymentView.Add(bigBankDataCenter)
    # liveDeploymentView.Add(customerMobileDevice)
    # liveDeploymentView.Add(customerComputer)
    # liveDeploymentView.Add(dataReplicationRelationship)
    # liveDeploymentView.PaperSize = PaperSize.A5_Landscape

    # colours, shapes and other diagram styling
    styles = views.configuration.styles
    styles.add(
        ElementStyle(tag=Tags.SOFTWARE_SYSTEM, background="#1168bd", color="#ffffff")
    )
    styles.add(ElementStyle(tag=Tags.CONTAINER, background="#438dd5", color="#ffffff"))
    styles.add(ElementStyle(tag=Tags.COMPONENT, background="#85bbf0", color="#000000"))
    styles.add(
        ElementStyle(
            tag=Tags.PERSON,
            background="#08427b",
            color="#ffffff",
            shape=Shape.Person,
            font_size=22,
        )
    )
    styles.add(
        ElementStyle(tag=existing_system_tag, background="#999999", color="#ffffff")
    )
    styles.add(ElementStyle(tag=bank_staff_tag, background="#999999", color="#ffffff"))
    styles.add(ElementStyle(tag=web_browser_tag, shape=Shape.WebBrowser))
    styles.add(ElementStyle(tag=mobile_app_tag, shape=Shape.MobileDeviceLandscape))
    styles.add(ElementStyle(tag=database_tag, shape=Shape.Cylinder))
    styles.add(ElementStyle(tag=failover_tag, opacity=25))
    styles.add(RelationshipStyle(tag=failover_tag, opacity=25, position=70))

    return workspace


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    main()
