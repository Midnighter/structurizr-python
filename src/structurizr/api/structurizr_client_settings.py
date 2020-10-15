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


"""Provide the Structurizr client settings."""


import logging
from getpass import getuser
from pathlib import Path
from socket import getfqdn


try:
    from importlib.metadata import version
except ModuleNotFoundError:
    from importlib_metadata import version

from pydantic import UUID4, BaseSettings, DirectoryPath, Field, HttpUrl


__all__ = ("StructurizrClientSettings",)


logger = logging.getLogger(__name__)


try:
    USER = getuser()
except ModuleNotFoundError:
    logger.error(
        "Could not determine the username. Please set it manually or provide a "
        "STRUCTURIZR_USER environment variable."
    )
    USER = "anonymous"
hostname = getfqdn()
if hostname:
    USER = f"{USER}@{hostname}"

AGENT = f"structurizr-python/{version('structurizr-python')}"


class StructurizrClientSettings(BaseSettings):
    """
    Define the Structurizr client settings.

    Attributes:
        url (str): The Structurizr API URL.
        workspace_id (int): The Structurizr workspace identifier.
        api_key (str): The Structurizr workspace API key.
        api_secret (str): The Structurizr workspace API secret.
        user (str): A string identifying the user (e.g. an e-mail address or username).
        agent (str): A string identifying the agent (e.g. 'structurizr-java/1.2.0').
        workspace_archive_location (pathlib.Path): A directory for archiving downloaded
            workspaces.

    """

    url: HttpUrl = Field(
        default="https://api.structurizr.com",
        env="STRUCTURIZR_URL",
        description="The Structurizr API URL.",
    )
    workspace_id: int = Field(
        ...,
        env="STRUCTURIZR_WORKSPACE_ID",
        description="The Structurizr workspace identifier.",
    )
    api_key: UUID4 = Field(
        ...,
        env="STRUCTURIZR_API_KEY",
        description="The Structurizr workspace API key.",
    )
    api_secret: UUID4 = Field(
        ...,
        env="STRUCTURIZR_API_SECRET",
        description="The Structurizr workspace API secret.",
    )
    user: str = Field(
        default=USER,
        env="STRUCTURIZR_USER",
        description="A string identifying the user (e.g. an e-mail address or "
        "username).",
    )
    agent: str = Field(
        default=AGENT,
        env="STRUCTURIZR_AGENT",
        description="A string identifying the agent (e.g. 'structurizr-java/1.2.0').",
    )
    workspace_archive_location: DirectoryPath = Field(
        default=Path.cwd(),
        env="STRUCTURIZR_WORKSPACE_ARCHIVE_LOCATION",
        description="A directory for archiving downloaded workspaces.",
    )

    class Config:
        """Configure the Structurizr client settings."""

        case_sensitive = True
        env_prefix = "STRUCTURIZR_"
        env_file = ".env"
