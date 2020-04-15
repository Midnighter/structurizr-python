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


"""Provide a superclass for all model elements."""


from abc import ABC
from typing import TYPE_CHECKING, Iterator
from weakref import ref

from pydantic import Field, HttpUrl

from .model_item import ModelItem


if TYPE_CHECKING:
    from .model import Model
    from .relationship import Relationship


__all__ = ("Element",)


class Element(ModelItem, ABC):
    """
    Define a superclass for all model elements.

    Attributes:
        name (str):
        description (str):
        url (pydantic.HttpUrl):

    """

    # Using slots for 'private' attributes prevents them from being included in model
    # serialization. See https://github.com/samuelcolvin/pydantic/issues/655
    # for a longer discussion.
    __slots__ = ("_model",)

    name: str = Field(...)
    description: str = ""
    url: HttpUrl = ""

    def __init__(self, **kwargs) -> None:
        """Initialize an element with an empty 'private' model reference."""
        super().__init__(**kwargs)
        # Using `object.__setattr__` is a workaround for setting a 'private' attribute
        # on a pydantic model. See https://github.com/samuelcolvin/pydantic/issues/655
        # for a longer discussion.
        object.__setattr__(self, "_model", lambda: None)

    def get_model(self) -> "Model":
        """
        Retrieve the model instance that contains this element.

        Returns:
            AbstractModel: The model that contains this element if any.

        Raises:
            RuntimeError: In case there exists no referenced model.

        """
        model = self._model()
        if model is None:
            raise RuntimeError(
                f"You must add this {type(self).__name__} element to a model instance "
                f"first."
            )
        return model

    def set_model(self, model: "Model") -> None:
        """
        Create a weak reference to the C4 model instance that contains this element.

        Warnings:
            This is an internal method and should not be directly called by users.

        Args:
            model (Model):

        """
        # Using `object.__setattr__` is a workaround for setting a 'private' attribute
        # on a pydantic model. See https://github.com/samuelcolvin/pydantic/issues/655
        # for a longer discussion.
        object.__setattr__(self, "_model", ref(model))

    def get_relationships(self) -> Iterator["Relationship"]:
        """Return a Iterator over all relationships involving this element."""
        return (
            r
            for r in self.get_model().get_relationships()
            if self is r.source or self is r.destination
        )

    def get_efferent_relationships(self) -> Iterator["Relationship"]:
        """Return a Iterator over all outgoing relationships involving this element."""
        return (r for r in self.get_model().get_relationships() if self is r.source)

    def get_afferent_relationships(self) -> Iterator["Relationship"]:
        """Return a Iterator over all incoming relationships involving this element."""
        return (
            r for r in self.get_model().get_relationships() if self is r.destination
        )
