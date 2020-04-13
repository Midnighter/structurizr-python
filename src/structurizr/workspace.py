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


"""Provide the workspace model."""


from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field

from .model import Model


__all__ = ("Workspace",)


class Workspace(BaseModel):
    """
    Represent a Structurizr workspace.

    A workspace is a wrapper for a software architecture model, views, and
    documentation.

    Attributes:
        id (int): The workspace ID.
        name (str): The name of the workspace.
        description (str): A short description of the workspace.
        version (str): A version number for the workspace.
        revision (int): The internal revision number.
        thumbnail (str): The thumbnail associated with the workspace; a Base64
            encoded PNG file as a Data URI (data:image/png;base64).
        last_modified_date (datetime.datetime): The last modified date, in ISO 8601
            format (e.g. "2018-09-08T12:40:03Z").
        last_modified_user (str): A string identifying the user who last modified the
            workspace (e.g. an e-mail address or username).
        last_modified_agent (str): A string identifying the agent that was last used to
            modify the workspace (e.g. "structurizr-java/1.2.0").
        model (Model): A software architecture model.
        views (Views): The set of views onto a software architecture model.
        documentation (Documentation): The documentation associated with this software
            architecture model.
        configuration (WorkspaceConfiguration): The workspace configuration.

    """

    id: int = Field(..., description="The workspace ID.")
    name: Optional[str] = Field(None, description="The name of the workspace.")
    description: Optional[str] = Field(
        None, description="A short description of the workspace."
    )
    version: Optional[str] = Field(
        None, description="A version number for the workspace."
    )
    revision: Optional[int] = Field(None, description="The internal revision number.")
    thumbnail: Optional[str] = Field(
        None,
        description="The thumbnail associated with the workspace; a Base64 encoded PNG"
        " file as a Data URI (data:image/png;base64).",
    )
    last_modified_date: Optional[datetime] = Field(
        None,
        alias="lastModifiedDate",
        description="The last modified date, in ISO 8601 format"
        " (e.g. '2018-09-08T12:40:03Z').",
    )
    last_modified_user: Optional[str] = Field(
        None,
        alias="lastModifiedUser",
        description="A string identifying the user who last modified the workspace"
        " (e.g. an e-mail address or username).",
    )
    last_modified_agent: Optional[str] = Field(
        None,
        alias="lastModifiedAgent",
        description="A string identifying the agent that was last used to modify the"
        " workspace (e.g. 'structurizr-java/1.2.0').",
    )
    model: Optional[Model] = Field(None, description="A software architecture model.")
    views: Optional[Any] = Field(
        None, description="The set of views onto a software architecture model."
    )
    documentation: Optional[Any] = Field(
        None,
        description="The documentation associated with this software architecture "
        "model.",
    )
    configuration: Optional[Any] = Field(
        None, description="The workspace configuration."
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = Model()
