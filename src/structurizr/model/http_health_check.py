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


"""Provide an HTTP health check model."""


from typing import Dict, Iterable

from pydantic import Field, HttpUrl

from ..abstract_base import AbstractBase
from ..base_model import BaseModel


__all__ = ("HTTPHealthCheck", "HTTPHealthCheckIO")


class HTTPHealthCheckIO(BaseModel):
    """
    Describe an HTTP-based health check.

    Attributes:
        name: The name of the health check.
        url: The health check URL/endpoint.
        interval: The polling interval, in seconds.
        timeout: The timeout after which a health check is deemed as failed,
                 in milliseconds.
        headers: A set of name-value pairs corresponding to HTTP headers that
                 should be sent with the request.

     """

    name: str = ""
    url: HttpUrl = ""
    interval: int = 30
    timeout: int = 5_000
    headers: Dict[str, str] = Field({})


class HTTPHealthCheck(AbstractBase):
    """
    Describe an HTTP-based health check.

    Attributes:
        name: The name of the health check.
        url: The health check URL/endpoint.
        interval: The polling interval, in seconds.
        timeout: The timeout after which a health check is deemed as failed,
                 in milliseconds.
        headers: A set of name-value pairs corresponding to HTTP headers that
                 should be sent with the request.

     """

    def __init__(
        self,
        *,
        name: str = "",
        url: str = "",
        interval: int = 30,
        timeout: int = 5_000,
        headers: Iterable = (),
        **kwargs,
    ):
        """Initialize an HTTP health check."""
        super().__init__(**kwargs)
        self.name = name
        self.url = url
        self.interval = interval
        self.timeout = timeout
        self.headers = dict(headers)
