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


"""Provide the Structurizr client."""


import gzip
import hashlib
import hmac
import logging
from base64 import b64encode
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict
from urllib.parse import unquote_plus

import httpx

from ..workspace import Workspace, WorkspaceIO
from .api_response import APIResponse
from .structurizr_client_exception import StructurizrClientException
from .structurizr_client_settings import StructurizrClientSettings


__all__ = ("StructurizrClient",)


logger = logging.getLogger(__name__)


class StructurizrClient:
    """
    Define a Structurizr client.

    A client for the Structurizr API (https://api.structurizr.com) that allows you to
    get and put Structurizr workspaces in a JSON format.

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

    def __init__(self, *, settings: StructurizrClientSettings, **kwargs):
        """
        Initialize a Structurizr client.

        Notes:
            Any unprovided arguments are attempted to be loaded from environment
            variables or a `.env` file.

        Keyword Args:
            settings (StructurizrClientSettings): The client configuration.

        """
        super().__init__(**kwargs)
        self.url = str(settings.url)
        self.workspace_id = settings.workspace_id
        self.api_key = str(settings.api_key)
        self.api_secret = str(settings.api_secret)
        self.user = settings.user
        self.agent = settings.agent
        self.workspace_archive_location = settings.workspace_archive_location
        self._workspace_url = f"/workspace/{self.workspace_id}"
        self._lock_url = f"{self._workspace_url}/lock"
        self._params = {
            "user": settings.user,
            "agent": settings.agent,
        }
        self._application_json = "application/json; charset=UTF-8"
        self._client = httpx.Client(
            base_url=self.url, headers={"User-Agent": self.agent},
        )

    def __repr__(self) -> str:
        """Return a string representation of the client."""
        return (
            f"{type(self).__name__}(url={self.url}, workspace_id={self.workspace_id})"
        )

    def __enter__(self):
        """Enter a context by locking the corresponding remote workspace."""
        is_successful = self.lock_workspace()
        if not is_successful:
            raise StructurizrClientException(
                f"Failed to lock the Structurizr workspace {self.workspace_id}."
            )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit a context by unlocking the corresponding remote workspace."""
        is_successful = self.unlock_workspace()
        self._client.close()
        if exc_type is None and not is_successful:
            raise StructurizrClientException(
                f"Failed to unlock the Structurizr workspace {self.workspace_id}."
            )

    def close(self) -> None:
        """Close the connection pool."""
        self._client.close()

    def get_workspace(self) -> Workspace:
        """
        Retrieve a Structurizr workspace from the API.

        Returns:
            Workspace: A workspace instance that represents the online state.

        Raises:
            httpx.HTTPError: If anything goes wrong in connecting to the API.

        """
        request = self._client.build_request("GET", self._workspace_url)
        request.headers.update(self._add_headers(request.url.full_path,))
        response = self._client.send(request)
        if response.status_code != 200:
            raise StructurizrClientException(
                f"Failed to retrieve the Structurizr workspace {self.workspace_id}.\n"
                f"Response {response.status_code} - {response.reason_phrase}"
            )
        logger.debug(response.text)
        self._archive_workspace(response.text)
        return Workspace.hydrate(WorkspaceIO.parse_raw(response.text))

    def put_workspace(self, workspace: Workspace) -> None:
        """
        Update the remote Structurizr workspace with the given instance.

        Args:
            workspace (Workspace): The new workspace to update with.

        Raises:
            httpx.HTTPError: If anything goes wrong in connecting to the API.

        """
        assert workspace.id == self.workspace_id
        ws_io = WorkspaceIO.from_orm(workspace)
        ws_io.thumbnail = None
        ws_io.last_modified_date = datetime.now(timezone.utc)
        ws_io.last_modified_agent = self.agent
        ws_io.last_modified_user = self.user
        workspace_json = ws_io.json(by_alias=True, exclude_none=True)
        logger.debug(workspace_json)
        request = self._client.build_request(
            "PUT", self._workspace_url, data=workspace_json
        )
        request.headers.update(
            self._add_headers(
                request.url.full_path,
                method="PUT",
                content=workspace_json,
                content_type=self._application_json,
            )
        )
        response = self._client.send(request)
        if response.status_code != 200:
            raise StructurizrClientException(
                f"Failed to update the Structurizr workspace {self.workspace_id}.\n"
                f"HTTP Status {response.status_code} - {response.reason_phrase}"
            )

    def lock_workspace(self) -> bool:
        """
        Lock the Structurizr workspace.

        Returns:
            bool: `True` if the workspace could be locked, `False` otherwise.

        """
        request = self._client.build_request("PUT", self._lock_url, params=self._params)
        request.headers.update(self._add_headers(request.url.full_path, method="PUT"))
        response = self._client.send(request)
        response.raise_for_status()
        response = APIResponse.parse_raw(response.text)
        if not response.success:
            logger.error(
                f"Failed to lock workspace {self.workspace_id}. {response.message}"
            )
        return response.success

    def unlock_workspace(self) -> bool:
        """
        Unlock the Structurizr workspace.

        Returns:
            bool: `True` if the workspace could be unlocked, `False` otherwise.

        """
        request = self._client.build_request(
            "DELETE", self._lock_url, params=self._params
        )
        request.headers.update(
            self._add_headers(request.url.full_path, method="DELETE")
        )
        response = self._client.send(request)
        response.raise_for_status()
        response = APIResponse.parse_raw(response.text)
        if not response.success:
            logger.error(
                f"Failed to unlock workspace {self.workspace_id}. {response.message}"
            )
        return response.success

    def _add_headers(
        self,
        url_path: str,
        method: str = "GET",
        content: str = "",
        content_type: str = "",
    ) -> Dict[str, str]:
        """
        Prepare the Structurizr specific headers.

        Args:
            url_path (str): The URL path to the workspace or lock.
            method (str): One of the HTTP verbs.
            content (str): The workspace definition as JSON.
            content_type (str): The content MIME-type (e.g. 'application/json').

        Returns:
            dict: Items in the dictionary define headers and their values.

        """
        definition_md5 = self._md5(content)
        nonce = self._number_once()
        message_digest = self._message_digest(
            method, unquote_plus(url_path), definition_md5, content_type, nonce,
        )
        logger.debug("The message digest:\n{message_digest}")
        message_hash = self._base64_str(self._hmac_hex(self.api_secret, message_digest))
        logger.debug("The hashed message digest: '{message_hash}'.")
        headers = {
            "X-Authorization": f"{self.api_key}:{message_hash}",
            "Nonce": nonce,
        }
        if method == "PUT":
            headers["Content-MD5"] = self._base64_str(definition_md5)
            headers["Content-Type"] = content_type
        return headers

    def _archive_workspace(self, json: str) -> None:
        """Store the workspace."""
        location = self._create_archive_filename()
        logger.debug(
            f"Archiving workspace {self.workspace_id} to"
            f" '{self.workspace_archive_location}'."
        )
        with gzip.open(location, mode="wt") as handle:
            handle.write(json)

    def _create_archive_filename(self) -> Path:
        """Generate a filename for a workspace archive."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return self.workspace_archive_location.joinpath(
            f"structurizr-{self.workspace_id}-{timestamp}.json.gz"
        )

    @staticmethod
    def _number_once() -> str:
        """Return a unique number as a string."""
        # The number of microseconds since the epoch.
        return str(
            int((datetime.utcnow() - datetime(1970, 1, 1)) / timedelta(microseconds=1))
        )

    @staticmethod
    def _hmac_hex(secret: str, digest: str) -> str:
        """Hash the given digest using HMAC+SHA256 and return the hex string."""
        return hmac.new(
            secret.encode("utf-8"), digest.encode("utf-8"), "sha256"
        ).hexdigest()

    @staticmethod
    def _md5(content: str) -> str:
        """Return the MD5 hash of the given string."""
        return hashlib.md5(content.encode("utf-8")).hexdigest()

    @staticmethod
    def _base64_str(content: str) -> str:
        """Return the base64 encoded string."""
        return b64encode(content.encode("utf-8")).decode("utf-8")

    @staticmethod
    def _message_digest(
        http_verb: str,
        uri_path: str,
        definition_md5: str,
        content_type: str,
        nonce: str,
    ) -> str:
        """Assemble the complete message digest."""
        return f"{http_verb}\n{uri_path}\n{definition_md5}\n{content_type}\n{nonce}\n"
