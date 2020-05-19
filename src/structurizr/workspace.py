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


import gzip
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Union

from pydantic import Field

from .abstract_base import AbstractBase
from .base_model import BaseModel
from .model import Model, ModelIO
from .view import ViewSet, ViewSetIO


__all__ = ("WorkspaceIO", "Workspace")


class WorkspaceIO(BaseModel):
    """
    Represent a Structurizr workspace.

    A workspace is a wrapper for a software architecture model, views, and
    documentation.

    Attributes:
        id (int): The workspace ID.
        name (str): The name of the workspace.
        description (str): A short description of the workspace.
        version (str): A version number for the workspace.
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
    name: str = Field(..., description="The name of the workspace.")
    description: str = Field(..., description="A short description of the workspace.")
    version: Optional[str] = Field(
        None, description="A version number for the workspace."
    )
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
    model: Optional[ModelIO] = Field(None, description="A software architecture model.")
    views: Optional[ViewSetIO] = Field(
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


class Workspace(AbstractBase):
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

    def __init__(
        self,
        *,
        name: str,
        description: str,
        id: Optional[int] = None,
        version: Optional[str] = None,
        revision: Optional[int] = None,
        thumbnail: Optional[str] = None,
        last_modified_date: Optional[datetime] = None,
        last_modified_user: Optional[str] = None,
        last_modified_agent: Optional[str] = None,
        model: Optional[Model] = None,
        views: Optional[ViewSet] = None,
        # TODO
        documentation: Optional[Any] = None,
        # TODO
        configuration: Optional[Any] = None,
        **kwargs
    ) -> None:
        """
        Initialize a new workspace.

        Args:
            name:
            description:
            id:
            version:
            revision:
            thumbnail:
            last_modified_date:
            last_modified_user:
            last_modified_agent:
            model:
            views:
            documentation:
            configuration:
            **kwargs:

        """
        super().__init__(**kwargs)
        self.id = id
        self.name = name
        self.description = description
        self.version = version
        self.revision = revision
        self.thumbnail = thumbnail
        self.last_modified_date = last_modified_date
        self.last_modified_user = last_modified_user
        self.last_modified_agent = last_modified_agent
        self.model = Model() if model is None else model
        self.views = ViewSet(model=self.model) if views is None else views
        self.documentation = documentation
        self.configuration = configuration

    @classmethod
    def load(cls, filename: Union[str, Path]) -> "Workspace":
        """"""
        filename = Path(filename)
        try:
            with gzip.open(filename, "rt") as handle:
                ws_io = WorkspaceIO.parse_raw(handle.read())
        except FileNotFoundError as error:
            raise error
        except OSError:
            with filename.open() as handle:
                ws_io = WorkspaceIO.parse_raw(handle.read())
        return cls.hydrate(ws_io)

    @classmethod
    def hydrate(cls, workspace_io: WorkspaceIO) -> "Workspace":
        """"""
        return cls(
            id=workspace_io.id,
            name=workspace_io.name,
            description=workspace_io.description,
            version=workspace_io.version,
            model=Model.hydrate(workspace_io.model),
            last_modified_date=workspace_io.last_modified_date,
            last_modified_user=workspace_io.last_modified_user,
            last_modified_agent=workspace_io.last_modified_agent,
        )
