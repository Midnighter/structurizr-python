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


"""Provide a common abstract base class."""


from abc import ABC


__all__ = ("AbstractBase",)


class AbstractBase(ABC):
    """Define common business logic through an abstract base class."""

    def __hash__(self) -> int:
        """Return an integer that represents a unique hash value for this instance."""
        return id(self)
