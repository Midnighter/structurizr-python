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


"""Provide a customized base model."""


from pydantic import BaseModel as BaseModel_


__all__ = ("BaseModel",)


class BaseModel(BaseModel_):
    """Define a customized base model."""

    class Config:
        """Define default configuration options for all models."""

        anystr_strip_whitespace = True
        allow_population_by_field_name = True
        orm_mode = True
