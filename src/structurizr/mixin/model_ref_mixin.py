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


"""Provide a mixin that includes a model reference."""


from typing import TYPE_CHECKING
from weakref import ref


if TYPE_CHECKING:
    from ..model import Model


__all__ = ("ModelRefMixin",)


class ModelRefMixin:
    """Define a model reference mixin."""

    def __init__(self, **kwargs) -> None:
        """Initialize the mixin."""
        super().__init__(**kwargs)
        self._model = lambda: None

    def get_model(self) -> "Model":
        """
        Retrieve the model instance from the reference.

        Returns:
            Model: The model, if any.

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
        Create a weak reference to the model instance.

        Warnings:
            This is an internal method and should not be directly called by users.

        Args:
            model (Model):

        """
        self._model = ref(model)
