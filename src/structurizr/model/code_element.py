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


"""Provide a code element model."""


from pydantic import HttpUrl

from ..abstract_base import AbstractBase
from ..base_model import BaseModel
from .code_element_role import CodeElementRole


__all__ = ("CodeElement", "CodeElementIO")


class CodeElementIO(BaseModel):
    """
    Represent a code element.

    A code element is, for example, an interface, a class, a function, etc.
    that is part of the implementation of a component.

    Attributes:
        role: The role of this code element.
        name: The name of this code element.
        type: The type of the code element (e.g. a fully qualified Java
              interface or class name).
        description: A short description of this code element.
        url: A URL to the source code (e.g. a GitHub repo URL).
        package: Gets the (Java) package of this component (i.e. the package
                 of the primary code element).
        language: The programming language of this code element
                  (e.g. "Java", "C#", etc).
        category: The category of code element; e.g. class, interface, etc.
        visibility: The visibility of the code element; e.g. public, package,
                    private.
        size: The size of the code element; e.g. the number of lines.

    """

    role: CodeElementRole = CodeElementRole.Supporting
    name: str = ""
    type: str = ""
    description: str = ""
    url: HttpUrl = ""
    package: str = ""
    language: str = ""
    category: str = ""
    visibility: str = ""
    size: int = -1


class CodeElement(AbstractBase):
    """
    Represent a code element.

    A code element is, for example, an interface, a class, a function, etc.
    that is part of the implementation of a component.

    Attributes:
        role: The role of this code element.
        name: The name of this code element.
        type: The type of the code element (e.g. a fully qualified Java
              interface or class name).
        description: A short description of this code element.
        url: A URL to the source code (e.g. a GitHub repo URL).
        package: Gets the (Java) package of this component (i.e. the package
                 of the primary code element).
        language: The programming language of this code element
                  (e.g. "Java", "C#", etc).
        category: The category of code element; e.g. class, interface, etc.
        visibility: The visibility of the code element; e.g. public, package,
                    private.
        size: The size of the code element; e.g. the number of lines.

    """

    def __init__(
        self,
        *,
        role: CodeElementRole = CodeElementRole.Supporting,
        name: str = "",
        type: str = "",
        description: str = "",
        url: str = "",
        package: str = "",
        language: str = "",
        category: str = "",
        visibility: str = "",
        size: int = -1,
        **kwargs
    ) -> None:
        """Initialize a code element."""
        super().__init__(**kwargs)
        self.role = role
        self.name = name
        self.type = type
        self.description = description
        self.url = url
        self.package = package
        self.language = language
        self.category = category
        self.visibility = visibility
        self.size = size
