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


"""Provide an abstract base class for the software architecture model."""


from abc import ABC

from pydantic import BaseModel

from .sequential_integer_id_generator import SequentialIntegerIDGenerator


__all__ = ("AbstractModel",)


class AbstractModel(BaseModel, ABC):
    """
    Define an abstract base class for the software architecture model.

    Using an abstract base class avoids some of the circular dependencies caused by
    importing and annotating types.

    See Also:
        Model

    """

    # Using slots for 'private' attributes prevents them from being included in model
    # serialization. See https://github.com/samuelcolvin/pydantic/issues/655
    # for a longer discussion.
    __slots__ = ("_elements_by_id", "_relationships_by_id", "_id_generator")

    def __init__(self, **kwargs):
        """
        Initialize the base model with its 'private' attributes.

        Args:
            **kwargs: Passed on to the parent constructor.

        """
        super().__init__(**kwargs)
        # Using `object.__setattr__` is a workaround for setting a 'private' attribute
        # on a pydantic model. See https://github.com/samuelcolvin/pydantic/issues/655
        # for a longer discussion.
        object.__setattr__(self, "_elements_by_id", {})
        object.__setattr__(self, "_relationships_by_id", {})
        object.__setattr__(self, "_id_generator", SequentialIntegerIDGenerator())
