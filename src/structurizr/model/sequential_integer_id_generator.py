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


"""Provide a sequential integer ID generator."""


__all__ = ("SequentialIntegerIDGenerator",)


class SequentialIntegerIDGenerator:
    """Define a sequential integer ID generator."""

    def __init__(self, **kwargs) -> None:
        """Initialize a new generator."""
        super().__init__(**kwargs)
        self._counter = 0

    def generate_id(self, **kwargs) -> str:
        """
        Generate a new sequential integer ID.

        Returns:
            str: The generated ID as a string.

        """
        self._counter += 1
        return str(self._counter)

    def found(self, id: str) -> None:
        """
        Update the generator with an existing ID.

        The ID is used to update the internal counter, if it can be converted to an
        integer.

        Args:
            id (str): The externally created ID.

        """
        try:
            id_as_int = int(id)
        except ValueError:
            pass
        else:
            if id_as_int > self._counter:
                self._counter = id_as_int
