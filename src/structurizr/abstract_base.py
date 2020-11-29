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

    def __init__(self, **kwargs):
        """
        Initialize an abstract base class.

        The AbstractBase class is designed to be the singular root of the entire class
        hierarchy, similar to `object`, and acts as a guard against unknown keyword
        arguments. Any keyword arguments not consumed in the hierarchy above cause a
        `TypeError`.

        """
        if kwargs:
            phrase = (
                "unexpected keyword arguments"
                if len(kwargs) > 1
                else "an unexpected keyword argument"
            )
            message = "\n    ".join(f"{key}={value}" for key, value in kwargs.items())
            raise TypeError(
                f"{type(self).__name__}.__init__() got {phrase}:\n    {message}"
            )
        super().__init__()

    def __hash__(self) -> int:
        """Return an integer that represents a unique hash value for this instance."""
        return id(self)

    def __repr__(self) -> str:
        """Return a string representation of this instance."""
        return f"{type(self).__name__}({id(self)})"
